"""Generate the figures for the 'Quantitative models' chapter.

Run from the book root:
    MPLCONFIGDIR=.mplcache ./.venv/bin/python sims/make_figures.py

Figures are written as PDF into ../figures/ (i.e. book/figures/).
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

import receiver_models as rm

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.normpath(os.path.join(HERE, "..", "figures"))
FONTDIR = os.path.normpath(os.path.join(HERE, "..", "fonts"))
os.makedirs(FIGDIR, exist_ok=True)

# Register Alegreya Sans (the book's body font) so figures match the text.
for _ttf in (
    "AlegreyaSans-Regular.ttf", "AlegreyaSans-Italic.ttf",
    "AlegreyaSans-Bold.ttf", "AlegreyaSans-BoldItalic.ttf",
    "AlegreyaSans-Medium.ttf", "AlegreyaSans-Light.ttf",
):
    _path = os.path.join(FONTDIR, _ttf)
    if os.path.exists(_path):
        font_manager.fontManager.addfont(_path)

# A restrained, book-friendly style: Alegreya Sans text, muted palette, light grid.
plt.rcParams.update({
    "font.family": "Alegreya Sans",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Alegreya Sans",
    "mathtext.it": "Alegreya Sans:italic",
    "mathtext.bf": "Alegreya Sans:bold",
    "mathtext.sf": "Alegreya Sans",
    "mathtext.fallback": "cm",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

BLUE, RED, GREEN, ORANGE, GREY = "#1f4e79", "#a4262c", "#2e7d32", "#e07b00", "#666666"


def save(fig, name):
    path = os.path.join(FIGDIR, name)
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
def fig_liv_sketch():
    """Idealized LIV curve with labeled I_th, slope, kink, rollover (schematic)."""
    I = np.linspace(0, 120, 500)  # mA
    Ith = 18.0
    eta = 0.45  # mW/mA above threshold (schematic)
    P = np.zeros_like(I)
    above = I > Ith
    P[above] = eta * (I[above] - Ith)
    # soft rollover above ~90 mA
    roll = I > 90
    P[roll] = eta * (90 - Ith) * (1 - 0.35 * ((I[roll] - 90) / 30) ** 2)
    P = np.clip(P, 0, None)
    # kink region around 70 mA (schematic dip in slope)
    kink = (I > 65) & (I < 78)
    P[kink] *= 0.92

    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.plot(I, P, color=BLUE, lw=1.8)
    ax.axvline(Ith, color=GREY, lw=0.9, ls="--")
    ax.annotate(r"$I_{\mathrm{th}}$", (Ith, 2), textcoords="offset points",
                xytext=(6, 8), fontsize=9, color=GREY)
    # slope segment
    ax.annotate("slope efficiency", (40, eta * (40 - Ith)),
                textcoords="offset points", xytext=(10, 12), fontsize=8, color=BLUE)
    ax.annotate("kink", (70, eta * (70 - Ith) * 0.92),
                textcoords="offset points", xytext=(-18, 14), fontsize=8, color=ORANGE)
    ax.annotate("thermal rollover", (100, P[I >= 100][0] if np.any(I >= 100) else 20),
                textcoords="offset points", xytext=(-40, -18), fontsize=8, color=RED)
    ax.set_xlabel("Bias current (mA)")
    ax.set_ylabel("Optical power (mW)")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, max(P) * 1.15)
    ax.set_title("Schematic LIV (not measured data)", fontsize=9)
    save(fig, "fig_liv_sketch.pdf")


def fig_ber_vs_q():
    """The fundamental Gaussian BER(Q) curve with FEC anchors."""
    q = np.linspace(2.5, 8.5, 400)
    ber = rm.q_to_ber(q)

    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    ax.semilogy(q, ber, color=BLUE, lw=1.6)

    anchors = [
        (rm.BER_UNCODED, "BER $10^{-12}$ (uncoded)", RED),
        (rm.BER_KP4_PRE, "KP4 pre-FEC $2.4\\times10^{-4}$", GREEN),
    ]
    for b, label, col in anchors:
        qv = float(rm.ber_to_q(b))
        ax.plot([qv, qv], [1e-16, b], color=col, lw=0.9, ls="--")
        ax.plot([2.5, qv], [b, b], color=col, lw=0.9, ls="--")
        ax.plot(qv, b, "o", color=col, ms=4)
        ax.annotate(f"{label}\n$Q={qv:.2f}$", (qv, b),
                    textcoords="offset points", xytext=(6, 6),
                    fontsize=7, color=col)

    ax.set_xlabel("Quality factor $Q$")
    ax.set_ylabel("Bit-error ratio")
    ax.set_ylim(1e-16, 1e-1)
    ax.set_xlim(2.5, 8.5)
    ax.set_title("Gaussian decision: $\\mathrm{BER}=\\frac{1}{2}\\,\\mathrm{erfc}(Q/\\sqrt{2})$")
    save(fig, "fig_ber_vs_q.pdf")


# ---------------------------------------------------------------------------
def fig_ber_vs_power_rin():
    """BER vs average received power, showing RIN-induced error floors."""
    R = 0.8            # A/W
    bw = 40e9          # Hz (about 2/3 of 60 GBaud)
    i_th = 25e-12 * np.sqrt(bw)   # 25 pA/rtHz input-referred TIA noise
    er_db = 6.0

    p_dbm = np.linspace(-16, 6, 400)
    p_w = rm.dbm_to_w(p_dbm)

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    # RIN values chosen to make the floor visible; good DFBs ($<-150$ dB/Hz)
    # show no floor in this frame, which is itself the engineering point.
    cases = [
        (-np.inf, "no RIN (thermal+shot only)", GREY, "-"),
        (-124.0, "RIN $-124$ dB/Hz", BLUE, "-"),
        (-120.0, "RIN $-120$ dB/Hz", GREEN, "-"),
        (-116.0, "RIN $-116$ dB/Hz", RED, "-"),
    ]
    for rin_db, label, col, ls in cases:
        ber = rm.nrz_ber(p_w, responsivity=R, i_thermal_rms=i_th, bw=bw,
                         er_db=er_db, rin_db_hz=rin_db)
        ax.semilogy(p_dbm, np.clip(ber, 1e-16, 0.5), color=col, ls=ls,
                    lw=1.5, label=label)

    ax.axhline(rm.BER_UNCODED, color="k", lw=0.7, ls=":")
    ax.text(-15.5, rm.BER_UNCODED * 1.5, "$10^{-12}$", fontsize=7)
    ax.axhline(rm.BER_KP4_PRE, color=ORANGE, lw=0.7, ls=":")
    ax.text(-15.5, rm.BER_KP4_PRE * 1.6, "KP4 pre-FEC", fontsize=7, color=ORANGE)

    ax.set_xlabel("Average received power [dBm]")
    ax.set_ylabel("Bit-error ratio")
    ax.set_ylim(1e-16, 0.5)
    ax.set_xlim(-16, 6)
    ax.set_title("RIN sets a BER floor no power can beat (NRZ, ER = 6 dB, BW = 40 GHz)")
    ax.legend(loc="lower left", framealpha=0.9)
    save(fig, "fig_ber_vs_power_rin.pdf")


# ---------------------------------------------------------------------------
def fig_rin_floor():
    """RIN-limited Q floor (and equivalent BER floor) vs RIN, for several rates."""
    rin_db = np.linspace(-160, -125, 400)

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    rates = [
        (17.5e9, "25G NRZ (BW 17.5 GHz)", BLUE),
        (37e9, "100G PAM4 (BW 37 GHz)", GREEN),
        (75e9, "200G PAM4 (BW 75 GHz)", RED),
    ]
    for bw, label, col in rates:
        q_floor = np.array([rm.rin_q_floor(r, bw) for r in rin_db])
        ax.semilogy(rin_db, q_floor, color=col, lw=1.5, label=label)

    for b, txt in [(rm.BER_UNCODED, "$Q=7.03$ ($10^{-12}$)"),
                   (rm.BER_KP4_PRE, "$Q=3.49$ (KP4)")]:
        qv = float(rm.ber_to_q(b))
        ax.axhline(qv, color="k", lw=0.7, ls=":")
        ax.text(-159.5, qv * 1.05, txt, fontsize=7)

    ax.set_xlabel("Relative intensity noise [dB/Hz]")
    ax.set_ylabel("Max achievable $Q$ (RIN floor)")
    ax.set_ylim(1, 300)
    ax.set_xlim(-160, -125)
    ax.set_title("Laser RIN caps link quality: $Q_{\\max}=1/\\sqrt{\\mathrm{RIN}\\cdot BW}$")
    ax.legend(loc="upper right", framealpha=0.9)
    save(fig, "fig_rin_floor.pdf")


# ---------------------------------------------------------------------------
def fig_noise_density_vs_power():
    """Noise current densities vs received power: why RIN needs an operating point.

    Thermal is flat, shot grows as sqrt(I), RIN grows as I. So RIN only overtakes
    the fixed thermal/shot floors above a break-in power that depends on the laser.
    """
    R = 0.8                       # A/W
    i_th_density = 25e-12         # A/rtHz, representative high-speed TIA
    p_dbm = np.linspace(-20, 6, 400)
    i_photo = R * rm.dbm_to_w(p_dbm)

    fig, ax = plt.subplots(figsize=(4.6, 3.2))

    ax.axhline(i_th_density * 1e12, color=GREY, lw=1.5, ls="--",
               label="thermal (TIA, ~25 pA/$\\sqrt{\\mathrm{Hz}}$)")
    ax.semilogy(p_dbm, rm.shot_noise_density(i_photo) * 1e12, color=ORANGE,
                lw=1.5, label="shot $\\sqrt{2qI}$")
    for rin_db, col in [(-145.0, BLUE), (-155.0, GREEN)]:
        ax.semilogy(p_dbm, rm.rin_noise_density(i_photo, rin_db) * 1e12, color=col,
                    lw=1.6, label=f"RIN {rin_db:.0f} dB/Hz")

    ax.axvline(0.0, color="k", lw=0.6, ls=":")
    ax.text(0.2, 1.4, "0 dBm", fontsize=7, rotation=90, va="bottom")

    ax.set_xlabel("Average received power [dBm]  ($I = \\mathcal{R}P$, $\\mathcal{R}=0.8$ A/W)")
    ax.set_ylabel("Noise current density [pA/$\\sqrt{\\mathrm{Hz}}$]")
    ax.set_ylim(1, 300)
    ax.set_xlim(-20, 6)
    ax.set_title("RIN needs a power: thermal flat, shot $\\propto\\!\\sqrt{I}$, RIN $\\propto\\!I$")
    ax.legend(loc="upper left", framealpha=0.9)
    save(fig, "fig_noise_density_vs_power.pdf")


# ---------------------------------------------------------------------------
def fig_trace_loss():
    """PCB trace insertion loss vs length: why reach halves from 112G to 224G.

    Loss per inch is taken at each rate's Nyquist (28 GHz for 112G, 56 GHz for
    224G) for good low-loss stripline; the 224G cases use skip-layer and regular
    routing (IEEE 802.3df 224G PCB study: ~1.9 and ~2.8 dB/inch at 56 GHz).
    """
    L_in = np.linspace(0, 16, 200)
    cases = [
        (1.0, "112G @ 28 GHz (low-loss SL)", BLUE),
        (1.9, "224G @ 56 GHz (skip-layer)", GREEN),
        (2.8, "224G @ 56 GHz (regular SL)", RED),
    ]
    budget = 10.0  # dB, representative PCB-trace share of a VSR host channel

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for slope, label, col in cases:
        ax.plot(L_in, slope * L_in, color=col, lw=1.6, label=label)
        reach = budget / slope
        ax.plot(reach, budget, "o", color=col, ms=4)
        ax.annotate(f"{reach:.1f}\"", (reach, budget), textcoords="offset points",
                    xytext=(3, -10), fontsize=7, color=col)

    ax.axhline(budget, color=GREY, lw=0.9, ls="--")
    ax.text(0.2, budget + 0.4, "$\\approx$ PCB-trace budget (VSR host)", fontsize=7,
            color=GREY)

    ax.set_xlabel("PCB trace length [inch]  (1 in = 25.4 mm)")
    ax.set_ylabel("Trace insertion loss [dB]")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 30)
    ax.set_title("Doubling the baud rate halves the copper reach")
    ax.legend(loc="upper right", framealpha=0.9)
    save(fig, "fig_trace_loss.pdf")


# ---------------------------------------------------------------------------
def fig_nrz_vs_pam4():
    """NRZ vs PAM4 BER at a fixed 100 Gb/s information rate."""
    R = 0.8
    i_dens = 25e-12  # A/rtHz
    er_db = 6.0

    bw_nrz = 0.66 * 100e9    # 100 GBaud NRZ
    bw_pam4 = 0.66 * 50e9    # 50 GBaud PAM4 (2 bits/symbol)

    p_dbm = np.linspace(-10, 6, 400)
    p_w = rm.dbm_to_w(p_dbm)

    ber_nrz = rm.nrz_ber(p_w, responsivity=R, i_thermal_rms=i_dens * np.sqrt(bw_nrz),
                         bw=bw_nrz, er_db=er_db)
    ber_pam4 = rm.pam4_ber(p_w, responsivity=R, i_thermal_rms=i_dens * np.sqrt(bw_pam4),
                           bw=bw_pam4, er_db=er_db)

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.semilogy(p_dbm, np.clip(ber_nrz, 1e-20, 0.5), color=BLUE, lw=1.5,
                label="NRZ, 100 GBaud")
    ax.semilogy(p_dbm, np.clip(ber_pam4, 1e-20, 0.5), color=RED, lw=1.5,
                label="PAM4, 50 GBaud")

    ax.axhline(rm.BER_KP4_PRE, color=GREEN, lw=0.8, ls=":")
    ax.text(-9.5, rm.BER_KP4_PRE * 1.5, "KP4 pre-FEC $2.4\\times10^{-4}$",
            fontsize=7, color=GREEN)

    ax.set_xlabel("Average received power [dBm]")
    ax.set_ylabel("Bit-error ratio")
    ax.set_ylim(1e-20, 0.5)
    ax.set_xlim(-10, 6)
    ax.set_title("Same 100 Gb/s: PAM4's level penalty vs. NRZ's bandwidth cost")
    ax.legend(loc="upper right", framealpha=0.9)
    save(fig, "fig_nrz_vs_pam4.pdf")


# ---------------------------------------------------------------------------
# Light palette for block diagrams (448G paths figure)
LIGHT_BLUE = "#d6e4f0"
LIGHT_GREEN = "#dce8dc"
LIGHT_ORANGE = "#fae8d4"
LIGHT_RED = "#f5dede"
LIGHT_GREY = "#ececec"
LIGHT_PINK = "#f8e8e8"
EDGE = "#8a8a8a"
TEXT_DARK = "#2a2a2a"
TEXT_MID = "#4a4a4a"
ACCENT_BLUE = "#4a7ba7"
ACCENT_GREEN = "#5a8f5a"
ACCENT_RED = "#b85c5c"
ACCENT_ORANGE = "#c4843a"


def fig_448g_paths():
    """Three 448G/lane architectures: baud rates at each hop (pluggable vs CPO)."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, axes = plt.subplots(3, 1, figsize=(6.4, 7.0))
    fig.subplots_adjust(hspace=0.78, left=0.04, right=0.98, top=0.93, bottom=0.02)

    y_block = 0.56
    block_h = 0.52

    def row_layout(n_blocks):
        margin, gap = 0.02, 0.045
        total_gap = gap * (n_blocks - 1)
        block_w = (1.0 - 2 * margin - total_gap) / n_blocks
        xs = [margin + i * (block_w + gap) for i in range(n_blocks)]
        return xs, block_w

    def draw_block(ax, x, block_w, label, rate, facecolor, hatch=None):
        box = FancyBboxPatch(
            (x, y_block - block_h / 2), block_w, block_h,
            boxstyle="round,pad=0.014,rounding_size=0.018",
            linewidth=0.8, edgecolor=EDGE, facecolor=facecolor,
            hatch=hatch, transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(box)
        ax.text(
            x + block_w / 2, y_block + 0.10, label,
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=TEXT_DARK, linespacing=1.15, transform=ax.transAxes,
        )
        ax.text(
            x + block_w / 2, y_block - 0.14, rate,
            ha="center", va="center", fontsize=8.5, color=TEXT_MID,
            linespacing=1.15, transform=ax.transAxes,
        )

    def draw_arrow(ax, x0, block_w0, x1, label=None, color=TEXT_MID):
        y = y_block
        arr = FancyArrowPatch(
            (x0 + block_w0, y), (x1, y),
            arrowstyle="-|>", mutation_scale=10, linewidth=1.0,
            color=EDGE, transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(arr)
        if label:
            mx = (x0 + block_w0 + x1) / 2
            y_lbl = y_block - block_h / 2 - 0.06
            ax.text(
                mx, y_lbl, label, ha="center", va="top", fontsize=8.5,
                color=color, linespacing=1.1, transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="none", alpha=0.85),
            )

    def setup_ax(ax, title, footnote):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(
            0.0, 0.97, title, ha="left", va="top",
            fontsize=10, fontweight="bold", color=TEXT_DARK,
            transform=ax.transAxes,
        )
        ax.text(
            0.50, 0.02, footnote, ha="center", va="bottom",
            fontsize=7.8, color=TEXT_MID, transform=ax.transAxes,
        )

    # (A) Native aligned pluggable — connector is the gate
    ax = axes[0]
    xs, bw = row_layout(5)
    setup_ax(
        ax,
        "(A) Pluggable, aligned PAM4 (LPO/retimed target)",
        "Needs connector BW past 112 GHz Nyquist; otherwise path (B) or CPO",
    )
    draw_block(ax, xs[0], bw, "Switch\nSerDes", "448G PAM4\n224 GBd", LIGHT_BLUE)
    draw_arrow(ax, xs[0], bw, xs[1], "PCB +\nconnector", ACCENT_RED)
    draw_block(
        ax, xs[1], bw, "Connector\n(VSR)", "$f_N\\!\\approx\\!90$ GHz\nlimit",
        LIGHT_PINK, hatch="///",
    )
    draw_arrow(ax, xs[1], bw, xs[2])
    draw_block(ax, xs[2], bw, "Module\n(LPO/retimer)", "448G PAM4\n224 GBd", LIGHT_GREEN)
    draw_arrow(ax, xs[2], bw, xs[3])
    draw_block(ax, xs[3], bw, "Driver +\nmodulator", "224 GBd\nPAM4", LIGHT_ORANGE)
    draw_arrow(ax, xs[3], bw, xs[4])
    draw_block(ax, xs[4], bw, "Fiber", "448G/$\\lambda$", LIGHT_GREY)

    # (B) Electrical PAM6 + gearbox — fits 90 GHz channel
    ax = axes[1]
    xs, bw = row_layout(5)
    setup_ax(
        ax,
        "(B) Pluggable, PAM6 electrical + gearbox (fallback)",
        "Breaks LPO; adds power, latency, and module silicon",
    )
    draw_block(ax, xs[0], bw, "Switch\nSerDes", "448G PAM6\n173 GBd", LIGHT_BLUE)
    draw_arrow(ax, xs[0], bw, xs[1], "fits\n90 GHz", ACCENT_GREEN)
    draw_block(ax, xs[1], bw, "Connector\n(VSR)", "173 GBd\nPAM6", LIGHT_GREEN)
    draw_arrow(ax, xs[1], bw, xs[2])
    draw_block(ax, xs[2], bw, "Gearbox +\nDSP", "173 $\\rightarrow$\n224 GBd", LIGHT_RED)
    draw_arrow(ax, xs[2], bw, xs[3])
    draw_block(ax, xs[3], bw, "Driver +\nmodulator", "224 GBd\nPAM4", LIGHT_ORANGE)
    draw_arrow(ax, xs[3], bw, xs[4])
    draw_block(ax, xs[4], bw, "Fiber", "448G/$\\lambda$", LIGHT_GREY)

    # (C) CPO — bypass connector
    ax = axes[2]
    xs, bw = row_layout(4)
    setup_ax(
        ax,
        "(C) CPO: aligned PAM4 (no pluggable connector in path)",
        "Transition modules (not shown): $2\\times$224G host lanes "
        "$\\rightarrow$ gearbox $\\rightarrow$ 448G optical",
    )
    draw_block(ax, xs[0], bw, "Switch\nSerDes", "448G PAM4\n224 GBd", LIGHT_BLUE)
    draw_arrow(ax, xs[0], bw, xs[1], "mm-scale\npackage", ACCENT_GREEN)
    draw_block(ax, xs[1], bw, "Die-to-OE\nlink", "224 GBd\nPAM4", LIGHT_GREEN)
    draw_arrow(ax, xs[1], bw, xs[2])
    draw_block(ax, xs[2], bw, "Optical\nengine", "224 GBd\nPAM4", LIGHT_ORANGE)
    draw_arrow(ax, xs[2], bw, xs[3])
    draw_block(ax, xs[3], bw, "Fiber", "448G/$\\lambda$", LIGHT_GREY)

    fig.suptitle(
        "448G/lane: electrical vs optical baud at each hop",
        fontsize=11, fontweight="bold", color=TEXT_DARK, y=0.995,
    )
    save(fig, "fig_448g_paths.pdf")


def fig_eq_chains():
    """Equalizer chains: generic SerDes EQ, retimed module, LPO."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, axes = plt.subplots(3, 1, figsize=(6.4, 6.6))
    fig.subplots_adjust(hspace=0.72, left=0.02, right=0.98, top=0.92, bottom=0.02)

    y_block = 0.54
    block_h = 0.50

    def row_layout(n_blocks):
        margin, gap = 0.015, 0.028
        total_gap = gap * (n_blocks - 1)
        block_w = (1.0 - 2 * margin - total_gap) / n_blocks
        xs = [margin + i * (block_w + gap) for i in range(n_blocks)]
        return xs, block_w

    def draw_block(ax, x, block_w, label, sub, facecolor, hatch=None, fs=8.5, sub_fs=7.2):
        box = FancyBboxPatch(
            (x, y_block - block_h / 2), block_w, block_h,
            boxstyle="round,pad=0.012,rounding_size=0.016",
            linewidth=0.8, edgecolor=EDGE, facecolor=facecolor,
            hatch=hatch, transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(box)
        ax.text(
            x + block_w / 2, y_block + (0.08 if sub else 0), label,
            ha="center", va="center", fontsize=fs, fontweight="bold",
            color=TEXT_DARK, linespacing=1.1, transform=ax.transAxes,
        )
        if sub:
            ax.text(
                x + block_w / 2, y_block - 0.13, sub,
                ha="center", va="center", fontsize=sub_fs, color=TEXT_MID,
                linespacing=1.1, transform=ax.transAxes,
            )

    def draw_arrow(ax, x0, block_w0, x1):
        arr = FancyArrowPatch(
            (x0 + block_w0, y_block), (x1, y_block),
            arrowstyle="-|>", mutation_scale=9, linewidth=1.0,
            color=EDGE, transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(arr)

    def setup_ax(ax, title, footnote):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(
            0.0, 0.97, title, ha="left", va="top",
            fontsize=9.5, fontweight="bold", color=TEXT_DARK,
            transform=ax.transAxes,
        )
        ax.text(
            0.50, 0.02, footnote, ha="center", va="bottom",
            fontsize=7.4, color=TEXT_MID, transform=ax.transAxes,
        )

    # (A) Most correct generic SerDes EQ stack
    ax = axes[0]
    xs, bw = row_layout(6)
    setup_ax(
        ax,
        "(A) Correct SerDes EQ order (one electrical lane)",
        "FFE is Tx and Rx. Linear stages first; DFE last. Mild channels may drop DFE.",
    )
    draw_block(ax, xs[0], bw, "Tx FFE", "pre-emphasis", LIGHT_BLUE)
    draw_arrow(ax, xs[0], bw, xs[1])
    draw_block(ax, xs[1], bw, "Channel", "trace / conn\n/ cable", LIGHT_GREY)
    draw_arrow(ax, xs[1], bw, xs[2])
    draw_block(ax, xs[2], bw, "CTLE", "analog HF\nboost", LIGHT_GREEN)
    draw_arrow(ax, xs[2], bw, xs[3])
    draw_block(ax, xs[3], bw, "Rx FFE", "linear FIR\n(TDECQ ref)", LIGHT_ORANGE)
    draw_arrow(ax, xs[3], bw, xs[4])
    draw_block(ax, xs[4], bw, "DFE", "post-cursor\ncancel", LIGHT_RED)
    draw_arrow(ax, xs[4], bw, xs[5])
    draw_block(ax, xs[5], bw, "Slicer\n+ CDR", "sample +\nretimed", LIGHT_PINK)

    # (B) Fully retimed pluggable
    ax = axes[1]
    xs, bw = row_layout(6)
    setup_ax(
        ax,
        "(B) Fully retimed pluggable (module owns heavy EQ)",
        "Module DSP includes FFE/DFE/CDR both sides of the optics.",
    )
    draw_block(ax, xs[0], bw, "Host\nSerDes", "EQ + FEC", LIGHT_BLUE)
    draw_arrow(ax, xs[0], bw, xs[1])
    draw_block(ax, xs[1], bw, "Connector", "VSR/MR", LIGHT_GREY)
    draw_arrow(ax, xs[1], bw, xs[2])
    draw_block(ax, xs[2], bw, "Module\nDSP", "FFE/DFE\n+ CDR", LIGHT_GREEN)
    draw_arrow(ax, xs[2], bw, xs[3])
    draw_block(ax, xs[3], bw, "Optics", "drv/mod\n+ PD/TIA", LIGHT_ORANGE)
    draw_arrow(ax, xs[3], bw, xs[4])
    draw_block(ax, xs[4], bw, "Module\nDSP", "FFE/DFE\n+ CDR", LIGHT_GREEN)
    draw_arrow(ax, xs[4], bw, xs[5])
    draw_block(ax, xs[5], bw, "Host\nSerDes", "EQ + FEC", LIGHT_BLUE)

    # (C) LPO — simplest product chain that still closes
    ax = axes[2]
    xs, bw = row_layout(6)
    setup_ax(
        ax,
        "(C) LPO (simplest module; host carries the EQ)",
        "No module DSP/CDR. Optional TIA CTLE only. Host SerDes must close (A).",
    )
    draw_block(ax, xs[0], bw, "Host\nSerDes", "full EQ\n+ FEC", LIGHT_BLUE)
    draw_arrow(ax, xs[0], bw, xs[1])
    draw_block(ax, xs[1], bw, "Linear\ndriver", "no DSP", LIGHT_ORANGE)
    draw_arrow(ax, xs[1], bw, xs[2])
    draw_block(ax, xs[2], bw, "Optics", "modulator\n+ fiber", LIGHT_GREY)
    draw_arrow(ax, xs[2], bw, xs[3])
    draw_block(ax, xs[3], bw, "PD +\nTIA", "optional\nCTLE", LIGHT_GREEN)
    draw_arrow(ax, xs[3], bw, xs[4])
    draw_block(
        ax, xs[4], bw, "Host\nSerDes", "CTLE+FFE\n+DFE+CDR", LIGHT_BLUE, hatch="///",
    )
    draw_arrow(ax, xs[4], bw, xs[5])
    draw_block(ax, xs[5], bw, "FEC", "KP4\ndecode", LIGHT_PINK)

    fig.suptitle(
        "Equalization chains: correct order, retimed module, LPO",
        fontsize=11, fontweight="bold", color=TEXT_DARK, y=0.995,
    )
    save(fig, "fig_eq_chains.pdf")


def fig_oif_448g_package():
    """OIF-style packaging map: CPC, CPO, and faceplate pluggables (redrawn)."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    PCB = "#dce8dc"
    PKG = "#b8cfc0"
    IC = "#d0d0d0"
    COPPER = "#c4843a"
    OPTIC = "#4a7ba7"
    EDGE_D = "#5a5a5a"

    def box(x, y, w, h, fc, ec=EDGE_D, lw=1.0, rs=0.012, z=1):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.006,rounding_size={rs}",
            linewidth=lw, edgecolor=ec, facecolor=fc,
            transform=ax.transAxes, clip_on=False, zorder=z,
        ))

    def label(x, y, text, fs=8, bold=False, color=TEXT_DARK, ha="center", va="center"):
        ax.text(x, y, text, ha=ha, va=va, fontsize=fs,
                fontweight="bold" if bold else "normal", color=color,
                transform=ax.transAxes, zorder=5, linespacing=1.15)

    def cable(x0, y0, x1, y1, color=COPPER, lw=1.6):
        ax.plot([x0, x1], [y0, y1], color=color, lw=lw,
                solid_capstyle="round", transform=ax.transAxes, zorder=3)

    # Nested containers
    box(0.04, 0.20, 0.82, 0.70, PCB, lw=1.2, rs=0.02, z=1)
    label(0.07, 0.86, "Host PCB", fs=9, bold=True, ha="left")

    box(0.20, 0.36, 0.40, 0.44, PKG, lw=1.1, rs=0.018, z=2)
    label(0.22, 0.76, "Package", fs=8.5, bold=True, ha="left")

    box(0.32, 0.48, 0.16, 0.16, IC, lw=1.0, rs=0.014, z=3)
    label(0.40, 0.56, "Host IC", fs=9, bold=True)

    # Left: CPC -> electrical CONN -> copper
    box(0.22, 0.40, 0.09, 0.09, LIGHT_ORANGE, z=3)
    label(0.265, 0.445, "CPC", fs=8, bold=True)
    cable(0.40, 0.48, 0.31, 0.445, COPPER, lw=1.2)
    cable(0.22, 0.445, 0.14, 0.445, COPPER)
    box(0.06, 0.40, 0.08, 0.09, LIGHT_GREY, z=3)
    label(0.10, 0.445, "Electrical\nCONN", fs=6.5)
    cable(0.06, 0.445, 0.005, 0.445, COPPER, lw=2.0)
    label(0.005, 0.51, "Copper\ncable", fs=6.5, color=COPPER, ha="left")

    # CPO: Optical Engine -> Optical CONN
    box(0.48, 0.64, 0.10, 0.11, LIGHT_BLUE, z=3)
    label(0.53, 0.695, "Optical\nEngine", fs=7, bold=True)
    label(0.53, 0.63, "CPO", fs=6.5, color=OPTIC)
    cable(0.48, 0.56, 0.48, 0.64, OPTIC, lw=1.2)
    cable(0.48, 0.64, 0.48, 0.695, OPTIC, lw=0.8)
    cable(0.58, 0.695, 0.70, 0.695, OPTIC)
    box(0.70, 0.65, 0.11, 0.09, LIGHT_GREY, z=3)
    label(0.755, 0.695, "Optical\nCONN", fs=6.5)
    cable(0.81, 0.695, 0.92, 0.695, OPTIC, lw=2.0)
    label(0.93, 0.695, "Optical\nfiber", fs=6.5, color=OPTIC, ha="left")

    # Right CPC feeding pluggables
    box(0.48, 0.44, 0.09, 0.09, LIGHT_ORANGE, z=3)
    label(0.525, 0.485, "CPC", fs=8, bold=True)
    cable(0.48, 0.56, 0.48, 0.53, COPPER, lw=1.2)
    cable(0.48, 0.53, 0.48, 0.485, COPPER, lw=1.0)

    plugs = [
        (0.64, 0.50, "Pluggable\nRetimed Optics", LIGHT_GREEN, OPTIC, "fiber"),
        (0.64, 0.36, "Pluggable\nLPO / LRO", LIGHT_PINK, OPTIC, "fiber"),
        (0.64, 0.24, "Pluggable\nAEC / DAC", LIGHT_ORANGE, COPPER, "copper"),
    ]
    for (x, y, name, fc, media_c, media_lbl) in plugs:
        box(x, y, 0.15, 0.10, fc, z=3)
        label(x + 0.075, y + 0.05, name, fs=6.5, bold=True)
        cable(0.57, 0.485, x, y + 0.05, COPPER, lw=1.2)
        cable(x + 0.15, y + 0.05, 0.88, y + 0.05, media_c, lw=1.7)
        label(0.89, y + 0.05, media_lbl, fs=6.5, color=media_c, ha="left")

    # Legend
    box(0.04, 0.02, 0.92, 0.14, "#f7f7f7", lw=0.7, rs=0.01, z=1)
    legend = (
        "CPC: co-packaged copper   |   CPO: co-packaged optics   |   "
        "LPO/LRO: linear / linear-receive pluggable\n"
        "DAC: direct-attach copper   |   AEC: active electrical cable   |   "
        "Redrawn from OIF CEI-448G packaging map"
    )
    label(0.50, 0.09, legend, fs=6.6, color=TEXT_MID)

    label(0.50, 0.965, "CEI-448G packaging map: where the SerDes stops",
          fs=10.5, bold=True)

    save(fig, "fig_oif_448g_package.pdf")


