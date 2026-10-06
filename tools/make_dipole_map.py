"""
make_dipole_map.py
Renders the 3D dipole field map used on the MEG-TREC home page
(images/dipole-map.png).

Model
-----
* Head: sphere of radius HEAD_R centered at the origin (meters).
* Source: one current dipole, tangential to the sphere, DIPOLE_DEPTH below
  the scalp. Moment Q_MOMENT in A*m (10 nAm is a typical evoked response).
* Sensors: a helmet surface (upper portion of a sphere of radius HELMET_R).
* Displayed quantity: the radial magnetic field Br on the helmet. For a
  spherical conductor the radial field equals that of the primary dipole
  alone (volume currents do not contribute), so it is computed with
      Br = mu0/(4*pi) * (Q x (r - r0)) . r_hat / |r - r0|^3
  (Sarvas 1987, Phys Med Biol 32:11-22).

Usage:  python3 tools/make_dipole_map.py      (writes images/dipole-map.png)
Requires numpy and matplotlib.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")                      # render without a display
import matplotlib.pyplot as plt
from matplotlib import cm, colors

# ── Parameters (SI units) ──────────────────────────────────────────────────
HEAD_R = 0.090          # head (sphere) radius, m
HELMET_R = 0.105        # sensor surface radius, m
DIPOLE_DEPTH = 0.025    # depth of the source below the head surface, m
Q_MOMENT = 10e-9        # dipole moment, A*m (10 nAm)
MU0_4PI = 1e-7          # mu0 / (4*pi), T*m/A
GRID_N = 360            # surface resolution (points per angular direction)
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "images", "dipole-map.png")

# Site colors (match style.css tokens)
NAVY = "#0f2a44"


def radial_field(points, r0, q):
    """Radial field Br (tesla) at each row of `points` (N x 3)."""
    d = points - r0                                   # vectors source -> sensor
    dist = np.linalg.norm(d, axis=1)
    dist = np.maximum(dist, 1e-6)                     # guard against division by zero
    r_hat = points / np.linalg.norm(points, axis=1)[:, None]
    cross = np.cross(q, d)                            # Q x (r - r0)
    return MU0_4PI * np.einsum("ij,ij->i", cross, r_hat) / dist**3


def main():
    # Dipole location: over the left temporoparietal region, tangential orientation
    src_dir = np.array([-0.55, 0.15, 0.82])
    src_dir /= np.linalg.norm(src_dir)
    r0 = src_dir * (HEAD_R - DIPOLE_DEPTH)

    # Tangential orientation: perpendicular to the radial direction
    q_dir = np.cross(src_dir, np.array([0.0, 1.0, 0.0]))
    q_dir /= np.linalg.norm(q_dir)
    q = q_dir * Q_MOMENT

    # Helmet surface in spherical coordinates (theta from vertex, phi azimuth)
    theta = np.linspace(0, np.pi, GRID_N)     # closed surface, so no open rim shows
    phi = np.linspace(0, 2 * np.pi, GRID_N)
    TH, PH = np.meshgrid(theta, phi)
    X = HELMET_R * np.sin(TH) * np.cos(PH)
    Y = HELMET_R * np.sin(TH) * np.sin(PH)
    Z = HELMET_R * np.cos(TH)
    pts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])

    br = radial_field(pts, r0, q).reshape(X.shape) * 1e15   # convert to fT
    vmax = np.max(np.abs(br))
    if vmax <= 0:                                            # should not happen
        raise RuntimeError("Field map is empty; check dipole parameters.")
    norm = colors.TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
    cmap = plt.get_cmap("RdBu_r")
    face = cmap(norm(br))
    face[..., 3] = 1.0                                       # opaque surface

    # Isofield contour lines: painted directly into the surface colors by
    # marking grid cells where the field crosses a contour level. (Drawing
    # separate 3D lines is unreliable because matplotlib does not hide lines
    # behind surfaces.)
    n_levels = 12
    step = 2 * vmax / n_levels
    band = np.floor(br / step)                               # contour band index
    edge = np.zeros_like(band, dtype=bool)
    edge[1:, :] |= band[1:, :] != band[:-1, :]               # change along phi
    edge[:, 1:] |= band[:, 1:] != band[:, :-1]               # change along theta
    face[edge, :3] = 0.35 * face[edge, :3] + 0.65            # blend toward white

    # Simple diffuse lighting so the sphere reads as three dimensional.
    # Surface normals of a sphere are the unit position vectors.
    normals = np.stack([X, Y, Z], axis=-1) / HELMET_R
    light = np.array([-0.6, 0.5, 0.65])
    light /= np.linalg.norm(light)
    lambert = np.clip(np.einsum("ijk,k->ij", normals, light), 0.0, 1.0)
    face[..., :3] *= (0.55 + 0.45 * lambert)[..., None]

    fig = plt.figure(figsize=(9, 7.5), dpi=160, facecolor=NAVY)
    ax = fig.add_subplot(111, projection="3d", facecolor=NAVY)
    ax.computed_zorder = False      # draw in the order given, so the arrow stays on top

    # Sensor surface with field map
    ax.plot_surface(X, Y, Z, facecolors=face, rstride=1, cstride=1,
                    linewidth=0, edgecolor='none', antialiased=False, shade=False, zorder=1)

    # Dipole arrow, drawn just outside the helmet above the source location
    # so it is visible; its direction matches the source orientation.
    base = src_dir * HELMET_R * 1.02 - q_dir * 0.018
    ax.quiver(*base, *(q_dir * 0.036), color="#5fbfb8", linewidth=3,
              arrow_length_ratio=0.35, zorder=5)
    ax.scatter(*(src_dir * HELMET_R * 1.02), color="#5fbfb8", s=18, zorder=6)

    # Nose marker (+y is anterior)
    ax.plot([0, 0], [HELMET_R * 0.98, HELMET_R * 1.12], [0.01, 0.01],
            color="white", linewidth=2, alpha=0.6, zorder=4)

    ax.set_box_aspect((1, 1, 1))
    lim = HELMET_R * 1.05
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.view_init(elev=30, azim=170)     # viewed from the left, slightly from the front
    ax.set_axis_off()

    # Color bar
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.45, pad=0.0, aspect=18)
    cbar.set_label("Radial field (fT)", color="white", fontsize=10)
    cbar.ax.tick_params(colors="white", labelsize=8)
    cbar.outline.set_edgecolor((1, 1, 1, 0.3))

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, facecolor=NAVY, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)

    # Trim the empty navy margin that matplotlib leaves around 3D axes
    try:
        from PIL import Image, ImageChops
        img = Image.open(OUT_PATH).convert("RGB")
        bg = Image.new("RGB", img.size, colors.to_hex(NAVY))
        bbox = ImageChops.difference(img, bg).getbbox()
        if bbox:                                   # None means the image is blank
            pad = 30
            left, top = max(bbox[0] - pad, 0), max(bbox[1] - pad, 0)
            right, bottom = min(bbox[2] + pad, img.width), min(bbox[3] + pad, img.height)
            img.crop((left, top, right, bottom)).save(OUT_PATH, optimize=True)
    except ImportError:
        pass                                       # Pillow not installed; keep untrimmed image

    print(f"Wrote {os.path.abspath(OUT_PATH)}  (peak |Br| = {vmax:.0f} fT)")


if __name__ == "__main__":
    main()
