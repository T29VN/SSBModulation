# ============================================================
#  config.py – Cấu hình toàn bộ dự án
# ============================================================

# --- Thu âm ---
SAMPLE_RATE    = 192000   # Hz  (tương đương audiorecorder(192000,...))
BIT_DEPTH      = 16       # bit (tương đương audiorecorder(...,16,...))
CHANNELS       = 1        # mono (tương đương audiorecorder(...,1))
DURATION       = 15       # giây muốn giữ lại (y = y(1:192000*10))

# --- Butter filter ---
FILTER_ORDER   = 5        # bậc bộ lọc (butter(5,...))
CUTOFF_NORM    = 3 / 96   # tần số cắt chuẩn hoá = 3 kHz / (Fs/2=96 kHz)

# --- Điều chế SSB ---
CARRIER_FREQ   = 47_000   # Hz – tần số sóng mang (47 kHz)

# --- Xuất file ---
OUTPUT_WAV     = "output/Tran_Nhat_Truong_20224182.wav"