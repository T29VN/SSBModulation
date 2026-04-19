# ============================================================
#  modules/filter.py – Lọc thông thấp Butterworth
#  Tương đương MATLAB:
#      [b, a] = butter(5, 3/96);
#      yf     = filter(b, a, y);
# ============================================================

import sys
import os

# Tự động thêm đường dẫn thư mục gốc vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
from scipy.signal import butter, lfilter

from config import SAMPLE_RATE, FILTER_ORDER, CUTOFF_NORM


def design_filter(order: int = FILTER_ORDER,
                  cutoff_norm: float = CUTOFF_NORM):
    """
    Thiết kế bộ lọc Butterworth thông thấp.

    Tương đương MATLAB:
        [b, a] = butter(5, 3/96);

    Giải thích tham số MATLAB butter(N, Wn):
        • N  = 5       → bậc bộ lọc
        • Wn = 3/96    → tần số cắt chuẩn hoá (Nyquist = 1)
          ↔  3 kHz / (Fs/2 = 96 kHz)  =  0.03125

    Parameters
    ----------
    order : int
        Bậc bộ lọc (mặc định = 5).
    cutoff_norm : float
        Tần số cắt chuẩn hoá theo Nyquist, trong (0, 1).
        Mặc định = 3/96 ≈ 0.03125.

    Returns
    -------
    b, a : np.ndarray
        Hệ số tử / mẫu của bộ lọc IIR.
    """
    b, a = butter(order, cutoff_norm, btype='low')
    return b, a


def apply_filter(y: np.ndarray,
                 order: int = FILTER_ORDER,
                 cutoff_norm: float = CUTOFF_NORM) -> np.ndarray:
    """
    Áp dụng bộ lọc Butterworth thông thấp lên tín hiệu y.

    Tương đương MATLAB:
        [b, a] = butter(5, 3/96);
        yf     = filter(b, a, y);

    Parameters
    ----------
    y : np.ndarray
        Tín hiệu đầu vào (1-D, float64).
    order : int
        Bậc bộ lọc.
    cutoff_norm : float
        Tần số cắt chuẩn hoá theo Nyquist.

    Returns
    -------
    yf : np.ndarray
        Tín hiệu sau khi lọc, cùng kích thước với y.
    """
    b, a = design_filter(order, cutoff_norm)
    yf = lfilter(b, a, y)

    print(f"[Filter] Butterworth LP  |  bậc {order}  |  "
          f"fc_norm = {cutoff_norm:.6f}  "
          f"(≈ {cutoff_norm * SAMPLE_RATE / 2 / 1000:.1f} kHz)")
    print(f"[Filter] Đầu vào: {len(y):,} mẫu  →  Đầu ra: {len(yf):,} mẫu")
    return yf


# ---------------------------------------------------------------
# Chạy thử độc lập:  python -m modules.filter
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Tạo tín hiệu test: pha trộn 1 kHz (giữ) + 20 kHz (loại bỏ)
    t = np.arange(0, 0.01, 1 / SAMPLE_RATE)
    test_signal = np.sin(2 * np.pi * 1000 * t) + np.sin(2 * np.pi * 20000 * t)

    yf = apply_filter(test_signal)

    print(f"\n--- Kiểm tra nhanh ---")
    print(f"  RMS trước lọc : {np.sqrt(np.mean(test_signal**2)):.4f}")
    print(f"  RMS sau lọc   : {np.sqrt(np.mean(yf**2)):.4f}")
    print(f"  (Thành phần 20 kHz phải bị suy giảm mạnh)")