def fig_cei_reach_map():
    """OIF CEI reach map on a host PCB: XSR/XSR+, VSR, MR, LR (redrawn)."""
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(6.8, 5.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    PCB = "#c8dcc8"
    ASIC = "#c9b8d4"
    CORE = "#c45c5c"
    OPT_PORT = "#e8c96a"
    MOD = "#d8dde3"
    EDGE = "#4a4a4a"
    TRACE = "#2a2a2a"
    TWINAX = "#1a1a1a"
    FIBER = "#5aa0c4"
    XSR_C = "#d97800"
    DIV = "#3d6f9a"

    def box(x, y, w, h, fc, ec=EDGE, lw=1.0, rs=0.01, z=2):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0.004,rounding_size={rs}",
            linewidth=lw, edgecolor=ec, facecolor=fc,
            transform=ax.transAxes, clip_on=False, zorder=z,
        ))

    def txt(x, y, s, fs=8, bold=False, c=TEXT_DARK, ha="center", va="center"):
        ax.text(x, y, s, ha=ha, va=va, fontsize=fs,
                fontweight="bold" if bold else "normal", color=c,
                transform=ax.transAxes, zorder=6, linespacing=1.05)

    def line(xs, ys, color=TRACE, lw=1.4, z=3):
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
                transform=ax.transAxes, zorder=z)

    # Title
    txt(0.50, 0.975, "CEI reach map: where each electrical class lives",
        fs=10.5, bold=True)

    # Backplane zone
    txt(0.50, 0.935, '"backplane" applications', fs=8, bold=True, c=DIV)
    ax.plot([0.05, 0.95], [0.915, 0.915], color=DIV, lw=1.0, ls="--",
            transform=ax.transAxes, zorder=1)

    # Host PCB (middle band)
    box(0.05, 0.28, 0.90, 0.60, PCB, lw=1.35, rs=0.014, z=1)
    txt(0.07, 0.84, "Host PCB", fs=9, bold=True, ha="left")

    # Left ASIC package + die + OE ports
    box(0.16, 0.42, 0.30, 0.34, ASIC, lw=1.1, rs=0.012, z=2)
    box(0.24, 0.52, 0.11, 0.12, CORE, lw=0.8, rs=0.008, z=3)
    txt(0.295, 0.58, "ASIC /\nFPGA", fs=7.2, bold=True, c="white")
    box(0.38, 0.66, 0.055, 0.055, OPT_PORT, lw=0.7, rs=0.004, z=3)  # top OE
    box(0.38, 0.45, 0.055, 0.055, OPT_PORT, lw=0.7, rs=0.004, z=3)  # bottom OE
    box(0.175, 0.45, 0.055, 0.055, OPT_PORT, lw=0.7, rs=0.004, z=3)  # left OE

    # Right ASIC
    box(0.60, 0.46, 0.24, 0.26, ASIC, lw=1.1, rs=0.012, z=2)
    box(0.66, 0.52, 0.11, 0.12, CORE, lw=0.8, rs=0.008, z=3)
    txt(0.715, 0.58, "ASIC /\nFPGA", fs=7.2, bold=True, c="white")

    # --- Backplane connectors (above PCB) ---
    box(0.20, 0.885, 0.07, 0.04, MOD, lw=0.8, rs=0.004, z=4)
    box(0.42, 0.885, 0.07, 0.04, MOD, lw=0.8, rs=0.004, z=4)
    box(0.72, 0.885, 0.07, 0.04, MOD, lw=0.8, rs=0.004, z=4)

    # PCB traces up to left backplane
    line([0.25, 0.235], [0.76, 0.885], TRACE, lw=1.25)
    txt(0.16, 0.82, "Host PCB\nTraces", fs=6.0, c=TEXT_MID, ha="right")

    # Twinax LR to center backplane
    line([0.36, 0.455], [0.76, 0.885], TWINAX, lw=2.5)
    txt(0.48, 0.83, "Twinax\nCopper", fs=6.0, c=TEXT_MID, ha="left")
    txt(0.40, 0.78, "LR", fs=8, bold=True)

    # Fiber from top OE to right backplane
    line([0.407, 0.407, 0.755], [0.715, 0.80, 0.885], FIBER, lw=1.7)
    txt(0.58, 0.855, "Optical Fiber", fs=6.3, c=FIBER)

    # --- Chip-to-chip MR ---
    line([0.46, 0.60], [0.58, 0.58], TRACE, lw=1.35)
    txt(0.53, 0.605, "MR", fs=8, bold=True)
    txt(0.53, 0.555, "PCB Traces", fs=5.8, c=TEXT_MID)

    line([0.46, 0.60], [0.50, 0.50], TWINAX, lw=2.3)
    txt(0.53, 0.475, "Twinax Copper", fs=5.7, c=TEXT_MID)

    line([0.435, 0.72, 0.72], [0.688, 0.688, 0.72], FIBER, lw=1.55)
    txt(0.58, 0.712, "Optical Fiber", fs=6.0, c=FIBER)
    txt(0.58, 0.685, "MR", fs=7.5, bold=True, c=FIBER)

    # --- XSR / XSR+ inside left package ---
    line([0.35, 0.38], [0.58, 0.687], XSR_C, lw=1.45)
    line([0.35, 0.38], [0.58, 0.477], XSR_C, lw=1.45)
    txt(0.33, 0.63, "XSR", fs=7.5, bold=True, c=XSR_C, ha="right")
    line([0.295, 0.23], [0.52, 0.477], XSR_C, lw=1.35)
    txt(0.23, 0.505, "XSR+", fs=7, bold=True, c=XSR_C, ha="right")

    # Faceplate divider (below PCB)
    ax.plot([0.05, 0.95], [0.255, 0.255], color=DIV, lw=1.0, ls="--",
            transform=ax.transAxes, zorder=1)
    txt(0.50, 0.215, '"faceplate" applications', fs=8, bold=True, c=DIV)

    # Faceplate modules
    box(0.08, 0.045, 0.14, 0.085, MOD, lw=0.85, rs=0.006, z=4)
    txt(0.15, 0.087, "Active and\npassive copper", fs=5.8)

    box(0.30, 0.045, 0.09, 0.085, MOD, lw=0.85, rs=0.006, z=4)

    box(0.48, 0.045, 0.12, 0.085, "#e6d9b8", lw=0.85, rs=0.006, z=4)
    txt(0.54, 0.087, "Optical\nModule", fs=6.2, bold=True)

    box(0.70, 0.045, 0.12, 0.085, "#e6d9b8", lw=0.85, rs=0.006, z=4)
    txt(0.76, 0.087, "Optical\nModule", fs=6.2, bold=True)

    # LR twinax to faceplate copper
    line([0.20, 0.15], [0.42, 0.13], TWINAX, lw=2.4)
    txt(0.10, 0.34, "LR", fs=8, bold=True, ha="right")
    txt(0.10, 0.30, "Twinax", fs=5.8, c=TEXT_MID, ha="right")

    # VSR PCB traces to faceplate cage (label stays inside PCB)
    line([0.295, 0.345], [0.42, 0.13], TRACE, lw=1.3)
    txt(0.37, 0.36, "VSR", fs=8, bold=True)
    txt(0.37, 0.315, "Host PCB Traces", fs=5.7, c=TEXT_MID)

    # XSR path to left optical module (near-package / CPO style)
    line([0.407, 0.54], [0.45, 0.13], XSR_C, lw=1.7)
    txt(0.49, 0.34, "Optical Module", fs=5.8, c=XSR_C, ha="right")

    # Fiber to right optical module
    line([0.407, 0.58, 0.76], [0.45, 0.32, 0.13], FIBER, lw=1.55)
    txt(0.66, 0.34, "Optical Fiber", fs=6.0, c=FIBER)

    # Legend
    box(0.05, 0.002, 0.90, 0.035, "#f3f3f3", lw=0.55, rs=0.006, z=1)
    txt(0.50, 0.019,
        "XSR/XSR+: in-package die-to-die / die-to-OE   |   "
        "VSR: chip-to-module   |   MR: chip-to-chip   |   LR: backplane / DAC",
        fs=6.0, c=TEXT_MID)

    save(fig, "fig_cei_reach_map.pdf")


