"""Mesh export helpers."""
from pathlib import Path
import numpy as np, trimesh


def manifold_to_trimesh(M, precise=True):
    """precise=True uses the float64 mesh (clean, indexed – best for 3MF)."""
    mm = M.to_mesh64() if precise else M.to_mesh()
    return trimesh.Trimesh(np.asarray(mm.vert_properties)[:, :3], np.asarray(mm.tri_verts), process=False)


def export_part(M, out_dir: Path, name: str) -> dict:
    """Write <name>.3mf and <name>.stl and return a small report dict."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tm = manifold_to_trimesh(M)
    tm.export(out_dir / f'{name}.3mf')
    tm.export(out_dir / f'{name}.stl')
    return dict(status=str(M.status()), volume_cm3=round(M.volume() / 1000, 1),
                extents_mm=[round(float(x), 1) for x in tm.extents], genus=int(M.genus()),
                triangles=int(len(tm.faces)))
