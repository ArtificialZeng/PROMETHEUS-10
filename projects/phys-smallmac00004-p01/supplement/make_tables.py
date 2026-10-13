#!/usr/bin/env python3
"""Render manuscript tables from the supplied aggregate certificate records."""
from pathlib import Path
from decimal import Decimal, localcontext
import json
from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
ctx.prec = 256

def read_ball(s):
    text = s.strip('[] ')
    if '+/-' in text:
        mid, rad = text.split('+/-')
        return arb(mid.strip(), rad.strip())
    return arb(text)

def main():
    data = json.loads((ROOT/'supplement/data/adaptive-certificate.json').read_text())
    assert data['all_pass'] and data['precision_bits'] == 256
    checks = {c['name']:c for c in data['checks']}
    rows = [
        ('center_positive', r'$C_p$', r'$p\in J$', '0.0017708', r'$1.7708\times10^{-3}$'),
        ('transverse_convex', r'$q-(1-q)a^4$', r'$p\in J$', '0.0686058', r'$6.86058\times10^{-2}$'),
        ('tail_coefficient_positive', r'$A_p$', r'$p\in J$', '0.0741354', r'$7.41354\times10^{-2}$'),
        ('lower_inner', r'$d_p(R_0)-\kl$', r'$p\in J$', '0.0004559', r'$4.559\times10^{-4}$'),
        ('upper_tail', r'$\ku-T_p$', r'$p\in J$', '0.0601217', r'$6.01217\times10^{-2}$'),
        ('lower_outer', r'$E_p(R)-E_p(r_t)+(d_p(R)-\kl)R^2$', r'$p\in J,\ R\in[R_0,1]$', '0.0000022027', r'$2.2027\times10^{-6}$'),
        ('upper_compact', r'$\ku-G_p^{\prime}(z^2)$', r'$p\in J,\ z\in[0,z_0]$', '0.00000012567', r'$1.2567\times10^{-7}$'),
    ]
    lines = [r'\begin{table*}[t]',r'\caption{Strict interval margins from the separately implemented adaptive 256-bit replay. Each listed decimal is rounded downward from the minimum certified lower endpoint over the accepted boxes, not a sampled minimum. The constants are $R_0=93/100$, $r_t=7/8$, $z_0=99/100$, $\kl=3/250$, and $\ku=11/1000$.}',r'\label{tab:certificate}',r'\begin{ruledtabular}',r'\begin{tabular}{llrr}',r'Margin & Domain & Leaf boxes & Lower bound \\']
    for name, expr, domain, threshold, tex in rows:
        c=checks[name]
        assert c['status']=='pass'
        assert read_ball(c['minimum_certified_lower']) > arb(threshold)
        assert c['exact_accepted_volume']==c['exact_domain_volume']
        lines.append(f"{expr} & {domain} & {c['accepted_leaves']} & {tex} "+r'\\')
    lines += [r'\end{tabular}',r'\end{ruledtabular}',r'\end{table*}','']
    (ROOT/'manuscript/certificate-table.tex').write_text('\n'.join(lines))

    source=json.loads((ROOT/'supplement/data/source-checks.json').read_text())
    lines=[r'\begin{table}[t]',r'\caption{Scalar coding values on $q=3p$. Each displayed center $r_c$ or $B_c$ specifies the certified enclosure $[r_c-\epsilon,r_c+\epsilon]$ or $[B_c-\epsilon,B_c+\epsilon]$, with $\epsilon=5\times10^{-13}$ in the units of its column. The first row is a reproduction baseline outside $J$; only the other rows are identified with $P^{(1)}$ by Theorem~\ref{thm:main}.}',r'\label{tab:rates}',r'\begin{ruledtabular}',r'\begin{tabular}{lrr}',r'$p$ & Radius center $r_c$ & Rate center $B_c$ (bits/use) \\']
    with localcontext() as context:
        context.prec=90
        for p,c in source['baselines'].items():
            radius=Decimal(c['r']).quantize(Decimal('0.000000000001'))
            value=Decimal(c['B_bits']).quantize(Decimal('0.000000000001'))
            enclosure=read_ball(c['arb_global_enclosure']['B_enclosure'])
            error=arb(1)/(2*10**12)
            assert enclosure>arb(str(value))-error and enclosure<arb(str(value))+error
            bracket=c['arb_global_enclosure']
            numerator=int(bracket['root_decimal_numerator'])
            root_lo=arb(numerator)/10**60
            root_hi=arb(numerator+1)/10**60
            assert root_lo>arb(str(radius))-error and root_hi<arb(str(radius))+error
            lines.append(f'{p} & {radius:.12f} & {value:.12f} '+r'\\')
    lines += [r'\end{tabular}',r'\end{ruledtabular}',r'\end{table}','']
    (ROOT/'manuscript/rates-table.tex').write_text('\n'.join(lines))
    print('Both manuscript tables generated; margin directions and rate rounding checked against interval records.')

if __name__=='__main__': main()