def fig_scale_up_node():
    """One AI compute node: scale-up fabric vs scale-out NICs (schematic)."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    LIGHT_PURPLE = "#e8dff0"
    SWITCH_BLUE = "#b8cce4"
    SCALEUP_LINE = "#b85c5c"
    SCALEOUT_LINE = "#4a7ba7"
    INTERNAL_LINE = "#b89840"

    def round_box(cx, cy, w, h, label, sub="", fc=LIGHT_GREY, fs=9.5, sub_fs=7.5):
        x, y = cx - w / 2, cy - h / 2
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.012,rounding_size=0.015",
            linewidth=0.9, edgecolor=EDGE, facecolor=fc,
            transform=ax.transAxes, clip_on=False, zorder=3,
        ))
        ax.text(cx, cy + (0.012 if sub else 0), label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=TEXT_DARK,
                transform=ax.transAxes, zorder=4)
        if sub:
            ax.text(cx, cy - 0.028, sub, ha="center", va="center",
                    fontsize=sub_fs, color=TEXT_MID, transform=ax.transAxes, zorder=4)

    def line(x0, y0, x1, y1, color, lw=1.6, style="-", zorder=2, alpha=1.0):
        ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=style,
                solid_capstyle="round", transform=ax.transAxes, zorder=zorder, alpha=alpha)

    def bi_arrow(x0, y0, x1, y1, color=INTERNAL_LINE):
        arr = FancyArrowPatch(
            (x0, y0), (x1, y1), arrowstyle="<->", mutation_scale=9,
            linewidth=1.2, color=color, transform=ax.transAxes,
            clip_on=False, zorder=2,
        )
        ax.add_patch(arr)

    # Stacked-node hint (cluster continues)
    for dx, dy, alpha in ((0.028, -0.022, 0.22), (0.056, -0.044, 0.12)):
        ax.add_patch(FancyBboxPatch(
            (0.07 + dx, 0.11 + dy), 0.86, 0.80,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=0.7, edgecolor=EDGE, facecolor="none",
            linestyle="--", transform=ax.transAxes, clip_on=False,
            zorder=0, alpha=alpha,
        ))

    # Compute node outline
    ax.add_patch(FancyBboxPatch(
        (0.07, 0.11), 0.86, 0.80,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=1.1, edgecolor=EDGE, facecolor="white",
        transform=ax.transAxes, clip_on=False, zorder=1,
    ))
    ax.text(0.09, 0.87, "Compute node", ha="left", va="top",
            fontsize=8.5, color=TEXT_MID, transform=ax.transAxes, zorder=5)
    ax.text(0.91, 0.13, "$\\cdots$", ha="right", va="bottom",
            fontsize=14, color=TEXT_MID, transform=ax.transAxes, zorder=5)

    # Scale-up switches (top)
    sw_y, sw_w, sw_h = 0.78, 0.13, 0.07
    sw_xs = [0.24, 0.41, 0.59, 0.76]
    for sx in sw_xs:
        round_box(sx, sw_y, sw_w, sw_h, "Scale-up", "switch", SWITCH_BLUE, fs=8, sub_fs=6.5)
    ax.text(0.50, sw_y, "$\\cdots$", ha="center", va="center",
            fontsize=11, color=TEXT_MID, transform=ax.transAxes, zorder=4)

    # Accelerators, CPU, NICs
    acc_y, acc_w, acc_h = 0.56, 0.20, 0.12
    acc1_x, acc2_x = 0.30, 0.70
    round_box(acc1_x, acc_y, acc_w, acc_h, "Accelerator", "(GPU / XPU)", LIGHT_GREEN)
    round_box(acc2_x, acc_y, acc_w, acc_h, "Accelerator", "(GPU / XPU)", LIGHT_GREEN)

    round_box(0.50, 0.40, 0.16, 0.09, "CPU", "host", LIGHT_PINK, fs=9)

    nic_w, nic_h = 0.17, 0.08
    round_box(acc1_x, 0.28, nic_w, nic_h, "Scale-out", "NIC", LIGHT_BLUE, fs=8.5, sub_fs=7)
    round_box(acc2_x, 0.28, nic_w, nic_h, "Scale-out", "NIC", LIGHT_BLUE, fs=8.5, sub_fs=7)
    round_box(0.50, 0.19, 0.17, 0.07, "Front-end", "NIC", LIGHT_PURPLE, fs=8.5, sub_fs=7)

    # Scale-up fabric (red): accelerator tops to nearest switches
    for ax_x in (acc1_x, acc2_x):
        line(ax_x, acc_y + acc_h / 2, ax_x, sw_y - sw_h / 2, SCALEUP_LINE, lw=2.0)
    line(acc1_x, acc_y + acc_h / 2 + 0.02, acc2_x, acc_y + acc_h / 2 + 0.02,
         SCALEUP_LINE, lw=1.4, alpha=0.55)

    # In-node links (gold)
    bi_arrow(acc1_x + acc_w / 2 - 0.01, acc_y, acc2_x - acc_w / 2 + 0.01, acc_y)
    bi_arrow(acc1_x, acc_y - acc_h / 2, acc1_x, 0.28 + nic_h / 2)
    bi_arrow(acc2_x, acc_y - acc_h / 2, acc2_x, 0.28 + nic_h / 2)
    bi_arrow(acc1_x + 0.04, acc_y - 0.02, 0.50 - 0.06, 0.40 + 0.03)
    bi_arrow(acc2_x - 0.04, acc_y - 0.02, 0.50 + 0.06, 0.40 + 0.03)
    bi_arrow(0.50, 0.40 - 0.09 / 2, 0.50, 0.19 + 0.07 / 2)

    # Scale-out fabric (blue): NICs to cluster network below node
    ax.add_patch(FancyBboxPatch(
        (0.05, 0.02), 0.90, 0.06,
        boxstyle="round,pad=0.01,rounding_size=0.012",
        linewidth=0.8, edgecolor=SCALEOUT_LINE, facecolor="#eef4fa",
        transform=ax.transAxes, clip_on=False, zorder=1,
    ))
    ax.text(0.50, 0.05, "Scale-out fabric (Ethernet / InfiniBand, rack-to-rack)",
            ha="center", va="center", fontsize=8.5, color=SCALEOUT_LINE,
            transform=ax.transAxes, zorder=4)
    for nx in (acc1_x, acc2_x):
        line(nx, 0.28 - nic_h / 2, nx, 0.08, SCALEOUT_LINE, lw=2.0)

    # Front-end path (purple, side)
    line(0.50 + 0.17 / 2, 0.19, 0.93, 0.19, "#7a5a9a", lw=1.5, style="--")
    ax.text(0.945, 0.19, "Mgmt /\nstorage", ha="left", va="center", fontsize=7.5,
            color="#7a5a9a", transform=ax.transAxes, linespacing=1.1)

    # Legend
    leg_y = 0.935
    for dx, (col, txt) in enumerate([
        (SCALEUP_LINE, "Scale-up (NVLink-class)"),
        (SCALEOUT_LINE, "Scale-out (cluster fabric)"),
        (INTERNAL_LINE, "In-node (PCIe / CXL)"),
    ]):
        lx = 0.08 + dx * 0.31
        line(lx, leg_y, lx + 0.04, leg_y, col, lw=2.2)
        ax.text(lx + 0.05, leg_y, txt, ha="left", va="center", fontsize=7.5,
                color=TEXT_MID, transform=ax.transAxes)

    ax.text(0.50, 0.975, "One node in an AI cluster: two fabrics, three roles",
            ha="center", va="top", fontsize=11, fontweight="bold", color=TEXT_DARK,
            transform=ax.transAxes)

    save(fig, "fig_scale_up_node.pdf")


def fig_cei_rate_vs_year():
    """OIF CEI lane rate vs year (from OFC 2025 CEI demo genealogy table)."""
    # Years: midpoints for ranges; 224G/448G are provisional placement for "202X".
    generations = [
        ("SPI4/SFI4", 2001.5, 1.6, False),
        ("SxI5", 2002.5, 3.125, False),
        ("CEI-6G", 2004, 6, False),
        ("CEI-11G", 2008, 11, False),
        ("CEI-28G", 2012, 28, False),
        ("CEI-56G", 2017, 56, False),
        ("CEI-112G", 2022, 112, False),
        ("CEI-224G", 2025, 224, True),   # framework 2022; shipping/demo era ~2025
        ("CEI-448G", 2028, 448, True),   # pathfinding; rate and year provisional
    ]
    years = np.array([g[1] for g in generations])
    rates = np.array([g[2] for g in generations])
    names = [g[0] for g in generations]
    provisional = [g[3] for g in generations]

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.set_yscale("log")
    ax.set_xlim(1999.5, 2030)
    ax.set_ylim(1, 900)
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate per differential pair (Gb/s)")
    ax.grid(True, which="both", alpha=0.28)

    # Solid history, open markers for provisional
    hist = ~np.array(provisional)
    fut = np.array(provisional)
    ax.plot(years[hist], rates[hist], "-o", color=BLUE, ms=6.5, lw=1.6,
            markerfacecolor=BLUE, markeredgecolor=BLUE, zorder=3, label="Published")
    ax.plot(years[fut], rates[fut], "o", color=ORANGE, ms=7.5, lw=1.4,
            markerfacecolor="white", markeredgecolor=ORANGE, markeredgewidth=1.6,
            zorder=4, label="Provisional (202X)")
    # Connect 112G -> 224G -> 448G with a dashed guide
    ax.plot(years[6:], rates[6:], "--", color=ORANGE, lw=1.1, alpha=0.85, zorder=2)

    # Labels: stagger a bit to reduce collisions
    offsets = {
        "SPI4/SFI4": (0, 8),
        "SxI5": (4, -10),
        "CEI-6G": (0, 8),
        "CEI-11G": (0, 8),
        "CEI-28G": (0, 8),
        "CEI-56G": (0, 8),
        "CEI-112G": (0, 8),
        "CEI-224G": (-2, 10),
        "CEI-448G": (-2, 10),
    }
    for name, y, r, prov in generations:
        dx, dy = offsets[name]
        ax.annotate(
            name, (y, r), textcoords="offset points", xytext=(dx, dy),
            fontsize=7.2, color=ORANGE if prov else TEXT_DARK, ha="center",
        )

    ax.set_yticks([1, 3, 10, 30, 100, 300, 448])
    ax.set_yticklabels(["1", "3", "10", "30", "100", "300", "448"])
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ax.set_title("OIF CEI lane-rate genealogy", fontsize=10, fontweight="bold",
                 color=TEXT_DARK, pad=8)

    save(fig, "fig_cei_rate_vs_year.pdf")


def fig_link_chain():
    """Full pluggable rack-to-rack link, folded U-shape: Tx row, fiber, Rx row."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    y_tx, y_rx = 0.70, 0.24
    bw, bh = 0.150, 0.150
    xs = [0.095, 0.265, 0.435, 0.605, 0.775]
    fiber_cx = 0.93

    def box(cx, cy, label, sub, fc):
        x, y = cx - bw / 2, cy - bh / 2
        ax.add_patch(FancyBboxPatch(
            (x, y), bw, bh,
            boxstyle="round,pad=0.010,rounding_size=0.014",
            linewidth=0.85, edgecolor=EDGE, facecolor=fc,
            transform=ax.transAxes, clip_on=False, zorder=3,
        ))
        ax.text(cx, cy + 0.028, label, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=TEXT_DARK,
                linespacing=1.05, transform=ax.transAxes, zorder=4)
        ax.text(cx, cy - 0.040, sub, ha="center", va="center",
                fontsize=6.6, color=TEXT_MID, linespacing=1.05,
                transform=ax.transAxes, zorder=4)

    def harrow(x0, y0, x1, y1):
        ax.add_patch(FancyArrowPatch(
            (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=9,
            linewidth=1.0, color=EDGE, transform=ax.transAxes,
            clip_on=False, zorder=2,
        ))

    # Tx row (left to right): host A then pluggable module A
    box(xs[0], y_tx, "Switch ASIC A", "MAC / PCS / FEC", LIGHT_BLUE)
    box(xs[1], y_tx, "Host SerDes", "PMA / EQ", LIGHT_GREEN)
    box(xs[2], y_tx, "PCB + cage", "AUI (VSR)", LIGHT_GREY)
    box(xs[3], y_tx, "Module DSP", "retimer / none", LIGHT_BLUE)
    box(xs[4], y_tx, "Driver + Tx", "laser/mod (PMD)", LIGHT_ORANGE)
    for i in range(4):
        harrow(xs[i] + bw / 2, y_tx, xs[i + 1] - bw / 2, y_tx)

    # Fiber (tall, right side) connects Tx row down to Rx row
    fx, fy = fiber_cx - 0.055, 0.155
    ax.add_patch(FancyBboxPatch(
        (fx, fy), 0.11, 0.51,
        boxstyle="round,pad=0.010,rounding_size=0.014",
        linewidth=0.85, edgecolor=EDGE, facecolor=LIGHT_PINK,
        transform=ax.transAxes, clip_on=False, zorder=3,
    ))
    ax.text(fiber_cx, 0.44, "Fiber\nplant", ha="center", va="center",
            fontsize=8.2, fontweight="bold", color=TEXT_DARK,
            linespacing=1.05, transform=ax.transAxes, zorder=4)
    ax.text(fiber_cx, 0.35, "connectors,\npatch panels", ha="center", va="center",
            fontsize=6.6, color=TEXT_MID, linespacing=1.05,
            transform=ax.transAxes, zorder=4)
    harrow(xs[4] + bw / 2, y_tx, fiber_cx, y_tx - 0.02)
    harrow(fiber_cx, y_rx + 0.02, xs[4] + bw / 2, y_rx)

    # Rx row (right to left): pluggable module B then host B
    box(xs[4], y_rx, "PD + TIA", "PMD Rx", LIGHT_ORANGE)
    box(xs[3], y_rx, "Module DSP", "retimer / none", LIGHT_BLUE)
    box(xs[2], y_rx, "PCB + cage", "AUI (VSR)", LIGHT_GREY)
    box(xs[1], y_rx, "Host SerDes", "PMA / EQ / FEC", LIGHT_GREEN)
    box(xs[0], y_rx, "Switch ASIC B", "$\\to$ NIC $\\to$ GPU", LIGHT_BLUE)
    for i in range(4, 0, -1):
        harrow(xs[i] - bw / 2, y_rx, xs[i - 1] + bw / 2, y_rx)

    # Domain-crossing labels at the optics
    ax.text(xs[4], y_tx + bh / 2 + 0.03, "E$\\to$O", ha="center", va="bottom",
            fontsize=7.2, fontweight="bold", color=RED, transform=ax.transAxes)
    ax.text(xs[4], y_rx - bh / 2 - 0.03, "O$\\to$E", ha="center", va="top",
            fontsize=7.2, fontweight="bold", color=RED, transform=ax.transAxes)

    # Module boundary hint (between AUI and module DSP), both rows
    for yb in (y_tx, y_rx):
        xline = (xs[2] + xs[3]) / 2
        ax.plot([xline, xline], [yb - bh / 2 - 0.015, yb + bh / 2 + 0.015],
                color=EDGE, lw=0.7, ls=":", transform=ax.transAxes, zorder=1)

    # Region labels
    ax.text(xs[0] - bw / 2, y_tx + bh / 2 + 0.075, "Rack A leaf switch (host)",
            ha="left", va="bottom", fontsize=7.4, color=TEXT_MID,
            transform=ax.transAxes)
    ax.text(xs[4] + bw / 2, y_tx + bh / 2 + 0.075, "Pluggable module A",
            ha="right", va="bottom", fontsize=7.4, color=TEXT_MID,
            transform=ax.transAxes)
    ax.text(xs[0] - bw / 2, y_rx - bh / 2 - 0.075, "Rack B leaf switch (host)",
            ha="left", va="top", fontsize=7.4, color=TEXT_MID,
            transform=ax.transAxes)
    ax.text(xs[4] + bw / 2, y_rx - bh / 2 - 0.075, "Pluggable module B",
            ha="right", va="top", fontsize=7.4, color=TEXT_MID,
            transform=ax.transAxes)

    # Legend (domain colors)
    leg = [
        (LIGHT_BLUE, "Digital"),
        (LIGHT_GREEN, "SerDes (PMA)"),
        (LIGHT_GREY, "Electrical"),
        (LIGHT_ORANGE, "Optics (PMD)"),
        (LIGHT_PINK, "Fiber"),
    ]
    lx0, ly = 0.06, 0.045
    for i, (col, txt) in enumerate(leg):
        lx = lx0 + i * 0.185
        ax.add_patch(FancyBboxPatch(
            (lx, ly - 0.012), 0.022, 0.024,
            boxstyle="round,pad=0.002,rounding_size=0.004",
            linewidth=0.7, edgecolor=EDGE, facecolor=col,
            transform=ax.transAxes, clip_on=False,
        ))
        ax.text(lx + 0.03, ly, txt, ha="left", va="center",
                fontsize=6.8, color=TEXT_MID, transform=ax.transAxes)

    ax.text(0.50, 0.985, "A pluggable rack-to-rack link, end to end",
            ha="center", va="top", fontsize=11, fontweight="bold",
            color=TEXT_DARK, transform=ax.transAxes)

    save(fig, "fig_link_chain.pdf")


if __name__ == "__main__":
    fig_ber_vs_q()
    fig_ber_vs_power_rin()
    fig_rin_floor()
    fig_noise_density_vs_power()
    fig_trace_loss()
    fig_nrz_vs_pam4()
    fig_448g_paths()
    fig_eq_chains()
    fig_oif_448g_package()
    fig_cei_reach_map()
    fig_cei_rate_vs_year()
    fig_scale_up_node()
    fig_link_chain()
    fig_liv_sketch()
    print("done")
