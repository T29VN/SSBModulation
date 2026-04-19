# ============================================================
#  main.py – Chương trình chính: Thu âm → Lọc → Điều chế SSB → Xuất
#
#  Pipeline tương đương MATLAB:
#      r = audiorecorder(192000, 16, 1);
#      record(r); stop(r);
#      y = getaudiodata(r, 'double');
#      y = y(1:192000*10);
#      [b, a] = butter(5, 3/96);
#      yf = filter(b, a, y);
#      ssb_lb = ssbmod(yf, 47, 192);
#      plot(abs(fft(ssb_lb)))
#      audiowrite('nguyenvanA_1234.wav', ssb_lb, 192000)
#
#  Chạy:  python main.py
# ============================================================

import numpy as np
from config import SAMPLE_RATE, DURATION, OUTPUT_WAV, CARRIER_FREQ

from modules.recorder import record, save_raw, list_devices
from modules.filter import apply_filter
from modules.modulator import ssbmod
from modules.exporter import plot_spectrum, plot_spectrum_freq, export_wav


def main():
    print("=" * 60)
    print("  SSB MODULATION  –  Thu âm → Lọc → Điều chế → Xuất file")
    print("=" * 60)
    print(f"  Fs         = {SAMPLE_RATE/1000:.0f} kHz")
    print(f"  Thời lượng = {DURATION} s")
    print(f"  Sóng mang  = {CARRIER_FREQ/1000:.0f} kHz")
    print(f"  File output= {OUTPUT_WAV}")
    print("=" * 60)

    # ----------------------------------------------------------
    # Bước 0: Hiển thị danh sách thiết bị âm thanh
    # ----------------------------------------------------------
    print("\n[Bước 0] Danh sách thiết bị âm thanh:")
    list_devices()

    # ----------------------------------------------------------
    # Bước 1: Thu âm
    #   MATLAB: r = audiorecorder(192000,16,1);
    #           record(r); stop(r);
    #           y = getaudiodata(r,'double');
    #           y = y(1:192000*10);
    # ----------------------------------------------------------
    print(f"\n{'─'*60}")
    print("[Bước 1] THU ÂM")
    print(f"{'─'*60}")
    y = record()
    print(f"  → Số mẫu: {len(y):,}  |  "
          f"Thời lượng: {len(y)/SAMPLE_RATE:.2f}s")

    # Lưu file thô (tuỳ chọn, để kiểm tra)
    save_raw(y, path="output/raw_record.wav")

    # ----------------------------------------------------------
    # Bước 2: Lọc thông thấp Butterworth
    #   MATLAB: [b, a] = butter(5, 3/96);
    #           yf = filter(b, a, y);
    # ----------------------------------------------------------
    print(f"\n{'─'*60}")
    print("[Bước 2] LỌC THÔNG THẤP (Butterworth)")
    print(f"{'─'*60}")
    yf = apply_filter(y)

    # ----------------------------------------------------------
    # Bước 3: Điều chế SSB (Lower Sideband)
    #   MATLAB: ssb_lb = ssbmod(yf, 47, 192);
    # ----------------------------------------------------------
    print(f"\n{'─'*60}")
    print("[Bước 3] ĐIỀU CHẾ SSB")
    print(f"{'─'*60}")
    ssb_lb = ssbmod(yf)

    # ----------------------------------------------------------
    # Bước 4: Vẽ phổ tín hiệu đã điều chế
    #   MATLAB: plot(abs(fft(ssb_lb)))
    # ----------------------------------------------------------
    print(f"\n{'─'*60}")
    print("[Bước 4] VẼ PHỔ TÍN HIỆU")
    print(f"{'─'*60}")

    # Phổ kiểu MATLAB gốc: plot(abs(fft(ssb_lb)))
    plot_spectrum(ssb_lb,
                  title="Phổ SSB – plot(abs(fft(ssb_lb)))",
                  save_path="output/spectrum_matlab_style.png")

    # Phổ trục tần số (kHz) – trực quan hơn
    plot_spectrum_freq(ssb_lb,
                       title="Phổ SSB – Trục tần số (kHz)",
                       save_path="output/spectrum_freq.png")

    # ----------------------------------------------------------
    # Bước 5: Xuất file WAV
    #   MATLAB: audiowrite('nguyenvanA_1234.wav', ssb_lb, 192000)
    # ----------------------------------------------------------
    print(f"\n{'─'*60}")
    print("[Bước 5] XUẤT FILE WAV")
    print(f"{'─'*60}")
    export_wav(ssb_lb)

    # ----------------------------------------------------------
    # Hoàn thành
    # ----------------------------------------------------------
    print(f"\n{'='*60}")
    print("  ✓ HOÀN THÀNH TOÀN BỘ PIPELINE!")
    print(f"  ✓ File WAV  : {OUTPUT_WAV}")
    print(f"  ✓ Hình phổ  : output/spectrum_matlab_style.png")
    print(f"  ✓           : output/spectrum_freq.png")
    print(f"  ✓ File thô  : output/raw_record.wav")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
