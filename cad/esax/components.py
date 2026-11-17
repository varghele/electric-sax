"""Proxy solids for bought parts, built from components/catalog.yaml, plus a clearance check.

Proxies are deliberately simple (boxes, cylinders, flange + body). They answer "does it fit and
does it collide", not "does it look right". Their accuracy is only as good as the catalog's
confidence levels – `fit_report` prints those next to every result.
"""
from pathlib import Path
import numpy as np, yaml, trimesh, manifold3d as m3d
from .geom import box, cyl, placed, to_man, idx_at_y_leg, profile, face_point, PTS, DIST

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / 'components' / 'catalog.yaml'
LAYOUT = ROOT / 'components' / 'layout.yaml'
PANEL_T = 3.0   # panel thickness left by the counterbores in bell.py


def load_catalog():
    return yaml.safe_load(CATALOG.read_text())['parts']


def load_layout():
    return yaml.safe_load(LAYOUT.read_text())


def proxy(spec):
    """Manifold in local coords. Panel parts: z=0 is the outer panel face, body extends to -z."""
    p = spec['proxy']; k = p['kind']
    if k == 'box':
        sx, sy, sz = p['size']; return box(sx, sy, sz, False).translate([-sx/2, -sy/2, 0])
    if k == 'cyl':
        return cyl(p['h'], p['d']/2, False, 48)
    if k == 'ring':
        return cyl(p['h'], p['od']/2, False, 64) - cyl(p['h']*3, p['id']/2, True, 64)
    if k == 'panel':
        fw, fh, ft = p['flange']; bw, bh, bd = p['body']
        flange = box(fw, fh, ft, False).translate([-fw/2, -fh/2, 0])
        body = box(bw, bh, bd, False).translate([-bw/2, -bh/2, -PANEL_T - bd])
        return flange + body
    raise ValueError(f'unknown proxy kind {k}')


def _confidence(spec):
    c = spec.get('confidence', 'unknown')
    if isinstance(c, dict):
        levels = set(c.values())
        return 'measured' if levels == {'measured'} else '/'.join(sorted(levels))
    return c


def place_panel(item, catalog):
    spec = catalog[item['part']]
    i = idx_at_y_leg(item['y']); a, k, w = profile(DIST[i]); _, n, t = face_point(i, item['phi'])
    vv = np.cross(n, t); origin = PTS[i] + n*a + vv*item['v']
    M = proxy(spec).rotate([0, 0, item.get('rot', 0)])
    # local x -> along the leg (t), local y -> across the face (n x t), local z -> outward normal
    return placed(M, origin, t, vv)


def place_internal(item, catalog):
    spec = catalog[item['part']]
    x = np.asarray(item['x_axis'], float); z = np.asarray(item['z_axis'], float)
    y = np.cross(z, x)
    return placed(proxy(spec), item['pos'], x, y)


def placed_parts():
    cat = load_catalog(); lay = load_layout(); out = []
    for it in lay.get('panel') or []:
        out.append((it['id'], it['part'], place_panel(it, cat), 'panel'))
    for it in lay.get('internal') or []:
        out.append((it['id'], it['part'], place_internal(it, cat), 'internal'))
    return out, cat


def fit_report(shell_parts: dict, min_overlap_mm3=1.0):
    """shell_parts: name -> Manifold of printed parts. Returns (lines, problems)."""
    items, cat = placed_parts()
    lines, problems = [], 0
    lines.append(f"{'component':<14} {'part':<16} {'confidence':<22} result")
    for cid, part, M, kind in items:
        hits = []
        for sname, S in shell_parts.items():
            v = (M ^ S).volume()
            if v > min_overlap_mm3:
                hits.append(f'{sname} {v:.0f} mm3')
        res = 'OK' if not hits else 'COLLIDES: ' + ', '.join(hits)
        problems += bool(hits)
        lines.append(f'{cid:<14} {part:<16} {_confidence(cat[part]):<22} {res}')
    for a in range(len(items)):
        for b in range(a+1, len(items)):
            v = (items[a][2] ^ items[b][2]).volume()
            if v > min_overlap_mm3:
                problems += 1
                lines.append(f'{items[a][0]} <-> {items[b][0]}: overlap {v:.0f} mm3')
    open_items = [(k, s['to_measure']) for k, s in cat.items() if s.get('to_measure')]
    lines.append(f'\n{len(open_items)} catalog parts still have open measurements (see to_measure in catalog.yaml).')
    return lines, problems


def export_proxies(out_dir: Path):
    """All placed proxies as one coloured-by-name mesh set, for viewing next to the shell."""
    items, _ = placed_parts()
    meshes = []
    for cid, part, M, kind in items:
        mm = M.to_mesh(); meshes.append(trimesh.Trimesh(mm.vert_properties[:, :3], mm.tri_verts, process=False))
    if meshes:
        trimesh.util.concatenate(meshes).export(out_dir / 'proxies.stl')
