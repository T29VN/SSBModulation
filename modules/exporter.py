# ============================================================
#  modules/exporter.py – Vẽ phổ & xuất file WAV
#  Tương đương MATLAB:
#      plot(abs(fft(ssb_lb)))
#      audiowrite('nguyenvanA_1234.wav', ssb_lb, 192000)
# ============================================================

import sys
import os

# Tự động thêm đường dẫn thư mục gốc vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

from config import SAMPLE_RATE, OUTPUT_WAV, CARRIER_FREQ


def plot_spectrum(signal: np.ndarray,
                  fs: int = SAMPLE_RATE,
                  title: str = "Phổ tín hiệu SSB đã điều chế",
                  save_path: str = None) -> None:
    """
    Vẽ phổ biên độ |FFT| của tín hiệu – giống MATLAB:
        plot(abs(fft(ssb_lb)))

    Trục X hiển thị chỉ số mẫu (sample index), giống hệt
    cách MATLAB vẽ mặc định khi gọi plot(abs(fft(...))).

    Parameters
    ----------
    signal : np.ndarray
        Tín hiệu đã điều chế SSB (1-D).
    fs : int
        Tần số lấy mẫu (Hz).
    title : str
        Tiêu đề biểu đồ.
    save_path : str or None
        Nếu khác None, lưu hình vào đường dẫn này (PNG).
    """
    N = len(signal)
    spectrum = np.abs(np.fft.fft(signal))

    # ---- Đồ thị giống MATLAB: plot(abs(fft(ssb_lb))) ----
    # Trục X = chỉ số mẫu 0..N-1, giống hệt MATLAB mặc định
    plt.figure(figsize=(12, 5))
    plt.plot(np.arange(N), spectrum, linewidth=0.6, color='#0072BD')
    plt.xlabel("Chỉ số mẫu (sample index)")
    plt.ylabel("|FFT|")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)
        print(f"[Exporter] Đã lưu hình phổ → {save_path}")

    plt.show()


def plot_spectrum_freq(signal: np.ndarray,
                       fs: int = SAMPLE_RATE,
                       title: str = "Phổ tín hiệu SSB (trục tần số)",
                       save_path: str = None) -> None:
    """
    Vẽ phổ biên độ với trục X là tần số (kHz) – chỉ nửa dương.
    Phiên bản trực quan hơn so với đồ thị MATLAB gốc.

    Parameters
    ----------
    signal : np.ndarray
        Tín hiệu đã điều chế SSB (1-D).
    fs : int
        Tần số lấy mẫu (Hz).
    title : str
        Tiêu đề biểu đồ.
    save_path : str or None
        Nếu khác None, lưu hình vào đường dẫn này (PNG).
    """
    N = len(signal)
    spectrum = np.abs(np.fft.fft(signal))

    # Chỉ lấy nửa phổ dương (0 → Fs/2)
    half_N = N // 2
    freqs_khz = np.fft.fftfreq(N, d=1/fs)[:half_N] / 1000  # kHz
    mag_half = spectrum[:half_N]

    plt.figure(figsize=(12, 5))
    plt.plot(freqs_khz, mag_half, linewidth=0.6, color='#0072BD')
    plt.xlabel("Tần số (kHz)")
    plt.ylabel("|FFT|")
    plt.title(title)

    # Đánh dấu vị trí sóng mang
    plt.axvline(x=CARRIER_FREQ/1000, color='red', linestyle='--',
                alpha=0.5, label=f'fc = {CARRIER_FREQ/1000:.0f} kHz')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)
        print(f"[Exporter] Đã lưu hình phổ (tần số) → {save_path}")

    plt.show()


def export_wav(signal: np.ndarray,
               path: str = OUTPUT_WAV,
               fs: int = SAMPLE_RATE) -> None:
    """
    Xuất tín hiệu đã điều chế ra file WAV.

    Tương đương MATLAB:
        audiowrite('nguyenvanA_1234.wav', ssb_lb, 192000)

    Parameters
    ----------
    signal : np.ndarray
        Tín hiệu SSB (1-D, float64, biên độ trong [-1, 1]).
    path : str
        Đường dẫn file WAV đầu ra.
    fs : int
        Tần số lấy mẫu (Hz).
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Chuẩn hoá biên độ về [-1, 1] để tránh clipping khi ghi WAV
    peak = np.max(np.abs(signal))
    if peak > 0:
        signal_norm = signal / peak * 0.95   # giữ headroom 5 %
    else:
        signal_norm = signal

    sf.write(path, signal_norm, fs, subtype='PCM_16')

    duration_s = len(signal) / fs
    print(f"[Exporter] Đã xuất file WAV → {path}")
    print(f"[Exporter]   Fs = {fs/1000:.0f} kHz  |  "
          f"{len(signal):,} mẫu  |  {duration_s:.2f}s  |  PCM 16-bit")


# ---------------------------------------------------------------
# Chạy thử độc lập:  python -m modules.exporter
# ---------------------------------------------------------------
if __name__ == "__main__":
    from modules.filter import apply_filter
    from modules.modulator import ssbmod

    # Tạo tín hiệu test: sóng sin 1 kHz, 0.5 giây
    duration_test = 0.5
    t = np.arange(0, duration_test, 1 / SAMPLE_RATE)
    test_signal = np.sin(2 * np.pi * 1000 * t)

    # Lọc → Điều chế
    yf = apply_filter(test_signal)
    ssb_lb = ssbmod(yf)

    # Vẽ phổ (kiểu MATLAB gốc)
    plot_spectrum(ssb_lb, title="Test: plot(abs(fft(ssb_lb)))")

    # Vẽ phổ (trục tần số kHz, trực quan hơn)
    plot_spectrum_freq(ssb_lb, title="Test: Phổ SSB – trục tần số")

    # Xuất WAV
    export_wav(ssb_lb, path="output/test_ssb_output.wav")
