
import numpy as np

from awgn_ber.modulation import bpsk_modulate, bpsk_demodulate, qpsk_modulate, qpsk_demodulate

bits = np.random.randint(0, 2, 20, dtype=np.uint8)

# BPSK
s = bpsk_modulate(bits)
bh = bpsk_demodulate(s)
print("BPSK ok:", np.all(bits == bh))

# QPSK (needs even bits)
bits2 = np.random.randint(0, 2, 20, dtype=np.uint8)
sq = qpsk_modulate(bits2)
bh2 = qpsk_demodulate(sq)
print("QPSK ok:", np.all(bits2 == bh2))

