# -*- coding: utf-8 -*-
import time
import numpy as np
import pmt
from gnuradio import gr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from top_block import top_block  # ficheiro gerado pelo GRC (No GUI)


class TagCounter(gr.sync_block):
    """Conta as tags 'wifi_start' que o Sync Short põe à saída em cada deteção."""
    def __init__(self, keys=("ofdm_start", "wifi_start")):
        gr.sync_block.__init__(self, name="tag_counter",
                               in_sig=[np.complex64], out_sig=None)
        self.keys = keys
        self.n_det = 0
        self.keys_vistas = set()

    def work(self, input_items, output_items):
        n = len(input_items[0])
        for t in self.get_tags_in_window(0, 0, n):
            k = pmt.symbol_to_string(t.key)
            self.keys_vistas.add(k)
            if k in self.keys:
                self.n_det += 1
        return n

# Primeiro teste com um só valor; depois troca pela linha do linspace
#thresholds = [0.56]
thresholds = np.linspace(0.2, 0.9, 36)

contagens = []
for i, th in enumerate(thresholds):
    tb = top_block(threshold=float(th))

    contador = TagCounter()
    tb.connect(tb.ieee802_11_ofdm_sync_short_0, contador)
    t0 = time.time()
    tb.start()
    tb.wait()
    dt = time.time() - t0

    if i == 0:
        print("tags vistas: {}".format(sorted(contador.keys_vistas)))

    contagens.append(contador.n_det)
    print("th={:.2f}  deteções={}  ({:.1f}s)".format(th, contador.n_det, dt))

    tb.stop()
    del tb, contador

resultado = np.column_stack((thresholds, contagens))
np.savetxt("resultado_sweep.csv", resultado, delimiter=",", header="threshold,deteccoes", comments="")
print(u"\n[threshold, deteções]")
print(resultado)

# opcional: gráfico
plt.figure()
plt.plot(thresholds, contagens, 'b-o')
plt.xlabel("Threshold")
plt.ylabel(u"Deteções (Sync Short)")
plt.grid(True)
plt.savefig("resultado_sweep.png")