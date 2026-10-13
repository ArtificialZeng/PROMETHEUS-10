#!/usr/bin/env python3
"""Build a GitHub-ready SmallMac overlay on the PROMETHEUS-10 release tree.

The input projects must already have passed the local release gate and have a
checked ``release/submission.zip`` created by the 6physics-research bundle tool.
This script validates every frozen bundle member before copying it.  It never
copies source literature, browser records, worker logs, or credentials.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath


UPSTREAM_COMMIT = "a2f0e6e50de892bf3544990ce41c444435edc540"
UPSTREAM_ARCHIVE_SHA256 = "722effaefadefc61f3e59f9d70f720d2fbfb29ed09f7091793a9b313ec5ceaa1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def public_id(original: str) -> str:
    if original == "PHY-13":
        return "phys-smallmac00000-p13"
    if original == "PHY-14":
        return "phys-smallmac00000-p14"
    if original.startswith("phys-smallmac"):
        return original
    match = re.fullmatch(r"phys-(\d{5})-p(\d{2})", original)
    if match:
        return f"phys-smallmac{match.group(1)}-p{match.group(2)}"
    raise ValueError(f"cannot assign SmallMac ID to {original}")


def brace_argument(text: str, command: str) -> str:
    match = re.search(rf"\\{re.escape(command)}(?:\[[^]]*\])?\s*\{{", text)
    if not match:
        return ""
    start = match.end()
    depth = 1
    index = start
    while index < len(text) and depth:
        if text[index] == "{" and (index == 0 or text[index - 1] != "\\"):
            depth += 1
        elif text[index] == "}" and (index == 0 or text[index - 1] != "\\"):
            depth -= 1
        index += 1
    return text[start : index - 1] if depth == 0 else ""


def plain_title(tex: bytes) -> str:
    value = brace_argument(tex.decode("utf-8", "replace"), "title")
    value = re.sub(r"(?m)%.*$", "", value)
    value = re.sub(r"\\(?:protect|newline|linebreak|allowbreak)\b(?:\s*\[[^]]*\])?", " ", value)
    value = value.replace("\\\\", " ").replace("~", " ")
    value = re.sub(r"\\(?:textbf|textit|emph|texorpdfstring)\{([^{}]*)\}", r"\1", value)
    value = value.replace("{", "").replace("}", "")
    value = value.replace("--", "–").replace("``", "“").replace("''", "”")
    value = re.sub(r"\\([#$%&_])", r"\1", value)
    return " ".join(value.split())


def text_portability(data: bytes, original: str, research_root: Path) -> tuple[bytes, list[str]]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data, []
    project_root = research_root / "projects" / original
    xcode_python = str(Path("/", "Library", "Developer", "CommandLineTools", "usr", "bin", "python3"))
    system_python = str(Path("/", "usr", "bin", "python3"))
    replacements = [
        (xcode_python, "python3", "Xcode command-line Python executable"),
        (system_python, "python3", "system Python executable"),
        (str(research_root / "runtime" / "venv" / "bin" / "python3"), "python3", "python executable"),
        (str(project_root), ".", "project root"),
        (str(research_root), "<original-research-root>", "research root provenance"),
        (str(Path.home()), "<original-home>", "home provenance"),
    ]
    notes: list[str] = []
    for old, new, label in replacements:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            notes.append(f"{label}: {count} replacement(s)")
    return text.encode("utf-8"), notes


def claim_class(kind: str, status: str) -> str:
    if kind == "resolution-paper" and status == "proved":
        return "Proof"
    if kind == "resolution-paper" and status == "disproved":
        return "Disproof"
    if kind == "computational-paper":
        return "Computational result"
    if kind == "method-note":
        return "Method result"
    if kind == "conjecture-note":
        return "Conjecture note"
    return "Partial result"


def scope_label(status: str) -> str:
    return {"proved": "proved", "disproved": "disproved", "unresolved": "unresolved"}.get(status, status)


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def escape_prose(value: str) -> str:
    """Prevent scientific interval notation from being parsed as Markdown links."""
    return value.replace("[", "\\[").replace("]", "\\]")


def project_materials(project: Path) -> tuple[list[str], list[str], list[str]]:
    guides: list[str] = []
    code: list[str] = []
    requirements: list[str] = []
    code_suffixes = {".py", ".sage", ".jl", ".m", ".nb", ".ipynb"}
    for path in sorted(project.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(project).as_posix()
        lower_name = path.name.lower()
        if path.suffix.lower() == ".md" and relative != "README.md" and (
            "reproduc" in lower_name or lower_name == "readme.md"
        ):
            guides.append(relative)
        if path.suffix.lower() in code_suffixes:
            code.append(relative)
        if lower_name in {"requirements.txt", "environment.yml", "environment.yaml", "pyproject.toml"}:
            requirements.append(relative)
    return guides, code, requirements


LANGUAGES = (
    ("en", "README.md", "English"),
    ("zh-CN", "README.zh-CN.md", "中文"),
    ("de", "README.de.md", "Deutsch"),
    ("fr", "README.fr.md", "Français"),
    ("ja", "README.ja.md", "日本語"),
    ("ru", "README.ru.md", "Русский"),
)
CATEGORIES = (
    ("Proof", "proofs"),
    ("Disproof", "disproofs"),
    ("Partial result", "partial-results"),
    ("Computational result", "computational-papers"),
)
INDEX_LABELS = {
    "en": {
        "title": "small_mac physics collection",
        "lead": "Forty-eight AI-assisted physics manuscripts packaged as inspectable research drafts.",
        "notice": "Every small_mac item passed the recorded local science, manuscript and release gates. Human author review remains required; these are not externally peer-reviewed or accepted publications.",
        "scope_notice": "Classification follows the frozen release record. Proof and Disproof refer to the stated claim and its assumptions; partial and computational results do not imply that the original question is fully solved. Consult each PDF and author handoff for the exact scientific scope and limitations.",
        "identity": "Display numbers 11–58, batch identifiers and original internal project IDs are preserved. The public `phys-smallmac` IDs point to the canonical project directories. The mapping is recorded in",
        "title_policy": "Manuscript titles retain the language of each frozen paper.",
        "number": "No.", "batch": "Batch", "project": "Public project ID", "original": "Original internal ID", "paper": "Manuscript / PDF", "scope": "Original question", "materials": "Code / replay", "code": "Code", "guide": "Replay guide", "category": "Category", "count": "Manuscripts",
        "outcomes": ("Proof", "Disproof", "Partial result", "Computational result"),
        "scopes": {"proved": "proved", "disproved": "disproved", "unresolved": "unresolved"},
        "browse": "Browse by recorded result class", "collection": "Full small_mac collection", "root": "PROMETHEUS-10 portfolio", "batch_status": "Detailed batch-status supplement (Chinese source titles)",
        "repro": "Reproducibility", "repro_text": "Each project contains the frozen PDF, manuscript source, release-selected code/data, an author handoff, provenance and SHA-256 checksums. Run from the repository root:",
        "root_title": "small_mac extension: 48 manuscripts by result class",
        "root_lead": "This repository contains **{total} manuscripts**: the original ten PROMETHEUS-10 projects and **{count} small_mac physics manuscripts**. The original ten projects and their scientific scope are documented below.",
    },
    "zh-CN": {
        "title": "small_mac 物理成果集",
        "lead": "本成果集收录 48 篇由 AI 辅助完成、可检查的物理研究草稿。",
        "notice": "每个 small_mac 项目均通过已记录的本地科学、文稿和发布门禁，但仍须作者人工审阅；这不等于外部同行评审或期刊接收。",
        "scope_notice": "分类依据冻结的发布记录。“证明”与“反证”针对文稿所述命题及其假设；部分结果与计算结果不代表原题已完全解决。具体科学范围和局限须查阅各篇 PDF 与作者交接文件。",
        "identity": "保留显示序号 11–58、批次编号和原始内部项目 ID。公开 `phys-smallmac` ID 均指向同一项目目录，映射记录见",
        "title_policy": "论文题名保留各冻结文稿中的原始语言。",
        "number": "序号", "batch": "批次", "project": "公开项目 ID", "original": "原始内部 ID", "paper": "论文题名 / PDF", "scope": "原题状态", "materials": "代码 / 复现", "code": "代码", "guide": "复现指南", "category": "成果类型", "count": "篇数",
        "outcomes": ("证明", "反证", "部分结果", "计算结果"),
        "scopes": {"proved": "已证明", "disproved": "已反证", "unresolved": "仍未完全解决"},
        "browse": "按已记录的成果类型浏览", "collection": "完整 small_mac 成果集", "root": "PROMETHEUS-10 首页", "batch_status": "按批次查看原题、解决程度、续研信心与未解决原因",
        "repro": "复现", "repro_text": "每个项目均含冻结 PDF、论文源码、发布门禁选定的代码/数据、作者交接、包来源记录和 SHA-256 校验。从仓库根目录运行：",
        "root_title": "small_mac 扩展：48 篇论文按成果分类",
        "root_lead": "本仓库共含 **{total} 篇论文草稿**：原 PROMETHEUS-10 的十项，以及 **{count} 篇 small_mac 物理论文草稿**。原有十项及其科学边界保留在下方。",
    },
    "de": {
        "title": "small_mac-Physiksammlung",
        "lead": "Diese Sammlung enthält 48 KI-unterstützte, überprüfbar verpackte Forschungsmanuskripte zur Physik.",
        "notice": "Alle small_mac-Einträge haben die dokumentierten lokalen Wissenschafts-, Manuskript- und Freigabekontrollen bestanden. Eine menschliche Autorenprüfung bleibt erforderlich; externe Begutachtung oder Annahme wird nicht behauptet.",
        "scope_notice": "Die Einteilung folgt dem eingefrorenen Freigabevermerk. Beweis und Widerlegung betreffen die formulierte Aussage unter ihren Annahmen; Teil- und Rechenergebnisse lösen die Ausgangsfrage nicht notwendigerweise vollständig. Die genaue wissenschaftliche Reichweite und Grenzen stehen im PDF und in der Autorenübergabe.",
        "identity": "Anzeigenummern 11–58, Chargenkennungen und ursprüngliche interne Projektkennungen bleiben erhalten. Öffentliche `phys-smallmac`-Kennungen verweisen auf die kanonischen Projektverzeichnisse. Die Zuordnung steht in",
        "title_policy": "Die Manuskripttitel bleiben in der Sprache des jeweiligen eingefrorenen Dokuments erhalten.",
        "number": "Nr.", "batch": "Charge", "project": "Öffentliche Projektkennung", "original": "Ursprüngliche interne Kennung", "paper": "Manuskript / PDF", "scope": "Ausgangsfrage", "materials": "Code / Reproduktion", "code": "Code", "guide": "Reproduktionsanleitung", "category": "Ergebnisklasse", "count": "Manuskripte",
        "outcomes": ("Beweis", "Widerlegung", "Teilergebnis", "Rechenergebnis"),
        "scopes": {"proved": "bewiesen", "disproved": "widerlegt", "unresolved": "nicht vollständig gelöst"},
        "browse": "Nach dokumentierter Ergebnisklasse öffnen", "collection": "Vollständige small_mac-Sammlung", "root": "PROMETHEUS-10-Portfolio", "batch_status": "Detaillierte Statusübersicht nach Charge (chinesische Ausgangstitel)",
        "repro": "Reproduzierbarkeit", "repro_text": "Jedes Projekt enthält das eingefrorene PDF, Manuskriptquellen, freigegebenen Code und Daten, die Autorenübergabe, Provenienz und SHA-256-Prüfsummen. Im Stammverzeichnis ausführen:",
        "root_title": "small_mac-Erweiterung: 48 Manuskripte nach Ergebnisklasse",
        "root_lead": "Dieses Repository enthält **{total} Manuskripte**: die ursprünglichen zehn PROMETHEUS-10-Projekte und **{count} small_mac-Physikmanuskripte**. Die ursprünglichen zehn Projekte und ihre wissenschaftlichen Grenzen sind unten dokumentiert.",
    },
    "fr": {
        "title": "Collection de physique small_mac",
        "lead": "Cette collection réunit 48 manuscrits de physique assistés par IA et conditionnés pour être vérifiables.",
        "notice": "Chaque élément small_mac a franchi les contrôles locaux documentés de science, de manuscrit et de diffusion. Une revue humaine par l’auteur reste requise ; aucune évaluation externe ni acceptation éditoriale n’est revendiquée.",
        "scope_notice": "La classification suit le registre de diffusion figé. Preuve et Réfutation concernent l’énoncé formulé et ses hypothèses ; les résultats partiels et computationnels ne signifient pas que la question initiale est entièrement résolue. Chaque PDF et note de transmission précise la portée scientifique et les limites.",
        "identity": "Les numéros d’affichage 11–58, les identifiants de lot et les identifiants internes d’origine sont conservés. Les identifiants publics `phys-smallmac` renvoient aux répertoires canoniques des projets. La correspondance figure dans",
        "title_policy": "Les titres sont conservés dans la langue de chaque manuscrit figé.",
        "number": "N°", "batch": "Lot", "project": "Identifiant public", "original": "Identifiant interne d’origine", "paper": "Manuscrit / PDF", "scope": "Question initiale", "materials": "Code / reproduction", "code": "Code", "guide": "Guide de reproduction", "category": "Catégorie", "count": "Manuscrits",
        "outcomes": ("Preuve", "Réfutation", "Résultat partiel", "Résultat computationnel"),
        "scopes": {"proved": "démontrée", "disproved": "réfutée", "unresolved": "non entièrement résolue"},
        "browse": "Parcourir par catégorie de résultat consignée", "collection": "Collection small_mac complète", "root": "Portfolio PROMETHEUS-10", "batch_status": "Tableau détaillé par lot (titres sources en chinois)",
        "repro": "Reproductibilité", "repro_text": "Chaque projet contient le PDF figé, les sources, le code et les données sélectionnés, la note de transmission, la provenance et les sommes SHA-256. Exécuter depuis la racine du dépôt :",
        "root_title": "Extension small_mac : 48 manuscrits par catégorie de résultat",
        "root_lead": "Ce dépôt contient **{total} manuscrits** : les dix projets PROMETHEUS-10 d’origine et **{count} manuscrits de physique small_mac**. Les dix projets d’origine et leurs limites scientifiques sont décrits ci-dessous.",
    },
    "ja": {
        "title": "small_mac 物理コレクション",
        "lead": "AI が支援した 48 本の物理学研究草稿を、検証可能な形で収録しています。",
        "notice": "small_mac の各項目は記録されたローカルの科学・原稿・公開ゲートを通過していますが、著者による最終確認が必要です。外部査読や掲載受理を意味しません。",
        "scope_notice": "分類は凍結済みの公開記録に基づきます。「証明」と「反証」は記載された命題と仮定に対するものです。部分結果と計算結果は元の問題の完全解決を意味しません。科学的範囲と限界は各 PDF と著者引継ぎ資料をご確認ください。",
        "identity": "表示番号 11–58、バッチ番号、元の内部プロジェクト ID を保持しています。公開 `phys-smallmac` ID は共通のプロジェクトディレクトリを指します。対応表：",
        "title_policy": "論文題名は各凍結原稿の言語のまま掲載しています。",
        "number": "番号", "batch": "バッチ", "project": "公開プロジェクト ID", "original": "元の内部 ID", "paper": "原稿 / PDF", "scope": "元の問題", "materials": "コード / 再現", "code": "コード", "guide": "再現ガイド", "category": "成果区分", "count": "原稿数",
        "outcomes": ("証明", "反証", "部分結果", "計算結果"),
        "scopes": {"proved": "証明済み", "disproved": "反証済み", "unresolved": "未完全解決"},
        "browse": "記録された成果区分別に見る", "collection": "small_mac 全コレクション", "root": "PROMETHEUS-10 ポートフォリオ", "batch_status": "バッチ別の詳細状況表（中国語の原題）",
        "repro": "再現性", "repro_text": "各プロジェクトには凍結 PDF、原稿ソース、公開ゲートが選んだコードとデータ、著者引継ぎ、来歴、SHA-256 検査値が含まれます。リポジトリのルートから実行：",
        "root_title": "small_mac 拡張：成果区分別の 48 本の原稿",
        "root_lead": "このリポジトリには **{total} 本の原稿**、すなわち元の PROMETHEUS-10 の 10 プロジェクトと **{count} 本の small_mac 物理学草稿**が含まれます。元の 10 プロジェクトと科学的範囲は以下に記載されています。",
    },
    "ru": {
        "title": "Физическая коллекция small_mac",
        "lead": "Коллекция содержит 48 исследовательских рукописей по физике, подготовленных с участием ИИ и упакованных для проверки.",
        "notice": "Каждая работа small_mac прошла зафиксированные локальные проверки научного содержания, рукописи и выпуска. Проверка автором всё ещё обязательна; внешнее рецензирование или принятие к публикации не заявляются.",
        "scope_notice": "Классификация следует зафиксированной записи выпуска. Доказательство и опровержение относятся к сформулированному утверждению при указанных предположениях; частичные и вычислительные результаты не означают полного решения исходной задачи. Точная научная область применимости и ограничения указаны в PDF и материалах для автора.",
        "identity": "Сохранены номера 11–58, идентификаторы серий запуска и исходные внутренние идентификаторы проектов. Публичные идентификаторы `phys-smallmac` ведут в канонические каталоги проектов. Таблица соответствий:",
        "title_policy": "Названия рукописей сохранены на языке каждого зафиксированного документа.",
        "number": "№", "batch": "Серия запуска", "project": "Публичный ID проекта", "original": "Исходный внутренний ID", "paper": "Рукопись / PDF", "scope": "Исходная задача", "materials": "Код / воспроизведение", "code": "Код", "guide": "Руководство", "category": "Категория", "count": "Рукописи",
        "outcomes": ("Доказательство", "Опровержение", "Частичный результат", "Вычислительный результат"),
        "scopes": {"proved": "доказана", "disproved": "опровергнута", "unresolved": "полностью не решена"},
        "browse": "Просмотр по зафиксированной категории результата", "collection": "Полная коллекция small_mac", "root": "Портфолио PROMETHEUS-10", "batch_status": "Подробная таблица по сериям запуска (исходные названия на китайском)",
        "repro": "Воспроизводимость", "repro_text": "Каждый проект содержит зафиксированный PDF, исходный текст рукописи, выбранные для выпуска код и данные, материалы для автора, сведения о происхождении и контрольные суммы SHA-256. Выполняйте из корня репозитория:",
        "root_title": "Расширение small_mac: 48 рукописей по категориям результата",
        "root_lead": "Репозиторий содержит **{total} рукописей**: десять исходных проектов PROMETHEUS-10 и **{count} рукописей по физике small_mac**. Десять исходных проектов и их научные ограничения описаны ниже.",
    },
}


def language_navigation(prefix: str = "") -> str:
    return " · ".join(f"[{label}]({prefix}{name})" for _, name, label in LANGUAGES)


def language_filename(language: str) -> str:
    return next(name for code, name, _ in LANGUAGES if code == language)


def outcome_labels(language: str) -> dict[str, str]:
    return dict(zip((kind for kind, _ in CATEGORIES), INDEX_LABELS[language]["outcomes"]))


def batch_identifier(row: dict) -> str:
    match = re.fullmatch(r"phys-smallmac(\d{5})-p\d{2}", row["id"])
    if not match:
        raise ValueError(f"invalid SmallMac public ID: {row['id']}")
    return f"small_mac / {match.group(1)}" if match.group(1) != "00000" else f"legacy / {row['original_internal_id']}"


def category_navigation(rows: list[dict], language: str, prefix: str) -> list[str]:
    labels = INDEX_LABELS[language]
    outcomes = outcome_labels(language)
    counts = Counter(row["claim_class"] for row in rows)
    name = language_filename(language)
    lines = [f"| {labels['category']} | {labels['count']} |", "|---|---:|"]
    for kind, slug in CATEGORIES:
        lines.append(f"| [{outcomes[kind]}]({prefix}{slug}/{name}) | **{counts[kind]}** |")
    return lines


def manuscript_table(rows: list[dict], language: str, project_prefix: str) -> list[str]:
    labels = INDEX_LABELS[language]
    columns = ("number", "batch", "project", "original", "paper", "scope", "materials")
    lines = ["| " + " | ".join(labels[key] for key in columns) + " |", "|---:|---|---|---|---|---|---|"]
    for row in rows:
        base = f"{project_prefix}{row['id']}/"
        title = escape_table(escape_prose(row["paper_title"]))
        code = next((value for value in row["code_files"] if Path(value).name != "build.py"), row["code_files"][0])
        guides = "<br>".join(f"[{labels['guide']}]({base}{guide})" for guide in row["reproduction_guides"])
        materials = f"[{labels['code']}]({base}{code}) ({len(row['code_files'])})<br>{guides}"
        lines.append(f"| {row['display_number']:02d} | `{batch_identifier(row)}` | [{row['id']}]({base}) | `{row['original_internal_id']}` | [{title}]({base}paper.pdf) | {labels['scopes'].get(row['original_status'], row['original_status'])} | {materials} |")
    return lines


def localized_collection(rows: list[dict], language: str) -> str:
    labels = INDEX_LABELS[language]
    outcomes = outcome_labels(language)
    counts = Counter(row["claim_class"] for row in rows)
    name = language_filename(language)
    lines = [f"# {labels['title']}", "", language_navigation(), "", f"[{labels['root']}](../../{name})", "", labels["lead"], "", labels["notice"], "", labels["scope_notice"], "", f"## {labels['browse']}", ""]
    lines += category_navigation(rows, language, "categories/")
    lines += ["", labels["title_policy"], "", f"{labels['identity']} [`id-map.json`](id-map.json).", "", f"[{labels['batch_status']}](BATCH_STATUS.zh-CN.md)."]
    for kind, slug in CATEGORIES:
        lines += ["", f"## {outcomes[kind]} ({counts[kind]})", "", f"[{outcomes[kind]}](categories/{slug}/{name})", ""]
        lines += manuscript_table([row for row in rows if row["claim_class"] == kind], language, "../../projects/")
    lines += ["", f"## {labels['repro']}", "", labels["repro_text"], "", "```bash", "python3 reproducibility/verify_small_mac.py --all", "python3 reproducibility/build_small_mac_papers.py --all", "```", "", "[`small_mac_projects.json`](../../reproducibility/small_mac_projects.json) · [SHA-256](../../reproducibility/SHA256SUMS)", ""]
    return "\n".join(lines)


def localized_category(rows: list[dict], language: str, kind: str) -> str:
    labels = INDEX_LABELS[language]
    outcomes = outcome_labels(language)
    selected = [row for row in rows if row["claim_class"] == kind]
    name = language_filename(language)
    lines = [f"# small_mac · {outcomes[kind]} ({len(selected)})", "", language_navigation(), "", f"[{labels['collection']}](../../{name}) · [{labels['root']}](../../../../{name})", "", labels["notice"], "", labels["scope_notice"], "", labels["title_policy"], "", f"{labels['identity']} [`id-map.json`](../../id-map.json).", "", f"## {labels['browse']}", ""]
    lines += category_navigation(rows, language, "../")
    lines += ["", "---", ""]
    lines += manuscript_table(selected, language, "../../../../projects/")
    lines += ["", f"[{labels['batch_status']}](../../BATCH_STATUS.zh-CN.md).", ""]
    return "\n".join(lines)


def russian_original_portfolio() -> str:
    """Translate the original ten-project portfolio without changing its scope."""
    projects = [
        ("phys-00002-p01", "Сколько шума нужно кубиту?", "Частичный результат",
         "Генераторы Линдблада описывают марковскую динамику открытых систем. Может ли один оператор скачка достичь всей границы области переноса населённостей кубита?",
         "Сертифицирована локальная оптимальность в области конечного радиуса около стационарной точки a=1/2 с одним скачком против возмущений ранга не выше двух. Исходная глобальная задача остаётся открытой.",
         "Явный интервальный сертификат превращает численно найденную стационарную точку в проверяемую локальную область исключения конкурирующих генераторов.",
         "Локальный радиус 10^-4; результат не устанавливает глобальную границу вложимости и не исключает удалённые конкурирующие решения."),
        ("phys-00002-p02", "Четыре измерения кубита: точный порог совместимости", "Доказательство",
         "Шумные квантовые измерения иногда реализуются как маргинальные измерения одного общего измерения. Где проходит порог шума?",
         "Рукопись доказывает порог 1/D для четырёх строго упорядоченных плоских несмещённых бинарных измерений кубита с общей видимостью.",
         "Совпадающие конструктивная и двойственная оценки дают аналитический порог; проверки SOCP/SDP подтверждают формулу.",
         "Результат ограничен указанной геометрией четырёх измерений и моделью шума; это не теорема для произвольных POVM или любого числа измерений."),
        ("phys-00002-p06", "Четырёхуровневый свидетель эффекта Мпембы за пределами трёхуровневых проверок", "Вычислительный результат",
         "В некоторых моделях тепловой релаксации более горячее начальное состояние релаксирует быстрее. Условия для трёх уровней могут не определять поведение более крупных систем.",
         "Четырёхуровневый свидетель при положительной температуре и детальном балансе сохраняется в независимых вычислениях с точностью 100 и 180 цифр, а проверенные трёхуровневые необходимые условия исключены.",
         "Конкретный механизм в большей размерности проверяет пределы сведения тепловой релаксации к трёхуровневой диагностике.",
         "Вычислительная работа; высокая точность не равнозначна сертификации с направленным округлением или общей классификации. Исходная задача остаётся нерешённой."),
        ("phys-00002-p15", "Критический сброс стирает когерентность с контролируемой скоростью", "Доказательство",
         "Случайный сброс меняет долговременную квантовую динамику. Критический показатель Сибуи разделяет качественно различные режимы процесса восстановления.",
         "Для alpha=1 и фиксированного конечномерного унитарного регистра рукопись доказывает сходимость в следовой норме к спектральному пинчингу со скоростями при фиксированных спектральных зазорах.",
         "Асимптотическая теорема для критического случая связывает коэффициенты процесса восстановления с затуханием внедиагональной квантовой когерентности.",
         "Фиксированы размерность и спектральные зазоры; не доказаны равномерные утверждения при закрывающемся зазоре, в термодинамическом пределе или для произвольных правил сброса."),
        ("phys-00003-p01", "Может ли вращающий момент уменьшить шум гауссовой частицы?", "Доказательство",
         "Неравновесное воздействие меняет флуктуации токов. Сравнение с той же равновесной ловушкой проверяет возможность подавления шума.",
         "Для устойчивой слабозатухающей модели Орнштейна–Уленбека с вращающим моментом и нулевым магнитным полем шум позиционных токов степени один и три ограничен снизу соответствующим равновесным значением.",
         "Точные полиномиальные вычисления и независимые расчёты по формулам Вика и уравнению Пуассона выделяют неотрицательный избыток шума и случаи равенства для градиентных граничных токов.",
         "Ограничены динамика и класс полиномиальных токов; нелинейные силы, магнитные поля и более высокие степени находятся вне теоремы."),
        ("phys-00004-p01", "Две шумные квантовые батареи: помогает ли совместный вход?", "Доказательство",
         "Корреляции могут влиять на извлечение работы из квантовых батарей. Обобщённое амплитудное затухание моделирует канал релаксации при конечной температуре.",
         "Рукопись доказывает W2(e)=2W1(e) для указанной задачи с двумя использованиями и ограничением энергии, включая комплексные входные состояния и извлечение работы глобальным унитарным преобразованием.",
         "Сведение фаз и точный сертификат полиномиальной положительности завершают оптимизацию двух использований в этой модели.",
         "Нет утверждения для произвольных семейств каналов, любого числа использований или иных операционных определений работы."),
        ("phys-00004-p02", "Точный контрпример на кутрите к гипотезе о неопределённости", "Опровержение",
         "Энтропийная неопределённость описывает ограничения совместной предсказуемости несовместимых измерений. Сводные спектральные характеристики могут терять существенную структуру.",
         "Точная рациональная трёхмерная унитарная конструкция опровергает проверяемую гипотезу extended-MUB.",
         "Краткий сертификат в рациональной арифметике показывает, почему второе сингулярное число само по себе не обеспечивает предложенное универсальное утверждение.",
         "Это контрпример к конкретной гипотезе, а не к принципу неопределённости. Новое точное заменяющее неравенство ещё предстоит найти."),
        ("phys-00005-p01", "Граф с 16 вершинами опровергает минимальность пути", "Опровержение",
         "Среднее смешивание квантового блуждания отражает устойчивую структуру возврата. Экстремальные утверждения о графах помогают исследовать перенос и локализацию.",
         "Связный простой невзвешенный граф с 16 вершинами и 62 рёбрами имеет показатель ленивости 1673/1192 против 23/16 у пути; разность равна -81/2384.",
         "Два точных представления сертифицируют конечный контрпример к указанному утверждению о минимальности пути для лапласианного квантового блуждания.",
         "Не классифицированы минимизаторы для всех размеров графов и не решены задачи для иных гамильтонианов и соглашений о нормировке."),
        ("phys-00006-p01", "Кубитная память нарушает предложенную универсальную оценку сжатия", "Опровержение",
         "Оценки сжатия канала количественно описывают потерю различимости. Квантовая память может нарушить интуицию, основанную на входах без вспомогательной системы.",
         "Точный пример амплитудного затухания с допустимыми запутанными входами и одинаковыми маргинальными состояниями опровергает предложенную универсальную замену alpha-Doeblin для hockey-stick оценки.",
         "Сертификат выявляет конкретный механизм нарушения, чувствительный к памяти и удовлетворяющий исходным ограничениям на входы.",
         "Опровергнута конкретная усиленная оценка; это не опровергает все неравенства Дёблина и не даёт оптимальной замены."),
        ("phys-00007-p01", "Когда граничность канала точно перемножается?", "Частичный результат · архивный черновик",
         "Граничность характеризует близость к границе выпуклого множества каналов. Тензорные произведения могут выявлять структуру, незаметную для одной копии.",
         "Точная мультипликативность доказана внутри явного двухпараметрического семейства полноранговых неунитальных матриц Чои кубитных каналов при &#124;s&#124;, &#124;t&#124; ≤ 1/5.",
         "Символьные проверки Чои, Штурма и LDL подтверждают явное семейство, в котором оптимум тензорного произведения поддаётся точному анализу.",
         "Общая задача остаётся открытой. Историческая проверка пакета для подачи выявила несоответствие привязки доказательств к рукописи; PDF включён как архивный черновик, а не как выпуск, прошедший эту проверку."),
    ]
    lines = ["# PROMETHEUS-10", "", "**Физика с участием ИИ, доступная для проверки**", "", language_navigation(), "",
             "Десять исходных рукописей по физике с участием ИИ и код для проверки их утверждений. PROMETHEUS-10 объединяет автоматизированный поиск доказательств, построение контрпримеров и контролируемые вычисления в проверяемую исследовательскую коллекцию. Число 10 обозначает рукописи и не означает десять полностью решённых универсальных задач.", "",
             "Исторические записи внутренней проверки: **4 доказательства, 3 опровержения, 2 работы с частичными результатами и 1 вычислительная работа**. PDF, содержащих только гипотезы, нет. Это исследовательские черновики, ожидающие проверки автором; внешнее рецензирование или принятие к публикации не заявляются.", "",
             "Под руководством человека ИИ участвовал в выводах, программировании, численном поиске, проверках и подготовке рукописей. Независимые контексты проверки ИИ не являются внешним рецензированием. Предлагаемый вклад описывает заявление рукописи; эта упаковка не устанавливает приоритет посредством нового исчерпывающего обзора литературы.", "",
             "| Проект | Категория результата | Подробнее |", "|---|---|---|"]
    for number, (ident, title, kind, *_rest) in enumerate(projects, 1):
        lines.append(f"| [{ident}](projects/{ident}/paper.pdf) · {title} | {kind} | ↓ {number:02d} |")
    for number, (ident, title, kind, background, result, contribution, limits) in enumerate(projects, 1):
        lines += ["", "<details>", f"<summary><strong>{number:02d} · {title}</strong> — {kind} · Нажмите, чтобы раскрыть описание</summary>", "", "| | |", "|---|---|",
                  f"| **Контекст** | {background} |", f"| **Результат и охват исходной задачи** | {result} |", f"| **Предлагаемый вклад** | {contribution} |", f"| **Ограничения** | {limits} |",
                  f"| **PDF и исходники** | [PDF](projects/{ident}/paper.pdf) · [TeX](projects/{ident}/manuscript/main.tex) · [Bib](projects/{ident}/manuscript/references.bib) · [Код / данные](projects/{ident}) · `python reproducibility/reproduce.py --project {ident}` |", "", "</details>"]
    lines += ["", "## Воспроизведение результатов", "",
              "Для этого повторного запуска использовался Python 3.12. Пример контрпримера на кутрите ниже требует только стандартной библиотеки Python. Для всех проектов установите закреплённые научные зависимости в виртуальную среду. Программа сначала копирует каждый проект в новый выходной каталог, затем выполняет проверки, сохраняя архивные свидетельства. Аккаунт ИИ, API-ключ или сеанс браузера не требуются.", "", "```bash",
              "# Точный контрпример: только стандартная библиотека", "python3 projects/phys-00004-p02/reproducibility/verify_counterexample.py", "", "# Полная научная среда и повторный запуск", "python3 -m venv .venv", "source .venv/bin/activate", "python -m pip install -r requirements.txt", "python reproducibility/reproduce.py --all", "```", "",
              "Результаты повторного запуска, команды и ограничения записаны в [reproducibility/VALIDATION.md](reproducibility/VALIDATION.md). Нулевой код выхода сам по себе не является научным сертификатом. Точная арифметика, интервальные сертификаты, высокоточные свидетели и стресс-тесты с плавающей точкой обладают разной доказательной силой; вид проверки указан в отдельных работах.", "",
              "Исходники рукописей и рисунки включены в каждый проект. Инструкции повторного запуска и сборки PDF находятся в [reproducibility/README.md](reproducibility/README.md). Байты архивных PDF сохранены; компиляция в другом дистрибутиве TeX может дать другой PDF.", "",
              "## Одно историческое исключение", "",
              "У `phys-00007-p01` есть PDF и воспроизводимые символьные вычисления, но историческая проверка пакета для подачи выявила несоответствие привязки свидетельств к рукописи. Работа явно помечена как архивный черновик. Упаковка и успешный повторный запуск кода не устраняют эту историческую ошибку и не являются новой научной проверкой.", "",
              "## Авторство и повторное использование", "",
              "В рукописях указан **Xiaojian Zeng**; сведения об авторе и окончательное утверждение текста требуют подтверждения автора. Раскрывается участие ИИ и вычислительных средств. Эта упаковка не предоставляет дополнительной лицензии с открытым кодом или Creative Commons; права остаются у соответствующих правообладателей. Сторонние исследования цитируются, но не распространяются вместе с пакетом. Зависимости сохраняют свои лицензии.", ""]
    return "\n".join(lines)


def strip_small_mac_block(text: str) -> str:
    """Remove only the generated extension, preserving the original portfolio."""
    begin = "<!-- SMALL_MAC_COLLECTION -->"
    end = "<!-- END_SMALL_MAC_COLLECTION -->"
    if begin not in text:
        return text
    before, remainder = text.split(begin, 1)
    if end in remainder:
        after = remainder.split(end, 1)[1]
    else:
        # The first generator placed an unbounded prose block before the
        # original portfolio table. Do not discard the original ten sections.
        table = remainder.find("\n|")
        after = remainder[table:] if table >= 0 else ""
    return before.rstrip() + "\n\n" + after.lstrip()


def root_insert(path: Path, language: str, rows: list[dict]) -> None:
    labels = INDEX_LABELS[language]
    name = language_filename(language)
    text = path.read_text(encoding="utf-8") if path.exists() else russian_original_portfolio()
    text = strip_small_mac_block(text)
    text = re.sub(r"(?m)^\[English\]\(README\.md\)[^\n]*$", language_navigation(), text)
    lines = ["<!-- SMALL_MAC_COLLECTION -->", "", f"## {labels['root_title']}", "", labels["root_lead"].format(total=len(rows) + 10, count=len(rows)), "", labels["notice"], "", labels["scope_notice"], "", f"[{labels['collection']}](collections/small_mac/{name})", ""]
    lines += category_navigation(rows, language, "collections/small_mac/categories/")
    lines += ["", f"{labels['identity']} [`id-map.json`](collections/small_mac/id-map.json).", "", "<!-- END_SMALL_MAC_COLLECTION -->"]
    block = "\n".join(lines)
    first_table = text.find("\n|")
    if first_table < 0:
        updated = text.rstrip() + "\n\n" + block + "\n"
    else:
        updated = text[:first_table].rstrip() + "\n\n" + block + "\n\n" + text[first_table + 1:].lstrip()
    path.write_text(updated, encoding="utf-8")


def render_indexes(output: Path, rows: list[dict] | None = None) -> list[dict]:
    """Refresh navigation only; never rewrite frozen artifacts or checksums."""
    if rows is None:
        rows = json.loads((output / "reproducibility" / "small_mac_projects.json").read_text(encoding="utf-8"))
    unknown = set(row["claim_class"] for row in rows) - {kind for kind, _ in CATEGORIES}
    if unknown:
        raise ValueError(f"unsupported SmallMac result classes: {sorted(unknown)}")
    collection = output / "collections" / "small_mac"
    collection.mkdir(parents=True, exist_ok=True)
    for language, name, _ in LANGUAGES:
        (collection / name).write_text(localized_collection(rows, language), encoding="utf-8")
        root_insert(output / name, language, rows)
        for kind, slug in CATEGORIES:
            category = collection / "categories" / slug
            category.mkdir(parents=True, exist_ok=True)
            (category / name).write_text(localized_category(rows, language, kind), encoding="utf-8")
    return rows


VERIFY_SCRIPT = r'''#!/usr/bin/env python3
"""Verify packaged SmallMac artifacts without changing them."""
from pathlib import Path
import argparse, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/'reproducibility/small_mac_projects.json').read_text())
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def check(row):
 project=ROOT/'projects'/row['id']; errors=[]
 manifest=project/'ARTIFACTS.sha256'
 for line in manifest.read_text().splitlines():
  expected,relative=line.split('  ',1); path=project/relative
  if not path.is_file():errors.append(f'missing {relative}')
  elif sha(path)!=expected:errors.append(f'hash mismatch {relative}')
 if sha(project/'paper.pdf')!=row['pdf_sha256']:errors.append('paper hash mismatch')
 return errors
def main():
 p=argparse.ArgumentParser();p.add_argument('--project',choices=[x['id'] for x in MANIFEST]);p.add_argument('--all',action='store_true');p.add_argument('--list',action='store_true');a=p.parse_args()
 if a.list: print(json.dumps(MANIFEST,ensure_ascii=False,indent=2));return 0
 if not a.project and not a.all:p.error('choose --project or --all')
 failed=False
 for row in MANIFEST if a.all else [next(x for x in MANIFEST if x['id']==a.project)]:
  errors=check(row); print(json.dumps({'project':row['id'],'ok':not errors,'errors':errors},ensure_ascii=False));failed|=bool(errors)
 return int(failed)
if __name__=='__main__':raise SystemExit(main())
'''


VERIFY_PACKAGE_SCRIPT = r'''#!/usr/bin/env python3
"""Cross-platform verification of the full packaged tree."""
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SUMS=ROOT/'reproducibility/SHA256SUMS'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def ignored(path):
 parts=set(path.parts)
 return bool(parts & {'.git','.venv','__pycache__','reproduction-runs'}) or path.suffix=='.pyc'
def main():
 expected={}
 for line in SUMS.read_text().splitlines():
  digest,relative=line.split('  ',1);expected[relative]=digest
 errors=[]
 for relative,digest in expected.items():
  path=ROOT/relative
  if not path.is_file():errors.append(f'missing {relative}')
  elif sha(path)!=digest:errors.append(f'hash mismatch {relative}')
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=SUMS and not ignored(p.relative_to(ROOT))}
 extras=sorted(actual-set(expected))
 errors.extend(f'unlisted file {item}' for item in extras)
 for error in errors:print(error,file=sys.stderr)
 print(f'verified={len(expected)-sum(1 for e in errors if not e.startswith("unlisted"))} listed={len(expected)} extras={len(extras)} ok={not errors}')
 return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
'''


BUILD_SCRIPT = r'''#!/usr/bin/env python3
"""Rebuild SmallMac manuscripts in disposable copies; archived PDFs stay unchanged."""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
ROWS=json.loads((ROOT/'reproducibility/small_mac_projects.json').read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument('--project',choices=[x['id'] for x in ROWS]);p.add_argument('--all',action='store_true');p.add_argument('--output-dir',type=Path,default=ROOT/'reproduction-runs');p.add_argument('--timeout',type=int,default=240);a=p.parse_args()
 if not a.project and not a.all:p.error('choose --project or --all')
 if not shutil.which('latexmk'):p.error('latexmk and a TeX distribution are required; no installation is attempted')
 chosen=ROWS if a.all else [next(x for x in ROWS if x['id']==a.project)]
 out=a.output_dir.resolve()/('small-mac-tex-'+time.strftime('%Y%m%d-%H%M%S'));out.mkdir(parents=True,exist_ok=False);results=[]
 for row in chosen:
  ident=row['id'];work=out/ident;shutil.copytree(ROOT/'projects'/ident,work)
  attempts=[(work/'manuscript',['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-outdir=rebuild','main.tex']),(work,['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','-outdir=rebuild','manuscript/main.tex'])]
  code=1;used=None;pdf=None;citations_clean=False
  for n,(cwd,command) in enumerate(attempts,1):
   log=work/f'compile-attempt-{n}.log';used={'cwd':str(cwd.relative_to(work)) or '.', 'command':command,'log':log.name}
   with log.open('w') as f:
    try:code=subprocess.run(command,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=a.timeout).returncode
    except subprocess.TimeoutExpired:code=124
   candidate=cwd/'rebuild/main.pdf'
   final_log=cwd/'rebuild/main.log'
   log_text=final_log.read_text(errors='replace') if final_log.is_file() else ''
   unresolved=(not final_log.is_file() or 'undefined citations' in log_text.lower() or 'there were undefined references' in log_text.lower() or ('citation' in log_text.lower() and 'undefined' in log_text.lower()) or ('reference' in log_text.lower() and 'undefined' in log_text.lower()) or 'please (re)run biber' in log_text.lower())
   if code==0 and candidate.is_file() and not unresolved:pdf=candidate;citations_clean=True;break
   if code==0 and candidate.is_file() and unresolved:code=65
  result={'project':ident,'exit_code':code,'pdf_exists':bool(pdf),'citations_clean':citations_clean,'attempt':used};results.append(result);print(json.dumps(result),flush=True);(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 return int(any(x['exit_code'] or not x['pdf_exists'] or not x['citations_clean'] for x in results))
if __name__=='__main__':raise SystemExit(main())
'''


def build(reference: Path, research_root: Path, output: Path) -> list[dict]:
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(reference, output)
    (output / "projects" / ".gitignore").write_text(
        "# Track curated SmallMac release evidence and frozen bibliography outputs.\n"
        "!phys-smallmac*/**/*.log\n"
        "!phys-smallmac*/**/*.bbl\n",
        encoding="utf-8",
    )
    queue = json.loads((research_root / "queue.json").read_text(encoding="utf-8"))
    selected = []
    for original, queue_row in queue["projects"].items():
        if queue_row.get("phase") != "done":
            continue
        project = research_root / "projects" / original
        state = json.loads((project / "state.json").read_text(encoding="utf-8"))
        claim = json.loads((project / "claim.json").read_text(encoding="utf-8"))
        bundle = project / "release" / "submission.zip"
        bundle_record = json.loads((project / "release" / "bundle.json").read_text(encoding="utf-8"))
        if file_digest(bundle) != bundle_record["zip_sha256"]:
            raise ValueError(f"stale source bundle: {original}")
        selected.append((state.get("created_at", ""), original, project, state, claim, bundle, bundle_record))
    selected.sort(key=lambda value: (value[0], value[1]))
    rows: list[dict] = []
    portability: list[dict] = []
    for offset, (_, original, source_project, state, claim, bundle, bundle_record) in enumerate(selected, 11):
        ident = public_id(original)
        destination = output / "projects" / ident
        if destination.exists():
            raise ValueError(f"public ID collision: {ident}")
        destination.mkdir(parents=True)
        with zipfile.ZipFile(bundle) as archive:
            names = archive.namelist()
            if "BUNDLE-CONTENTS.json" not in names or "main.pdf" not in names:
                raise ValueError(f"incomplete source bundle: {original}")
            contents = json.loads(archive.read("BUNDLE-CONTENTS.json"))
            expected = contents["files"]
            for name in names:
                posix = PurePosixPath(name)
                if posix.is_absolute() or ".." in posix.parts or name.endswith("/"):
                    raise ValueError(f"unsafe source bundle member: {original}:{name}")
                raw = archive.read(name)
                if name == "BUNDLE-CONTENTS.json":
                    target_relative = "SOURCE-BUNDLE-CONTENTS.json"
                else:
                    if name not in expected or digest(raw) != expected[name]:
                        raise ValueError(f"source bundle hash mismatch: {original}:{name}")
                    target_relative = "paper.pdf" if name == "main.pdf" else name
                modified = raw
                notes: list[str] = []
                if name != "main.pdf" and Path(name).suffix.lower() in {".md", ".txt", ".json", ".jsonl", ".log", ".py", ".tex", ".bib", ".csv"}:
                    modified, notes = text_portability(raw, original, research_root)
                target = destination / target_relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(modified)
                if modified != raw:
                    portability.append({"project": ident, "file": target_relative, "source_sha256": digest(raw), "packaged_sha256": digest(modified), "changes": notes})
        tex = (destination / "manuscript" / "main.tex").read_bytes()
        title = plain_title(tex) or state.get("title") or original
        status = state.get("original_status", claim.get("original_status", "unresolved"))
        kind = state.get("candidate_kind", claim.get("kind", "result-note"))
        paper_hash = file_digest(destination / "paper.pdf")
        release_manifest_path = source_project / "release" / "manifest.json"
        release_manifest = json.loads(release_manifest_path.read_text(encoding="utf-8"))
        if release_manifest.get("status") != "draft_ready_author_review_required":
            raise ValueError(f"inactive release manifest: {original}")
        if release_manifest.get("pdf_digest") != paper_hash:
            raise ValueError(f"release PDF digest mismatch: {original}")
        release_manifest_hash = file_digest(release_manifest_path)
        guides, code_files, requirement_files = project_materials(destination)
        if not guides or not code_files:
            raise ValueError(f"missing replay guide or source code: {original}")
        row = {
            "id": ident,
            "series": "small_mac",
            "display_number": offset,
            "original_internal_id": original,
            "paper_title": title,
            "original_topic_title": state.get("title", ""),
            "candidate_kind": kind,
            "claim_class": claim_class(kind, status),
            "original_status": status,
            "claim_statement": claim.get("statement", ""),
            "release_status": "draft_ready_author_review_required",
            "pdf_sha256": paper_hash,
            "source_bundle_sha256": bundle_record["zip_sha256"],
            "source_bundle_manifest_sha256": bundle_record["core_manifest_sha256"],
            "source_release_manifest_sha256": release_manifest_hash,
            "reproduction_guides": guides,
            "code_files": code_files,
            "dependency_files": requirement_files,
        }
        rows.append(row)
        guide_lines = [f"- [{path}]({path})" for path in guides]
        dependency_lines = [f"- `{path}`" for path in requirement_files] or ["- See the linked replay guide for standard-library or system-tool requirements."]
        original_topic = escape_prose(state.get("title", "See the immutable project source and manuscript."))
        frozen_claim = escape_prose(claim.get("statement", "The exact scope is stated in the paper and author handoff."))
        readme = [
            f"# {ident}", "", f"**{title}**", "",
            f"- Series: `small_mac`", f"- Display number in PROMETHEUS-10: `{offset:02d}`", f"- Original internal ID: `{original}`",
            f"- Claim class: **{row['claim_class']}**", f"- Original problem status: **{scope_label(status)}**", f"- Release status: `draft_ready_author_review_required`", "",
            "## Original topic (Chinese source text)", "", original_topic, "",
            "## Frozen scientific claim", "", frozen_claim, "",
            "## Result classification", "", f"This release is classified as `{kind}`; the original problem status is `{scope_label(status)}`. The paper and author handoff state the scoped contribution, assumptions, physical use and remaining limitations.", "",
            "## Files", "", "- [Frozen release PDF](paper.pdf)", "- [Manuscript source](manuscript/main.tex)", "- [Author handoff](AUTHOR_HANDOFF.md)", "- [Release status and verification boundary](RELEASE-STATUS.md)", "- `SOURCE-BUNDLE-CONTENTS.json` records the frozen release-selected inputs before portability substitutions.", "- `PACKAGE-PROVENANCE.json` binds this public ID to the original internal project and release bundle.", "- `ARTIFACTS.sha256` verifies every packaged artifact in this directory.", "",
            "## Reproduction", "", "Release-selected replay guide(s):", "", *guide_lines, "", f"The package includes {len(code_files)} source-code file(s). Dependency declaration(s):", "", *dependency_lines, "", "No AI account or browser session is required for replay. The guide states the scientific command, scope and numerical or exact-certification boundary.", "",
            "This is an AI-assisted research draft awaiting human author review. A local release gate is an internal verification record, not external peer review or journal acceptance.", "",
        ]
        (destination / "README.md").write_text("\n".join(readme), encoding="utf-8")
        release_status = [
            "# Release status", "",
            f"- Local release state: `draft_ready_author_review_required`",
            f"- Candidate kind: `{kind}`",
            f"- Original problem status: `{scope_label(status)}`",
            f"- Frozen PDF SHA-256: `{paper_hash}`",
            f"- Source release manifest SHA-256: `{release_manifest_hash}`",
            f"- Source submission bundle SHA-256: `{bundle_record['zip_sha256']}`", "",
            "The source release manifest and curated submission bundle were validated again while this GitHub package was assembled. The PDF bytes were copied unchanged. Text-only portability substitutions, if any, are enumerated in `../../reproducibility/small_mac-portability-changes.json`.", "",
            "`AUTHOR_HANDOFF.md` was written before the final release pass and may describe release checks as pending. This status record reflects the later frozen release manifest. Author review is still required; no external peer review, submission or journal acceptance is claimed.", "",
        ]
        (destination / "RELEASE-STATUS.md").write_text("\n".join(release_status), encoding="utf-8")
        provenance = {
            "schema_version": 1,
            "series": "small_mac",
            "public_id": ident,
            "original_internal_id": original,
            "source_bundle_sha256": bundle_record["zip_sha256"],
            "source_bundle_manifest_sha256": bundle_record["core_manifest_sha256"],
            "source_release_manifest_sha256": release_manifest_hash,
            "source_main_pdf_sha256": bundle_record["files"]["main.pdf"],
            "packaged_paper_pdf_sha256": paper_hash,
            "pdf_bytes_preserved": paper_hash == bundle_record["files"]["main.pdf"],
            "portability_changes_record": "../../reproducibility/small_mac-portability-changes.json",
        }
        (destination / "PACKAGE-PROVENANCE.json").write_text(canonical(provenance), encoding="utf-8")
        artifact_rows = []
        for path in sorted(destination.rglob("*")):
            if path.is_file() and path.name != "ARTIFACTS.sha256":
                artifact_rows.append(f"{file_digest(path)}  {path.relative_to(destination).as_posix()}")
        (destination / "ARTIFACTS.sha256").write_text("\n".join(artifact_rows) + "\n", encoding="utf-8")
    collection = output / "collections" / "small_mac"
    collection.mkdir(parents=True, exist_ok=True)
    (collection / "id-map.json").write_text(canonical([{k: row[k] for k in ("id", "display_number", "original_internal_id", "paper_title")} for row in rows]), encoding="utf-8")
    batch_status = [
        "# SmallMac 批次成果统计", "",
        "本表按冻结的发布状态汇总。‘继续解决的信心’不编造百分比：已经证明或反证的冻结命题不再需要续解；未完全解决的项目只说明现有可复现成果能否作为后续基线。详细边界以论文和各项目 `AUTHOR_HANDOFF.md` 为准。", "",
        "| 当前批次 + PDF title | 原始课题 | 解决程度 | 继续解决的信心 | 没能解决的原因 |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        match = re.match(r"phys-smallmac(\d{5})-p\d{2}$", row["id"])
        batch = (f"small_mac 第{match.group(1)}批" if match and match.group(1) != "00000" else "small_mac legacy")
        paper = f"{batch} · [{escape_table(row['paper_title'])}](../../projects/{row['id']}/paper.pdf)"
        topic = escape_table(row["original_topic_title"])
        if row["original_status"] == "proved":
            degree, confidence, reason = "在冻结量词下已证明", "当前命题无需续解", "—"
        elif row["original_status"] == "disproved":
            degree, confidence, reason = "已给出满足原前提的反证", "当前命题无需续解", "—"
        else:
            degree = "已有可发布局部成果；原题未完全解决"
            confidence = "不作数值化承诺；现有代码与证据可作续研基线"
            reason = f"当前出口为 `{row['candidate_kind']}`；未闭合部分见项目交接文件"
        batch_status.append(f"| {paper} | {topic} | {degree} | {confidence} | {reason} |")
    batch_status += ["", "状态数据同时见 [`../../reproducibility/small_mac_projects.json`](../../reproducibility/small_mac_projects.json)。", ""]
    (collection / "BATCH_STATUS.zh-CN.md").write_text("\n".join(batch_status), encoding="utf-8")
    repro = output / "reproducibility"
    (repro / "small_mac_projects.json").write_text(canonical(rows), encoding="utf-8")
    (repro / "small_mac-portability-changes.json").write_text(canonical(portability), encoding="utf-8")
    (repro / "verify_small_mac.py").write_text(VERIFY_SCRIPT, encoding="utf-8")
    (repro / "verify_package.py").write_text(VERIFY_PACKAGE_SCRIPT, encoding="utf-8")
    (repro / "build_small_mac_papers.py").write_text(BUILD_SCRIPT, encoding="utf-8")
    shutil.copy2(Path(__file__).resolve(), repro / "assemble_small_mac_package.py")
    (repro / "verify_small_mac.py").chmod(0o755)
    (repro / "verify_package.py").chmod(0o755)
    (repro / "build_small_mac_papers.py").chmod(0o755)
    upstream = {
        "repository": "https://github.com/ArtificialZeng/PROMETHEUS-10",
        "base_commit": UPSTREAM_COMMIT,
        "downloaded_archive_sha256": UPSTREAM_ARCHIVE_SHA256,
        "small_mac_project_count": len(rows),
        "small_mac_public_ids": [row["id"] for row in rows],
    }
    (output / "UPSTREAM-BASE.json").write_text(canonical(upstream), encoding="utf-8")
    catalog = [
        "# SmallMac reproducibility index", "",
        "Each row points to the release-selected scientific replay guide. Run commands from the project directory unless that guide says otherwise. The global verifier checks frozen bytes; the global builder recompiles manuscripts in disposable copies. Scientific replay requirements vary by project and remain project-local.", "",
        "| No. | Project | Replay guide(s) | Code files |", "|---:|---|---|---:|",
    ]
    for row in rows:
        links = "<br>".join(f"[{path}](../projects/{row['id']}/{path})" for path in row["reproduction_guides"])
        catalog.append(f"| {row['display_number']:02d} | [{row['id']}](../projects/{row['id']}/) | {links} | {len(row['code_files'])} |")
    catalog += ["", "## Collection commands", "", "```bash", "python3 reproducibility/verify_package.py", "python3 reproducibility/verify_small_mac.py --all", "python3 reproducibility/build_small_mac_papers.py --all", "```", "", "The first command verifies the full-tree SHA-256 manifest, and the second verifies every SmallMac project record. The manuscript builder needs `latexmk` and creates disposable build directories under the ignored `reproduction-runs/` path. None of these commands submits, uploads or modifies a frozen PDF.", ""]
    (repro / "SMALL_MAC.md").write_text("\n".join(catalog), encoding="utf-8")
    merge_guide = f"""# Merging the SmallMac collection

