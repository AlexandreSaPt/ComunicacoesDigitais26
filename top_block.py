#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Oct 30 16:35:53 2026
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ieee802_11


class top_block(gr.top_block):

    def __init__(self, threshold=0.56):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.threshold = threshold

        ##################################################
        # Variables
        ##################################################
        self.window_size = window_size = 48
        self.samp_rate = samp_rate = 20e6
        self.max_samples = max_samples = 5200
        self.gain = gain = 30
        self.fft_size = fft_size = 64
        self.center_frq = center_frq = 5.22e9

        ##################################################
        # Blocks
        ##################################################
        self.ieee802_11_ofdm_sync_short_0 = ieee802_11.ofdm_sync_short(threshold, max_samples, 2, False, False)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(1, ([1]*window_size))
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, ([1]*window_size))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/mnt/c/Users/josed/Universidade/ComDig/Wifi_Project_Baseband_recordings/Sample3_20MHz_Channel100.bin', False)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 16)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.ieee802_11_ofdm_sync_short_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.ieee802_11_ofdm_sync_short_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.ieee802_11_ofdm_sync_short_0, 0), (self.blocks_null_sink_0, 0))

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
        self.fir_filter_xxx_0_0.set_taps(([1]*self.window_size))
        self.fir_filter_xxx_0.set_taps(([1]*self.window_size))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_max_samples(self):
        return self.max_samples

    def set_max_samples(self, max_samples):
        self.max_samples = max_samples

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_center_frq(self):
        return self.center_frq

    def set_center_frq(self, center_frq):
        self.center_frq = center_frq


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--threshold", dest="threshold", type="eng_float", default=eng_notation.num_to_str(0.56),
        help="Set threshold [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(threshold=options.threshold)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
