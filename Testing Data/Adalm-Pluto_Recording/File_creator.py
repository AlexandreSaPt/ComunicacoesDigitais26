# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import adi

# Pasta (caminho absoluto) onde os ficheiros vao ser gravados
OUTPUT_DIR = "/mnt/c/Users/josed/Universidade/ComDig/Testing Data/Adalm-Pluto_Recording/Recordings"

BASE_FILENAME = "wifi_FEUPParkingLot_6_nov_2026"
EXTENSION = ".bin"

NUM_FILES = 3
TARGET_BYTES = 500 * 1024 * 1024      # 500 MB por ficheiro

# O pyadi-iio devolve valores brutos do ADC de 12 bits (-2048..2047).
# O GNU Radio (gr-iio) entrega amostras normalizadas para +-1.
# Ponha False se quiser os valores brutos.
NORMALIZE = True

# Cria a pasta de destino se nao existir
if not os.path.isabs(OUTPUT_DIR):
    sys.exit("ERRO: OUTPUT_DIR tem de ser um caminho absoluto: {}".format(OUTPUT_DIR))
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sdr = adi.Pluto("ip:10.227.144.100")
sdr.sample_rate = int(20e6)
sdr.rx_rf_bandwidth = int(20e6)
sdr.rx_lo = int(5.22e9)
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = 30
sdr.rx_buffer_size = 1000000

print("A iniciar gravacao de {} ficheiros de 500 MB em '{}'...".format(NUM_FILES, OUTPUT_DIR))

for file_idx in range(1, NUM_FILES + 1):
    filename = "{}_{}{}".format(BASE_FILENAME, file_idx, EXTENSION)
    current_path = os.path.join(OUTPUT_DIR, filename)
    bytes_written = 0

    print("\n[Ficheiro {}/{}] A gravar em '{}'...".format(file_idx, NUM_FILES, current_path))

    with open(current_path, "wb") as f:
        while bytes_written < TARGET_BYTES:
            samples = sdr.rx()
            if NORMALIZE:
                samples = samples / 2048.0

            raw_bytes = samples.astype(np.complex64).tobytes()

            remaining = TARGET_BYTES - bytes_written
            if len(raw_bytes) > remaining:
                raw_bytes = raw_bytes[:remaining]

            f.write(raw_bytes)
            bytes_written += len(raw_bytes)

            mb = bytes_written / (1024.0 * 1024.0)
            pct = bytes_written * 100.0 / TARGET_BYTES
            sys.stdout.write("Progresso: {:.2f} MB / 500.00 MB ({:.1f}%)\r".format(mb, pct))
            sys.stdout.flush()

print("\n\nGravacao concluida! {} ficheiros criados em '{}'.".format(NUM_FILES, OUTPUT_DIR))