"""Build the self-contained three.js preview page (cad/build/viewer.html).

Meshes are decimated and embedded as base64 so the page works offline / as a published artifact.
"""
from pathlib import Path
import base64, json
import numpy as np, trimesh
from .geom import PTS, TAN, DIST, P, frame, idx_at_y_leg, profile, face_point

HERE = Path(__file__).resolve().parent.parent


def _enc(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()


def _pack(m, target=None):
    if target and len(m.faces) > target:
        m = m.simplify_quadric_decimation(face_count=target)
    return dict(v=_enc(m.vertices.astype(np.float32)), f=_enc(m.faces.astype(np.uint32)),
                nv=len(m.vertices), nf=len(m.faces))


def _padp(phi, y, v):
    i = idx_at_y_leg(y); a, k, w = profile(DIST[i]); _, n, t = face_point(i, phi)
    vv = np.cross(n, t)
    return (PTS[i] + n * a + vv * v).tolist(), n.tolist()


def build_viewer(build_dir: Path, out_html: Path):
    load = lambda n: trimesh.load(build_dir / f'{n}.stl')
    meshes = dict(A=_pack(load('A_collar_bow'), 30000), B=_pack(load('B_leg_controls')),
                  C=_pack(load('C_bell_rim')), G=_pack(load('G_clamp_half_NerdSniped'), 8000))
    # cover plate seated in the rim pocket
    e = len(PTS) - 1; pe, te = PTS[e], TAN[e]; Ne, Be = frame(te)
    cov = load('D_cover_plate'); T = np.eye(4)
    T[:3, 0] = Ne; T[:3, 1] = Be; T[:3, 2] = -te; T[:3, 3] = pe + te * P['rim_plate']
    cov.apply_transform(T); meshes['D'] = _pack(cov)
    # TX02 cradle on the audience pad
    cr = load('E_tx02_cradle'); T = np.eye(4)
    T[:3, 0] = [0, 1, 0]; T[:3, 1] = [1, 0, 0]; T[:3, 2] = [0, 0, -1]; T[:3, 3] = [-116, 85, -46]
    cr.apply_transform(T); meshes['E'] = _pack(cr)
    tx = trimesh.creation.box([62, 48, 15]); tx.apply_translation([-1, 0, 3 + 7.8]); tx.apply_transform(T)
    meshes['TX'] = _pack(tx)
    # the player's own S-bow on top of the EMEO
    sb = trimesh.load(HERE / 'vendor' / 's-bow' / 's_bow_v3.3mf', force='mesh')
    sb.apply_translation([0, 482.6, 0]); meshes['S'] = _pack(sb, 10000)
    # LED ring glow just in front of the cover skin
    ring = trimesh.creation.annulus(r_min=17, r_max=22, height=0.4, sections=64)
    Tr = np.eye(4); Tr[:3, 0] = Ne; Tr[:3, 1] = Be; Tr[:3, 2] = te; Tr[:3, 3] = pe + te * (P['rim_plate'] + 0.35)
    ring.apply_transform(Tr); meshes['R'] = _pack(ring)

    hw = []
    for y, v, kind in [(28, -15, 'toggle'), (28, 0, 'toggle'), (28, 15, 'toggle'), (52, 0, 'button'),
                       (82, 0, 'djack'), (110, 0, 'usbc')]:
        p, n = _padp(90, y, v); hw.append(dict(p=p, n=n, kind=kind))
    p, n = _padp(270, 32, 0); hw.append(dict(p=p, n=n, kind='midi'))

    ex = dict(A=[0, 0, 0], B=[0, 1, 0], C=(np.array([0, 1, 0]) * 1.6 + te * 0.8).tolist(),
              D=(te * 2.6 + np.array([0, 1.6, 0])).tolist(), E=[0, 0, -1.2], TX=[0, 0, -1.9],
              G=[-1.0, 0, 0], R=(te * 2.6 + np.array([0, 1.6, 0])).tolist())
    data = json.dumps(dict(meshes=meshes, hw=hw, explode=ex,
                           rim=dict(p=(pe + te * P['rim_plate']).tolist(), t=te.tolist())))
    tpl = (HERE / 'viewer' / 'template.html').read_text()
    out_html.write_text(tpl.replace('__DATA__', data))
    return out_html
