"""Analytic models for short-reach optical receivers.

Everything here is first-principles and matches the treatment in
Saeckinger, *Analysis and Design of Transimpedance Amplifiers for Optical
Receivers* (Wiley, 2018), Chapter 4. SI units throughout unless a name says
otherwise (dBm, dB/Hz).

Core relations
--------------
- Gaussian decision:            BER = 1/2 * erfc(Q / sqrt(2))
- Q at reference BER 1e-12:     Q = 7.03
- Optical sensitivity (avg):    P_sens = Q * i_n / R
- OMA sensitivity:              P_OMA_sens = 2 * Q * i_n / R
- Extinction-ratio penalty:     PP = (ER + 1) / (ER - 1)
- RIN power penalty:            PP = 1 / sqrt(1 - Q^2 * RIN_lin * BW)
- RIN-limited Q floor:          Q_max = 1 / sqrt(RIN_lin * BW)
"""

from __future__ import annotations

import numpy as np
from scipy.special import erfc, erfcinv

# Physical constants (SI)
Q_E = 1.602176634e-19  # elementary charge, C
H_PLANCK = 6.62607015e-34  # J*s
C_LIGHT = 299792458.0  # m/s


# ---------- BER <-> Q ----------

def q_to_ber(q: np.ndarray | float) -> np.ndarray | float:
    """BER for a Gaussian decision with quality factor Q."""
    return 0.5 * erfc(np.asarray(q, dtype=float) / np.sqrt(2.0))


def ber_to_q(ber: np.ndarray | float) -> np.ndarray | float:
    """Inverse of :func:`q_to_ber`."""
    return np.sqrt(2.0) * erfcinv(2.0 * np.asarray(ber, dtype=float))


# ---------- unit helpers ----------

def dbm_to_w(p_dbm: np.ndarray | float) -> np.ndarray | float:
    return 1e-3 * 10.0 ** (np.asarray(p_dbm, dtype=float) / 10.0)


def w_to_dbm(p_w: np.ndarray | float) -> np.ndarray | float:
    return 10.0 * np.log10(np.asarray(p_w, dtype=float) / 1e-3)


def rin_linear(rin_db_hz: float) -> float:
    """Convert RIN in dB/Hz to a linear 1/Hz spectral density."""
    return 10.0 ** (rin_db_hz / 10.0)


# ---------- noise variances (A^2) ----------

def shot_noise_var(i_photo: np.ndarray | float, bw: float) -> np.ndarray | float:
    """Shot-noise current variance for a mean photocurrent over bandwidth bw."""
    return 2.0 * Q_E * np.asarray(i_photo, dtype=float) * bw


def rin_noise_var(i_photo: np.ndarray | float, rin_db_hz: float, bw: float):
    """Intensity-noise current variance: sigma^2 = RIN_lin * I^2 * BW."""
    return rin_linear(rin_db_hz) * np.asarray(i_photo, dtype=float) ** 2 * bw


# ---------- noise current spectral densities (A/sqrt(Hz)) ----------
# RIN is a *relative* number, so it only becomes an absolute noise current once a
# photocurrent I = R*P is fixed. These return the one-sided amplitude spectral
# density in A/sqrt(Hz); square them for the PSD in A^2/Hz.

def shot_noise_density(i_photo: np.ndarray | float) -> np.ndarray | float:
    """Shot-noise current density sqrt(2 q I), in A/sqrt(Hz)."""
    return np.sqrt(2.0 * Q_E * np.asarray(i_photo, dtype=float))


def rin_noise_density(i_photo: np.ndarray | float, rin_db_hz: float) -> np.ndarray | float:
    """RIN current density sqrt(RIN_lin) * I, in A/sqrt(Hz)."""
    return np.sqrt(rin_linear(rin_db_hz)) * np.asarray(i_photo, dtype=float)


# ---------- extinction ratio ----------

def er_levels(p_avg_w, er_db):
    """Return (P1, P0) one/zero optical powers for a given average power and ER."""
    p_avg = np.asarray(p_avg_w, dtype=float)
    if np.isinf(er_db):
        return 2.0 * p_avg, np.zeros_like(p_avg)
    er = 10.0 ** (er_db / 10.0)
    p1 = p_avg * 2.0 * er / (er + 1.0)
    p0 = p_avg * 2.0 / (er + 1.0)
    return p1, p0


def er_penalty_db(er_db: float) -> float:
    """Power penalty (dB) from a finite extinction ratio, PP=(ER+1)/(ER-1)."""
    er = 10.0 ** (er_db / 10.0)
    return 10.0 * np.log10((er + 1.0) / (er - 1.0))


# ---------- full NRZ receiver BER model ----------

