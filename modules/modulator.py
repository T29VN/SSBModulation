# ============================================================
#  modules/modulator.py – Điều chế SSB (Single-Sideband)
#  Tương đương MATLAB:
#      ssb_lb = ssbmod(yf, Fc, Fs);
#
#  Công thức SSB Lower Sideband (LSB):
#      y(t) = x(t)·cos(2π·fc·t) + x̂(t)·sin(2π·fc·t)
#  trong đó x̂(t) là biến đổi Hilbert của x(t).
# ============================================================

import sys
import os

# Tự động thêm đường dẫn thư mục gốc vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
from scipy.signal import hilbert

from config import SAMPLE_RATE, CARRIER_FREQ


def ssbmod(x: np.ndarray,
           fc: float = CARRIER_FREQ,
           fs: int = SAMPLE_RATE,
           sideband: str = "lower") -> np.ndarray:
    """
    Điều chế SSB – tương đương hàm ssbmod() của MATLAB.

    MATLAB gốc:
        ssb_lb = ssbmod(yf, 47, 192);
        → fc = 47 kHz, fs = 192 kHz  (MATLAB truyền đơn vị kHz)

    Ở đây ta dùng đơn vị Hz trực tiếp (fc = 20000 Hz, fs = 192000 Hz)
    để rõ ràng hơn.

    Công thức (Lower Sideband – LSB):
        y(t) = x(t) · cos(2π·fc·t)  +  x̂(t) · sin(2π·fc·t)

    Công thức (Upper Sideband – USB):
        y(t) = x(t) · cos(2π·fc·t)  –  x̂(t) · sin(2π·fc·t)

    Parameters
    ----------
    x : np.ndarray
        Tín hiệu đầu vào đã lọc (1-D, float64).
    fc : float
        Tần số sóng mang (Hz). Mặc định = 20000 Hz (20 kHz).
    fs : int
        Tần số lấy mẫu (Hz). Mặc định = 192000 Hz.
    sideband : str
        "lower" (LSB) hoặc "upper" (USB). Mặc định = "lower".

    Returns
    -------
    y_ssb : np.ndarray
        Tín hiệu SSB đã điều chế, cùng kích thước với x.
    """
    N = len(x)
    t = np.arange(N) / fs                    # vector thời gian (s)

    # Biến đổi Hilbert → lấy phần ảo = tín hiệu Hilbert x̂(t)
    x_hilbert = np.imag(hilbert(x))           # tương đương imag(hilbert(x))

    # Sóng mang
    cos_carrier = np.cos(2 * np.pi * fc * t)
    sin_carrier = np.sin(2 * np.pi * fc * t)

    # Điều chế SSB
    if sideband == "lower":
        # LSB: y = x·cos + x̂·sin  (giống MATLAB ssbmod mặc định)
        y_ssb = x * cos_carrier + x_hilbert * sin_carrier
    elif sideband == "upper":
        # USB: y = x·cos – x̂·sin
        y_ssb = x * cos_carrier - x_hilbert * sin_carrier
    else:
        raise ValueError(f"sideband phải là 'lower' hoặc 'upper', nhận được '{sideband}'")

    print(f"[Modulator] SSB {sideband.upper()} sideband")
    print(f"[Modulator] Sóng mang fc = {fc/1000:.1f} kHz  |  "
          f"Fs = {fs/1000:.0f} kHz")
    print(f"[Modulator] Số mẫu: {N:,}  |  "
          f"Thời lượng: {N/fs:.2f}s")

    return y_ssb


# ---------------------------------------------------------------
# Chạy thử độc lập:  python -m modules.modulator
# ---------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Tạo tín hiệu test: sóng sin 1 kHz
    duration_test = 0.05   # 50 ms
    t = np.arange(0, duration_test, 1 / SAMPLE_RATE)
    test_signal = np.sin(2 * np.pi * 1000 * t)   # 1 kHz

    # Điều chế SSB-LSB
    ssb = ssbmod(test_signal)

    # Vẽ phổ biên độ (tương đương MATLAB: plot(abs(fft(ssb_lb))))
    N = len(ssb)
    freqs = np.fft.fftfreq(N, d=1/SAMPLE_RATE) / 1000   # kHz
    spectrum = np.abs(np.fft.fft(ssb))

    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:N//2], spectrum[:N//2])
    plt.xlabel("Tần số (kHz)")
    plt.ylabel("|FFT|")
    plt.title(f"Phổ SSB-LSB  |  fc = {CARRIER_FREQ/1000:.0f} kHz  |  "
              f"Tín hiệu test 1 kHz")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
