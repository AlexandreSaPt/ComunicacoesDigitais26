# -*- coding: utf-8 -*-

import sys
# Adiciona a pasta onde está o top_block.py ao caminho do Python
sys.path.append("/mnt/c/Users/josed/Universidade/ComDig")

import glob
import os
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pmt
from gnuradio import gr
from top_block import top_block  # ficheiro gerado pelo GRC (No GUI)

matplotlib.use('Agg')

# ==============================================================================
# CONFIGURAÇÃO DE PASTAS E THRESHOLDS
# ==============================================================================
PASTA_ENTRADA = "/mnt/c/Users/josed/Universidade/ComDig/Testing Data/Adalm-Pluto_Recording/To test"
PASTA_SAIDA = "/mnt/c/Users/josed/Universidade/ComDig/Testing Data/Adalm-Pluto_Recording/Results"

thresholds = np.linspace(0.2, 0.9, 80)

# Criar a pasta de saída caso não exista
if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)


class TagCounter(gr.sync_block):
    """Conta as tags 'wifi_start' que o Sync Short põe à saída em cada deteção."""

    def __init__(self, keys=("ofdm_start", "wifi_start")):
        gr.sync_block.__init__(
            self, name="tag_counter", in_sig=[np.complex64], out_sig=None
        )
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


def formatar_tempo(segundos):
    """Converte segundos para um formato legível (MM:SS ou HH:MM:SS)."""
    m, s = divmod(int(segundos), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return "{:02d}h {:02d}m {:02d}s".format(h, m, s)
    return "{:02d}m {:02d}s".format(m, s)


# procurar todos os ficheiros .bin na pasta especificada
padrao_ficheiros = os.path.join(PASTA_ENTRADA, "*.bin")
ficheiros_bin = sorted(glob.glob(padrao_ficheiros))

if not ficheiros_bin:
    print("Nenhum ficheiro .bin encontrado em: {}".format(PASTA_ENTRADA))
else:
    total_ficheiros = len(ficheiros_bin)
    total_iteracoes_por_ficheiro = len(thresholds)
    total_passos_globais = total_ficheiros * total_iteracoes_por_ficheiro
    
    print("Encontrados {} ficheiros para processar.".format(total_ficheiros))
    print("Total de iterações por ficheiro: {}".format(total_iteracoes_por_ficheiro))
    print("Total global de testes: {}\n".format(total_passos_globais))

tempo_inicio_global = time.time()
passos_concluidos = 0

for idx_f, caminho_ficheiro in enumerate(ficheiros_bin):
    nome_base = os.path.splitext(os.path.basename(caminho_ficheiro))[0]

    print("=" * 70)
    print(
        "[{}/{}] Processando ficheiro: {}".format(
            idx_f + 1, total_ficheiros, os.path.basename(caminho_ficheiro)
        )
    )
    print("=" * 70)

    contagens = []

    for i, th in enumerate(thresholds):
        tb = top_block(threshold=float(th), file_path=caminho_ficheiro)

        contador = TagCounter()
        tb.connect(tb.ieee802_11_ofdm_sync_short_0, contador)

        t0 = time.time()
        tb.start()
        tb.wait()
        dt = time.time() - t0

        if i == 0 and idx_f == 0:
            print("  Tags vistas: {}".format(sorted(contador.keys_vistas)))

        contagens.append(contador.n_det)
        
        # Atualização do progresso e estimativa de tempo
        passos_concluidos += 1
        tempo_decorrido = time.time() - tempo_inicio_global
        tempo_medio_por_passo = tempo_decorrido / passos_concluidos
        
        passos_restantes = total_passos_globais - passos_concluidos
        eta_segundos = passos_restantes * tempo_medio_por_passo
        
        print(
            "  [{:2d}/{}] th={:.2f} | deteções={:4d} ({:.1f}s) | ETA total: {}".format(
                i + 1,
                total_iteracoes_por_ficheiro,
                th,
                contador.n_det,
                dt,
                formatar_tempo(eta_segundos)
            )
        )

        tb.stop()
        del tb, contador

    # Guardar CSV
    resultado = np.column_stack((thresholds, contagens))
    nome_csv = os.path.join(PASTA_SAIDA, "resultado_{}.csv".format(nome_base))
    nome_png = os.path.join(PASTA_SAIDA, "grafico_{}.png".format(nome_base))

    np.savetxt(
        nome_csv,
        resultado,
        delimiter=",",
        header="threshold,deteccoes",
        comments="",
    )

    # Guardar Gráfico
    plt.figure()
    plt.plot(thresholds, contagens, "b-o")
    plt.title("Ficheiro: {}".format(nome_base))
    plt.xlabel("Threshold")
    plt.ylabel(u"Deteções (Sync Short)")
    plt.grid(True)
    plt.savefig(nome_png)
    plt.close()

    print("\nGuardado: {}".format(nome_csv))
    print("Guardado: {}\n".format(nome_png))

tempo_total = time.time() - tempo_inicio_global
print("Processamento concluído para todos os ficheiros em {}.".format(formatar_tempo(tempo_total)))