#!/usr/bin/env python3
"""Build every printable part of the EMEO hex bell.

    python build.py            # all parts -> build/  (+ report.json)
    python build.py --viewer   # also build/viewer.html (interactive 3D preview)
    python build.py --fit      # also run the component clearance check (components/*.yaml)
    python build.py --only A_collar_bow F_hole_gauge

Run from the cad/ folder. Takes ~1-2 min for a full build.
"""
import argparse, json, shutil, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from esax import bell                      # noqa: E402
from esax.export import export_part        # noqa: E402

BUILD = HERE / 'build'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--viewer', action='store_true', help='write build/viewer.html')
    ap.add_argument('--fit', action='store_true', help='run the component fit check')
    ap.add_argument('--only', nargs='*', help='export only these parts')
    a = ap.parse_args()

    t0 = time.time()
    parts = bell.build()
    report = {}
    for name, M in parts.items():
        if a.only and name not in a.only:
            continue
        report[name] = export_part(M, BUILD, name)
        print(f"{name:<24} {report[name]['volume_cm3']:>7} cm3  {report[name]['extents_mm']}  {report[name]['status']}")
    # Nerd-Sniped's removable clamp half is used unchanged
    shutil.copy(HERE / 'vendor' / 'nerd-sniped' / 'fonia-001-01.stl', BUILD / 'G_clamp_half_NerdSniped.stl')
    (BUILD / 'report.json').write_text(json.dumps(report, indent=1))
    print(f'built in {time.time()-t0:.0f} s -> {BUILD}')

    if a.fit:
        from esax.components import fit_report, export_proxies
        lines, problems = fit_report({k: parts[k] for k in ('A_collar_bow', 'B_leg_controls', 'C_bell_rim')})
        print('\n'.join(lines))
        export_proxies(BUILD)
        (BUILD / 'fit_report.txt').write_text('\n'.join(lines) + '\n')
        if problems:
            print(f'\n{problems} fit problem(s).')
    if a.viewer:
        from esax.viewer import build_viewer
        print('viewer ->', build_viewer(BUILD, BUILD / 'viewer.html'))


if __name__ == '__main__':
    main()
