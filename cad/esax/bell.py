"""EMEO hex bell V1 – all printed parts.

Ported 1:1 from the V1.3 design (Oct 2026). Every dimension is a parameter here or in geom.py.
Frame and units: see geom.py (mm, Y along the EMEO, EMEO axis at x=0/z=0).
Mounting positions on the pads are expressed as (phi, y, v): phi = face angle (90 = player side,
270 = audience side), y = height on the straight leg, v = offset across the face.
"""
from pathlib import Path
import numpy as np, trimesh, manifold3d as m3d
from .geom import *

VENDOR = Path(__file__).resolve().parent.parent / 'vendor'

W = P['wall']; CLR = 0.25; SPIG = 3.2
J1_Y = 10.0
J2_D = D_LEG_END
PAD_Y0, PAD_Y1 = 18.0, 120.0
XSPLIT = -52.0

def cyl_along(origin, n, t, h, r, seg=48):
    """cylinder of height h centred at origin, axis n"""
    return placed(cyl(h, r, True, seg), origin, t, np.cross(n, t))
def box_along(origin, n, t, lt, lv, ln):
    """box: lt along t, lv along n×t, ln along n, centred at origin"""
    return placed(box(lt, lv, ln), origin, t, np.cross(n, t))

def idx_range_d(d0, d1):
    return [i for i, d in enumerate(DIST) if d0-1e-6 <= d <= d1+1e-6]
def idx_range_y(y0, y1):
    xl = -2*P['bend_R']
    return [i for i, p in enumerate(PTS) if abs(p[0]-xl) < 1e-6 and y0-1e-6 <= p[1] <= y1+1e-6]