def nrz_q(
    p_avg_w,
    responsivity: float,
    i_thermal_rms: float,
    bw: float,
    er_db: float = np.inf,
    rin_db_hz: float = -np.inf,
    include_shot: bool = True,
):
    """Q factor for an NRZ IM/DD receiver including thermal, shot and RIN noise.

    Noise on the ones and zeros is computed separately (both shot and RIN are
    signal dependent), so Q = (I1 - I0) / (sigma1 + sigma0).
    """
    p1, p0 = er_levels(p_avg_w, er_db)
    i1 = responsivity * p1
    i0 = responsivity * p0

    var_th = i_thermal_rms ** 2
    var1 = np.full_like(np.asarray(i1, dtype=float), var_th)
    var0 = np.full_like(np.asarray(i0, dtype=float), var_th)
    if include_shot:
        var1 = var1 + shot_noise_var(i1, bw)
        var0 = var0 + shot_noise_var(i0, bw)
    if np.isfinite(rin_db_hz):
        var1 = var1 + rin_noise_var(i1, rin_db_hz, bw)
        var0 = var0 + rin_noise_var(i0, rin_db_hz, bw)

    return (i1 - i0) / (np.sqrt(var1) + np.sqrt(var0))


def nrz_ber(p_avg_w, **kwargs):
    return q_to_ber(nrz_q(p_avg_w, **kwargs))


# ---------- PAM4 ----------

def pam4_ber(
    p_avg_w,
    responsivity: float,
    i_thermal_rms: float,
    bw: float,
    er_db: float = np.inf,
    rin_db_hz: float = -np.inf,
    include_shot: bool = True,
):
    """Approximate PAM4 BER (Gray-coded, equally spaced levels).

    BER ~= (3/4) * 1/2 * erfc( (d/2) / (sigma * sqrt(2)) ), with level spacing
    d = OMA_current / 3. Noise is evaluated at the worst (top) inner level.
    """
    p1, p0 = er_levels(p_avg_w, er_db)  # outer one/zero -> OMA
    oma_i = responsivity * (p1 - p0)
    d = oma_i / 3.0

    i_top = responsivity * p1
    var = i_thermal_rms ** 2
    if include_shot:
        var = var + shot_noise_var(i_top, bw)
    if np.isfinite(rin_db_hz):
        var = var + rin_noise_var(i_top, rin_db_hz, bw)
    sigma = np.sqrt(var)

    return 0.75 * 0.5 * erfc((d / 2.0) / (sigma * np.sqrt(2.0)))


# ---------- RIN floor ----------

def rin_q_floor(rin_db_hz: float, bw: float) -> float:
    """Maximum achievable Q (infinite optical power) set by RIN: 1/sqrt(RIN_lin*BW)."""
    return 1.0 / np.sqrt(rin_linear(rin_db_hz) * bw)


def rin_penalty_db(q_target: float, rin_db_hz: float, bw: float) -> float:
    """Power penalty (dB) to hold q_target in the presence of RIN; inf past the floor."""
    x = q_target ** 2 * rin_linear(rin_db_hz) * bw
    if x >= 1.0:
        return np.inf
    return 10.0 * np.log10(1.0 / np.sqrt(1.0 - x))


# ---------- reference BER / FEC anchors ----------

BER_UNCODED = 1e-12            # classic reference, Q = 7.03
BER_KP4_PRE = 2.4e-4           # KP4 RS(544,514) pre-FEC threshold
BER_KP4_POST = 1e-15


if __name__ == "__main__":
    # Sanity checks against the textbook worked numbers.
    print("Q @ 1e-12      :", round(float(ber_to_q(1e-12)), 3), "(expect 7.03)")
    print("Q @ 1e-4       :", round(float(ber_to_q(1e-4)), 3), "(expect ~3.72)")
    print("Q @ KP4 pre    :", round(float(ber_to_q(BER_KP4_PRE)), 3))
    print("ER penalty 10dB:", round(er_penalty_db(10.0), 3), "dB (expect ~0.87)")
    print("ER penalty 6dB :", round(er_penalty_db(6.0), 3), "dB (expect ~2.2)")
    print("RIN floor -140 dB/Hz @ 40 GHz: Q_max =",
          round(rin_q_floor(-140.0, 40e9), 2))
    _i0 = 0.8 * dbm_to_w(0.0)  # R=0.8 A/W, P=0 dBm -> I=0.8 mA
    print("@0 dBm (I=0.8 mA): shot density =",
          round(shot_noise_density(_i0) * 1e12, 1), "pA/rtHz")
    for _rin in (-136.0, -145.0, -155.0, -165.0):
        print(f"  RIN {_rin:.0f} dB/Hz density =",
              round(rin_noise_density(_i0, _rin) * 1e12, 1), "pA/rtHz")
