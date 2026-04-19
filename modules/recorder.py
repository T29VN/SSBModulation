# ============================================================
#  modules/recorder.py – Thu âm thanh (thay thế audiorecorder + record + stop)
# ============================================================

import numpy as np
import sounddevice as sd
import soundfile as sf

import sys
import os

# Tự động thêm đường dẫn thư mục gốc (D:\SSBModulation) vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import SAMPLE_RATE, CHANNELS, DURATION, BIT_DEPTH


def list_devices():
    """In danh sách thiết bị âm thanh để chọn đúng micro."""
    print(sd.query_devices())


def record(duration: int = DURATION,
           sample_rate: int = SAMPLE_RATE,
           channels: int = CHANNELS) -> np.ndarray:
    """
    Thu âm trong `duration` giây.

    Tương đương MATLAB:
        r = audiorecorder(192000, 16, 1);
        record(r); stop(r);
        y = getaudiodata(r, 'double');
        y = y(1 : 192000*10);

    Returns
    -------
    y : np.ndarray, shape (duration*sample_rate,)
        Dữ liệu âm thanh dạng float64, biên độ trong [-1, 1].
    """
    print(f"[Recorder] Bắt đầu thu âm {duration}s  |  "
          f"{sample_rate} Hz  |  {channels} kênh  |  {BIT_DEPTH}-bit ...")

    y = sd.rec(
        frames      = int(duration * sample_rate),
        samplerate  = sample_rate,
        channels    = channels,
        dtype       = "float64",   # tương đương getaudiodata(...,'double')
        blocking    = True         # tự động stop() khi hết duration
    )

    sd.wait()  # chắc chắn ghi xong
    y = y.flatten()  # chuyển (N,1) → (N,) như MATLAB column-vector

    print(f"[Recorder] Hoàn thành. Số mẫu thu được: {len(y):,}  "
          f"(mong đợi: {duration * sample_rate:,})")
    return y


def save_raw(y: np.ndarray,
             path: str = "output/raw_record.wav",
             sample_rate: int = SAMPLE_RATE) -> None:
    """
    Lưu âm thanh thô ra file WAV (tuỳ chọn, để kiểm tra trước khi xử lý).
    """
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, y, sample_rate, subtype="PCM_16")
    print(f"[Recorder] Đã lưu file thô → {path}")


# ---------------------------------------------------------------
# Chạy thử độc lập:  python -m modules.recorder
# ---------------------------------------------------------------
if __name__ == "__main__":
    list_devices()
    audio = record()
    save_raw(audio)