def build():
    """Return dict name -> manifold3d.Manifold for every printable part."""
    # ---------- base shell ----------
    tube = to_man(loft_tube(range(len(PTS)), W))

    # Nerd-Sniped clamp/socket crop (OCL v1 remix)
    f002 = to_man(trimesh.load(VENDOR / 'nerd-sniped' / 'fonia-002-01.stl'))
    crop = placed(cyl(48, 42.5, True, 96), [0, 2, 0], [1, 0, 0], [0, 0, -1])
    socket = f002 ^ crop
    # re-bore the clamp insert holes (orig. 6 mm) to standard M3 heat-set inserts (4.2 mm, 6 mm deep)
    for (bx, bz) in ((-35.3, 0.0), (-14.9, 32.0), (-14.9, -32.0)):
        socket = socket + placed(cyl(7.9, 3.1, False, 32), [bx, -14.3, bz], [1, 0, 0], [0, 0, -1])
        socket = socket - placed(cyl(6.3, 2.0, False, 32), [bx, -12.4, bz], [1, 0, 0], [0, 0, -1])

    # rim plate with screen pocket
    e = len(PTS)-1; pe, te = PTS[e], TAN[e]; Ne, Be = frame(te)
    r_rim = radius(PHI, P['a_rim'], 0, 1)
    r_rin = radius(PHI, P['a_rim']-2.4, 0, 1)
    def hexprism(r, h, z0): 
        pts = np.c_[r*np.cos(PHI), r*np.sin(PHI)]
        return m3d.CrossSection([pts.tolist()]).extrude(h).translate([0, 0, z0])
    T = P['rim_plate']; pocket_z0 = T - P['screen_depth']; Rp = P['screen_d']/2
    rim = hexprism(r_rim, T+0.5, -0.5) - hexprism(r_rin, T+2, -1)                 # outer hex wall
    rim = rim + (hexprism(r_rim, 2.0, T-2.0) - cyl(10, Rp, True, 180).translate([0, 0, T]))   # front frame
    rim = rim + (cyl(P['screen_depth'], Rp+2.4, False, 180) - cyl(20, Rp, True, 180)).translate([0, 0, pocket_z0])  # pocket wall
    rim = rim + (cyl(3.0, Rp+2.4, False, 180) - cyl(10, P['rim_open_d']/2, True, 128)).translate([0, 0, pocket_z0-3.0])  # ledge
    for k in range(6):   # stiffening webs between pocket wall and hex wall
        web = box(P['a_rim']-Rp+2, 2.0, T-(pocket_z0-3.0), False).translate([Rp, -1.0, pocket_z0-3.0])
        rim = rim + web.rotate([0, 0, 30+60*k])
    COVER_SCREW_R = 71.0
    for k in range(4):
        a = np.radians(45+90*k)
        rim = rim - cyl(30, 1.7, True, 24).translate([COVER_SCREW_R*np.cos(a), COVER_SCREW_R*np.sin(a), 0])
    rim = placed(rim, pe, Ne, Be)

    shell = tube + socket + rim

    # ---------- pads (flat control plates on ±z faces of the leg) ----------
    i_mid = idx_at_y_leg((PAD_Y0+PAD_Y1)/2)
    pads = []
    for phi in (90, 270):
        a, k, w = profile(DIST[i_mid])
        p0, n, t = face_point(i_mid, phi)
        centre = PTS[i_mid] + n*(a-3.0)
        pads.append(box_along(centre, n, t, PAD_Y1-PAD_Y0, 50.0, 6.0))
    shell = shell + pads[0] + pads[1]

    def pad_pos(phi, y, v):
        i = idx_at_y_leg(y); a, k, w = profile(DIST[i])
        _, n, t = face_point(i, phi)
        vv = np.cross(n, t)
        return PTS[i] + n*a + vv*v, n, t, a

    cuts = []
    def hole(phi, y, v, dia, cb_dia=None, keep=3.0):
        o, n, t, a = pad_pos(phi, y, v)
        cuts.append(cyl_along(o, n, t, 30, dia/2))
        if cb_dia:  # counterbore from inside, leaves `keep` mm panel
            cuts.append(cyl_along(o - n*(keep+10), n, t, 20, cb_dia/2))
    def slot(phi, y, v, lt, lv, cb=None, keep=3.0):
        o, n, t, a = pad_pos(phi, y, v)
        cuts.append(box_along(o, n, t, lt, lv, 30))
        if cb: cuts.append(box_along(o - n*(keep+10), n, t, cb[0], cb[1], 20))

    HOLES = dict(toggle=6.4, button=16.2, dhole=24.2)
    def dcut(phi, y, v, rot=False, cb=(34, 28)):
        """Neutrik D-size cutout: 24 mm hole + 2x 3.4 mm on a 19 x 24 diagonal. rot=True: 31 mm flange side across the face"""
        hole(phi, y, v, HOLES['dhole'])
        pts = ((12, 9.5), (-12, -9.5)) if not rot else ((9.5, 12), (-9.5, -12))   # (dy, dv): 24 mm along the 31 mm flange side
        for dy, dv in pts: hole(phi, y+dy, v+dv, 3.4)
        o, n, t, a = pad_pos(phi, y, v)
        cuts.append(box_along(o - n*(3.0+10), n, t, cb[1], cb[0], 20))         # room for nuts/body behind 3 mm panel
    # +z pad : player-side controls (bottom to top)
    for v in (-15, 0, 15): hole(90, 28, v, HOLES['toggle'])                # MIDI | Pi | LED/Display
    o, n, t, a = pad_pos(90, 28, 0)                                        # one pocket behind the row: toggle body is
    cuts.append(box_along(o - n*(3.0+10), n, t, 16, 46, 20))               # 12.5 x 6.5 (diag 14.1) – round 13 mm pockets were too small
    hole(90, 52, 0, HOLES['button'], 24)                                    # Pi button (19 mm head)
    dcut(90, 82, 0, rot=True)                                               # headphones (Hicon HI-J35SEFD, D-size)
    slot(90, 110, 0, 3.8, 9.8, cb=(16, 12))                                 # USB-C charge port (board perpendicular behind)
    # -z pad : audience side, MIDI socket + TX02 cradle
    dcut(270, 32, 0, rot=False, cb=(30, 34))                                # MIDI socket (D-size)
    for y in (62, 108):   # heat-set inserts for cradle (internal boss so a 5.7 mm insert fits)
        o, n, t, a = pad_pos(270, y, 0)
        shell = shell + cyl_along(o - n*7.0, n, t, 4.0, 4.6)
        cuts.append(cyl_along(o - n*3.2, n, t, 6.4, 2.0))
    # vents: intake low toward the body, exhaust high on the outer faces
    for phi, y0 in ((150, 45), (210, 45), (30, 100), (330, 100)):
        i = idx_at_y_leg(y0); a, k, w = profile(DIST[i]); _, n, t = face_point(i, phi)
        vv = np.cross(n, t)
        for v in np.linspace(-12, 12, 5):
            cuts.append(box_along(PTS[i] + n*a + vv*v, n, t, 18, 2.6, 30))
    yb = P['start_y'] - P['drop'] - P['bend_R']
    for dx in (-8, 8):   # EMEO bottom cap has a drain hole – let condensation out at the lowest point
        cuts.append(placed(cyl(40, 1.75, True, 24), [-P['bend_R']+dx, yb-50, 0], [1, 0, 0], [0, 0, -1]))
    shell = shell - m3d.Manifold.batch_boolean(cuts, m3d.OpType.Add)

    # ---------- split ----------
    def region(x0, x1, y0, y1):
        return box(x1-x0, y1-y0, 800).translate([(x0+x1)/2, (y0+y1)/2, 0])
    y_leg_top = P['leg_top_y']
    partA = shell - region(-1000, XSPLIT, J1_Y, 1000)
    partB = shell ^ region(-1000, XSPLIT, J1_Y, y_leg_top)
    partC = shell ^ region(-1000, XSPLIT, y_leg_top, 1000)

    # ---------- joints ----------
    def joint(lower, upper, spig_idx, bridge_idx, screw_idx):
        spig = loft_offsets(spig_idx, W+CLR, W+CLR+SPIG)
        bridge = loft_offsets(bridge_idx, W-0.6, W+CLR+SPIG)
        upper = upper + spig + bridge
        for phi in (90, 210, 330):
            o, n, t = face_point(screw_idx, phi)
            a, k, w = profile(DIST[screw_idx]); r_in = radius(np.array([np.radians(phi)]), a-W-CLR, k, w)[0]
            base = PTS[screw_idx] + n*r_in
            upper = upper + cyl_along(base - n*3.8, n, t, 7.6, 4.6)          # boss
            upper = upper - cyl_along(base - n*3.0, n, t, 6.2, 2.0)          # insert hole (ruthex M3x5.7)
            lower = lower - cyl_along(o, n, t, 14, 1.7)                      # clearance hole
        return lower, upper

    sp1 = idx_range_y(J1_Y-15, J1_Y+0.5); br1 = idx_range_y(J1_Y, J1_Y+4); sc1 = idx_at_y_leg(J1_Y-7)
    partA, partB = joint(partA, partB, sp1, br1, sc1)
    sp2 = idx_range_d(J2_D-15, J2_D+0.5); br2 = idx_range_d(J2_D-0.5, J2_D+5)
    sc2 = min(range(len(PTS)), key=lambda i: abs(DIST[i]-(J2_D-7)))
    partB, partC = joint(partB, partC, sp2, br2, sc2)

    # ---------- cover plate (V1, LED ring backlight, ribbed & light) ----------
    cov_t = P['screen_depth'] - 0.2
    R_cov = (P['screen_d']-0.6)/2
    skin = 2.4
    cover = cyl(skin, R_cov, False, 180)
    cover = cover + (cyl(cov_t, R_cov, False, 180) - cyl(40, R_cov-3.0, True, 180))    # outer lip
    for k in range(6):                                                                        # radial ribs
        a = np.radians(30*k)
        rib = box(2*R_cov-4, 2.0, cov_t-skin, False).translate([-(R_cov-2), -1.0, skin])
        cover = cover + rib.rotate([0, 0, 30*k])
    RING_ID, RING_OD = 34.0, 44.0          # Botland CJMCU-2812-16 ring: 44 / 34 mm
    cover = cover + (cyl(4.0, RING_OD/2+2.2, False, 96) - cyl(9, RING_OD/2+0.4, True, 96)).translate([0, 0, skin])  # ring seat wall
    cover = cover - (cyl(1.4, RING_OD/2+0.4, False, 96) - cyl(3, RING_ID/2-0.4, True, 96)).translate([0, 0, skin-1.4])  # 1.0 mm skin over LEDs
    cover = cover - cyl(10, RING_ID/2-3, True, 64)            # centre opening (wires / V2 screen cable)
    for k in range(4):
        a = np.radians(45+90*k); c = [COVER_SCREW_R*np.cos(a), COVER_SCREW_R*np.sin(a), 0]
        cover = cover + cyl(cov_t-skin, 4.6, False, 32).translate([c[0], c[1], skin])
        cover = cover - cyl(6.2, 2.0, False, 24).translate([c[0], c[1], cov_t-6.2])
    # ---------- TX02 cradle ----------
    TXL, TXW, TXH = 62.0, 48.0, 15.0
    bl, bw, bt = 70.0, TXW + 1.0 + 2*2.5, 3.0
    cr = box(bl, bw, bt, False).translate([-bl/2, -bw/2, 0])
    for s in (-1, 1):
        rail = box(bl-2, 2.5, TXH+0.6+1.6+0.2, False).translate([-bl/2+2, s*(TXW/2+0.5) + (0 if s > 0 else -2.5), bt-0.2])
        lip = box(bl-2, 1.8, 1.6, False).translate([-bl/2+2, (TXW/2+0.5-1.6) if s > 0 else -(TXW/2+0.5+0.2), bt+TXH+0.6])
        cr = cr + rail + lip
    cr = cr + box(2.5, bw, TXH*0.6, False).translate([bl/2-2.5, -bw/2, bt-0.2])        # end stop (top)
    cr = cr + box(1.2, TXW-10, 1.0, False).translate([-bl/2+8, -(TXW-10)/2, bt-0.2])    # detent ridge (open end)
    for x in (-23, 23):
        cr = cr - cyl(10, 1.7, True, 24).translate([x, 0, 0])
        cr = cr - m3d.Manifold.cylinder(1.8, 1.7, 3.4, 32, False).translate([x, 0, bt-1.8])  # countersink
    cr = cr - box(bl*0.55, TXW-16, 10).translate([-4, 0, 0])   # window: back (battery door) visible/push-out

    # ---------- hole gauge ----------
    gauge = box(150, 42, 3, False)
    gx = 10
    for d in (6.2, 6.4, 6.7, 16.2, 24.2, 4.0):
        gauge = gauge - cyl(10, d/2).translate([gx+d/2, 21, 0]); gx += d + 8
    gauge = gauge - box(9.6, 3.6, 10).translate([gx+5, 21, 0])
    cx = 10+6.2+8+6.4+8+6.7+8+16.2+8+12.1           # centre of the 24.2 D-hole
    for dx, dy in ((12, 9.5), (-12, -9.5)): gauge = gauge - cyl(10, 1.7).translate([cx+dx, 21+dy, 0])

    # ---------- collar fit test (socket region of part A only) ----------
    ctest = partA ^ box(100, 56, 100).translate([0, 2, 0])
    ctest = ctest - box(100, 100, 100).translate([-100, 2, 0])

    return dict(A_collar_bow=partA, B_leg_controls=partB, C_bell_rim=partC,
                D_cover_plate=cover, E_tx02_cradle=cr, F_hole_gauge=gauge,
                H_collar_fit_test=ctest)
