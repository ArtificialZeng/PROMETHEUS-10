"""Exact exported-partition bookkeeping; panel-range validity is a separate check.

No discovery solver or stored observable totals are imported. The exact
dyadic partition and exported panel integral endpoints are summed as Python
fractions; independent directed tails enclose the rest of the physical band.
"""
import datetime
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / 'evidence/research/r3-interval-refine.json'
OUT = ROOT / 'reproducibility/run-output/certificate-check.json'
OBS = ['Delta', 'J', 'sigma_over_kB', 'chi_minus24']


def exact_endpoint(encoded):
    sign, mantissa, exponent, _ = encoded
    return (-1 if sign else 1) * Fraction(mantissa) * Fraction(2) ** exponent


def main():
    data = json.loads(CERT.read_text())
    panels = data['panels']
    assert data['status'] == 'positive_residual_enclosed_proposer_only'
    assert len(panels) == 26275
    totals = [[Fraction(0), Fraction(0)] for _ in OBS]
    last, width, fallbacks = Fraction(-8192), Fraction(0), 0
    for panel in panels:
        lo, hi = map(Fraction, panel['q_interval'])
        assert lo == last and hi > lo
        assert Fraction(float(hi) - float(lo)) == hi - lo
        width += hi - lo
        last = hi
        fallbacks += not panel['transmission_denominator_validated']
        assert len(panel['integrated_ranges']) == 4
        for total, bounds in zip(totals, panel['integrated_ranges']):
            lower, upper = map(Fraction, bounds)
            assert lower <= upper
            total[0] += lower
            total[1] += upper
    assert last == 16384 and width == 24576 and fallbacks == 727
    mp.iv.dps = 100
    holes = 3 * mp.iv.exp(-mp.iv.mpf(8192) / 100 + 24)
    particles = 3 * mp.iv.exp(1 - mp.iv.mpf(16384) / 100)
    jtail = 2 * (holes + particles)
    etail = 28 * jtail
    ctail = 2 * mp.iv.exp(24) * (holes + particles)
    dtail = 24 * jtail + 4 * etail + ctail
    tails = [exact_endpoint(v._mpi_[1]) for v in [dtail, jtail, etail, ctail]]
    exact, display = {}, {}
    for name, endpoints, tail in zip(OBS, totals, tails):
        lower, upper = endpoints[0] - tail, endpoints[1] + tail
        exact[name] = [str(lower), str(upper)]
        display[name] = [math.nextafter(float(lower), -math.inf),
                         math.nextafter(float(upper), math.inf)]
    delta_lo = totals[0][0] - tails[0]
    delta_hi = totals[0][1] + tails[0]
    assert delta_lo > Fraction('0.019447')
    assert delta_hi < Fraction('0.024248')
    assert delta_hi - delta_lo < Fraction('0.005')
    assert totals[1][0] - tails[1] > 0 and totals[2][0] - tails[2] > 0
    result = {
        'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'pass_exported_bookkeeping_and_margin',
        'scope': 'Exact resummation and tail check, conditional on the validity of every whole-panel range. This is not a new independent scientific acceptance.',
        'certificate': str(CERT.relative_to(ROOT)),
        'certificate_sha256': hashlib.sha256(CERT.read_bytes()).hexdigest(),
        'panels': len(panels), 'fallback_panels': fallbacks,
        'exact_q_width': str(width), 'full_consecutive_coverage': True,
        'enclosures': display,
        'exact_endpoint_fractions': exact,
        'tails_upper': [math.nextafter(float(v), math.inf) for v in tails],
        'strict_margin_above_0_019': delta_lo > Fraction('0.019'),
        'environment': {'mpmath': mp.__version__},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'panels', 'fallback_panels', 'enclosures', 'strict_margin_above_0_019']}))


if __name__ == '__main__':
    main()