This tree is based on [`ArtificialZeng/PROMETHEUS-10`](https://github.com/ArtificialZeng/PROMETHEUS-10) commit `{UPSTREAM_COMMIT}`. It preserves the original ten project files and the upstream root `.gitignore` byte-for-byte. The five existing root README files and `reproducibility/SHA256SUMS` are updated, a Russian root README is added, and 48 release-gated SmallMac projects are included. Six-language collection and category indexes group the additions into 21 proofs, 7 disproofs, 19 partial results and 1 computational result while preserving display numbers, batch identifiers and original project IDs. The new `projects/.gitignore` allows curated SmallMac evidence logs and frozen bibliography outputs to be tracked.

## Merge

Copy the contents of this tree over a checkout of that exact upstream commit, review the diff, then run:

```bash
python3 reproducibility/verify_small_mac.py --all
python3 reproducibility/build_small_mac_papers.py --all
python3 reproducibility/verify_package.py
```

Project IDs, original internal IDs and frozen PDF hashes are in `reproducibility/small_mac_projects.json`; the concise mapping is in `collections/small_mac/id-map.json`. Assembly provenance is in `UPSTREAM-BASE.json` and `reproducibility/assemble_small_mac_package.py`.

The package does not contain browser state, model credentials, downloaded primary-literature full texts or worker logs. It does not grant a new license or authorize external submission. Every new manuscript remains `draft_ready_author_review_required`.
"""
    (output / "SMALL_MAC_MERGE.md").write_text(merge_guide, encoding="utf-8")
    render_indexes(output, rows)
    checksum = output / "reproducibility" / "SHA256SUMS"
    lines = []
    for path in sorted(output.rglob("*")):
        if path.is_file() and path != checksum:
            lines.append(f"{file_digest(path)}  {path.relative_to(output).as_posix()}")
    checksum.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--research-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--indexes-only", action="store_true", help="refresh six-language README/category indexes from the packaged manifest; leave frozen artifacts and checksums unchanged")
    args = parser.parse_args()
    if args.indexes_only:
        rows = render_indexes(args.output.resolve())
    else:
        if args.reference is None or args.research_root is None:
            parser.error("--reference and --research-root are required for a full build")
        rows = build(args.reference.resolve(), args.research_root.resolve(), args.output.resolve())
    print(canonical({"ok": True, "output": str(args.output.resolve()), "small_mac_projects": len(rows), "classes": Counter(row["claim_class"] for row in rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
