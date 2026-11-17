"""EMEO hex bell – parametric geometry (units: mm).
Frame: Y up, EMEO axis on x=0,z=0 (same frame as Nerd-Sniped 'fonia' parts).
Bend plane = XY. Hex corners lie in the bend plane (spine on outer/inner curve), like the S-bow.
"""
import numpy as np, trimesh, manifold3d as m3d

# ---------------- parameters ----------------
P = dict(
    wall=2.2,            # shell wall
    start_y=-20.0,       # tube starts under the Nerd-Sniped socket (overlaps crop by 2 mm)
    drop=12.0,           # straight drop before bend
    bend_R=58.0,         # U-bend radius (centerline)
    leg_top_y=140.0,     # end of straight leg / start of flare
    flare_R=180.0, flare_deg=35.0,
    a_start=40.0,        # round radius at collar
    a_bow=42.0, a_leg=46.0, a_rim=85.0,   # hex apothems (outer)
    k_bow=0.10, k_leg=0.06,               # concavity of hex faces (S-bow style)
    rim_plate=12.0,      # thickness of rim ring (along rim normal)
    screen_d=154.0, screen_depth=7.5, rim_open_d=128.0,
)
NSEG = 144  # points per section (24 per hex face)

def smooth(x):
    x = np.clip(x, 0, 1); return x*x*(3-2*x)

def path(step=2.0):
    """Centerline points, tangents, arclength."""
    pts = []
    y0 = P['start_y']; yb = y0 - P['drop']; R = P['bend_R']
    for y in np.arange(y0, yb, -step): pts.append((0, y))
    n = int(np.pi*R/step)
    for a in np.linspace(0, -np.pi, n+1): pts.append((-R + R*np.cos(a), yb + R*np.sin(a)))
    xl = -2*R
    for y in np.arange(yb+step, P['leg_top_y'], step): pts.append((xl, y))
    Rf = P['flare_R']; cx = xl - Rf
    n = int(Rf*np.radians(P['flare_deg'])/step)
    for a in np.linspace(0, np.radians(P['flare_deg']), n+1):
        pts.append((cx + Rf*np.cos(a), P['leg_top_y'] + Rf*np.sin(a)))
    Pn = np.array([(x, y, 0.0) for x, y in pts])
    # dedupe
    keep = np.r_[True, np.linalg.norm(np.diff(Pn, axis=0), axis=1) > 1e-6]
    Pn = Pn[keep]
    T = np.gradient(Pn, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Pn, axis=0), axis=1))]
    return Pn, T, d

PTS, TAN, DIST = path()
L = DIST[-1]
D_BEND_END = P['drop'] + np.pi*P['bend_R']
D_LEG_END = D_BEND_END + (P['leg_top_y'] - (P['start_y']-P['drop']))
D_FLARE0 = D_LEG_END + 25.0

def profile(d):
    """returns apothem a, concavity k, hex weight w at arclength d"""
    w = smooth((d-6)/(D_BEND_END-6))
    a = P['a_start'] + (P['a_bow']-P['a_start'])*smooth((d-6)/60) \
        + (P['a_leg']-P['a_bow'])*smooth((d-D_BEND_END+40)/80)
    if d > D_FLARE0:
        u = (d-D_FLARE0)/(L-D_FLARE0); a += (P['a_rim']-P['a_leg'])*u**2.2
    k = P['k_bow']*smooth((d-10)/(D_BEND_END*0.6))
    k += (P['k_leg']-P['k_bow'])*smooth((d-D_BEND_END)/60)
    if d > D_FLARE0:
        k *= 1-smooth((d-D_FLARE0)/(L-D_FLARE0)*1.3)
    return a, k, w

PHI = 2*np.pi*np.arange(NSEG)/NSEG
def rpoly(phi, a, k, n=6):
    per = 2*np.pi/n
    dd = (phi % per) - per/2
    return a/np.cos(dd) * (1 - k*(1-(dd/(per/2))**2))

def radius(phi, a, k, w):
    return (1-w)*a + w*rpoly(phi, a, k)

def frame(t):
    Z = np.array([0, 0, 1.0]); N = np.cross(Z, t); N /= np.linalg.norm(N); B = np.cross(t, N)
    return N, B

