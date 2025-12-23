# Project Structure

This repository follows an industry-style layout for
a reproducible wireless PHY simulation project.

## Folder Overview

- src/awgn_ber/
  - modulation.py : BPSK/QPSK modulation and demodulation
  - channel.py    : AWGN channel and noise variance mapping
  - metrics.py    : BER computation utilities
  - utils.py      : Common helpers

- scripts/
  - run_ber_vs_snr.py : Entry point for BER vs SNR experiments

- tests/
  - Unit tests for modulation and channel blocks

- results/
  - Generated BER plots and CSV outputs
