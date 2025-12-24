# AWGN BER Simulator (BPSK/QPSK)

Python simulation of digital baseband transmission over an Additive White Gaussian Noise (AWGN) channel, with BER vs SNR analysis for BPSK and QPSK.

## What this project does
- Generates random bits
- Modulates bits using **BPSK** or **QPSK**
- Passes symbols through an **AWGN** channel
- Demodulates and estimates **Bit Error Rate (BER)**
- Plots **BER vs SNR (dB)** and saves results

## Why it matters
This is a foundational wireless-communications simulation that demonstrates:
- correct SNR → noise variance mapping
- end-to-end PHY simulation workflow
- reproducible experiments and clean project structure

## Theory (quick)
We model:
- Transmit symbols: `x`
- AWGN noise: `n ~ CN(0, σ²)` (complex) or `N(0, σ²)` (real)
- Received: `y = x + n`

For normalized symbol energy `Es = 1`:
- `SNR_linear = 10^(SNR_dB/10)`
- Real noise variance (BPSK): `σ² = 1 / (2 * SNR_linear)`
- Complex noise variance (QPSK): `σ² = 1 / (SNR_linear)` for `CN(0, σ²)`
  - equivalently: each of I and Q has variance `σ²/2`

> Note: The code explicitly documents the chosen normalization so results are consistent.

## Repository structure
The project follows a clean, industry-style layout with a clear separation
between core modules, experiment scripts, tests, and results.

See **[`docs/project_structure.md`](docs/project_structure.md)** for the
detailed directory structure and design rationale.