def section(i, off=0.0):
    p, t, d = PTS[i], TAN[i], DIST[i]
    a, k, w = profile(d)
    r = radius(PHI, a-off, k, w)
    N, B = frame(t)
    return p + np.outer(r*np.cos(PHI), N) + np.outer(r*np.sin(PHI), B)

def loft_tube(idx, wall):
    """closed thick-walled tube from section indices"""
    O = [section(i) for i in idx]; I = [section(i, wall) for i in idx]
    n = len(idx); M = NSEG
    V = np.vstack(O + I)
    F = []
    def q(a, b, c, d): F.extend([[a, b, c], [a, c, d]])
    for s in range(n-1):
        for j in range(M):
            j2 = (j+1) % M
            o0, o1, o2, o3 = s*M+j, s*M+j2, (s+1)*M+j2, (s+1)*M+j
            q(o0, o3, o2, o1)                       # outer (normals out)
            i0, i1, i2, i3 = [x + n*M for x in (o0, o1, o2, o3)]
            q(i0, i1, i2, i3)                       # inner (normals in)
    for j in range(M):                              # start + end annulus
        j2 = (j+1) % M
        q(j, j2, n*M+j2, n*M+j)
        e = (n-1)*M
        q(e+j, n*M+e+j, n*M+e+j2, e+j2)
    m = trimesh.Trimesh(V, np.array(F), process=True)
    if m.volume < 0: m.invert()
    return m

def to_man(m):
    m = m.copy(); m.merge_vertices()
    return m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                                 tri_verts=np.asarray(m.faces, np.uint32)))

def to_tri(M):
    mm = M.to_mesh(); return trimesh.Trimesh(mm.vert_properties[:, :3], mm.tri_verts, process=False)

def placed(M, origin, xdir, ydir):
    """place a manifold built in local coords (x=xdir, y=ydir, z=xdir×ydir) at origin"""
    x = np.asarray(xdir, float); x /= np.linalg.norm(x)
    y = np.asarray(ydir, float); y = y - x*np.dot(x, y); y /= np.linalg.norm(y)
    z = np.cross(x, y)
    Mx = np.c_[x, y, z, origin]
    return M.transform(Mx.tolist())

def box(sx, sy, sz, center=True): return m3d.Manifold.cube([sx, sy, sz], center)
def cyl(h, r, center=True, seg=64): return m3d.Manifold.cylinder(h, r, r, seg, center)

def loft_offsets(idx, off_out, off_in):
    """solid tube between two offset surfaces (off measured inward from outer skin)"""
    O = [section(i, off_out) for i in idx]; I = [section(i, off_in) for i in idx]
    n = len(idx); M = NSEG; V = np.vstack(O + I); F = []
    def q(a, b, c, d): F.extend([[a, b, c], [a, c, d]])
    for s in range(n-1):
        for j in range(M):
            j2 = (j+1) % M
            o0, o1, o2, o3 = s*M+j, s*M+j2, (s+1)*M+j2, (s+1)*M+j
            q(o0, o3, o2, o1)
            i0, i1, i2, i3 = [x+n*M for x in (o0, o1, o2, o3)]
            q(i0, i1, i2, i3)
    for j in range(M):
        j2 = (j+1) % M; e = (n-1)*M
        q(j, j2, n*M+j2, n*M+j); q(e+j, n*M+e+j, n*M+e+j2, e+j2)
    m = trimesh.Trimesh(V, np.array(F), process=True)
    if m.volume < 0: m.invert()
    return to_man(m)

def idx_at_y_leg(y):
    """section index on the straight leg nearest to height y"""
    xl = -2*P['bend_R']
    cand = [i for i, p in enumerate(PTS) if abs(p[0]-xl) < 1e-6]
    return min(cand, key=lambda i: abs(PTS[i][1]-y))

def face_point(i, phi_deg, off=0.0):
    """point on hex face centre (outer skin minus off) and outward normal"""
    p, t, d = PTS[i], TAN[i], DIST[i]; a, k, w = profile(d)
    N, B = frame(t); ph = np.radians(phi_deg)
    n = np.cos(ph)*N + np.sin(ph)*B
    r = radius(np.array([ph]), a-off, k, w)[0]
    return p + r*n, n, t
