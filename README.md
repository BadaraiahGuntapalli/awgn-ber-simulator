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

## Reproducing Results (BER vs SNR)

This repository does **not** track generated result files (CSV/PNG) in Git.
All results are **reproducible** using the provided experiment script.

### Prerequisites
- Python ≥ 3.9
- NumPy
- Matplotlib

Install the project in editable mode from the repository root:

```bash
pip install -e .
````

### Run BER vs SNR Experiments

#### BPSK over AWGN

```bash
python scripts/run_ber_vs_snr.py \
    --mod bpsk \
    --snr_db 0 2 4 6 8 10 \
    --n_bits 200000 \
    --seed 0
```

#### QPSK over AWGN

```bash
python scripts/run_ber_vs_snr.py \
    --mod qpsk \
    --snr_db 0 2 4 6 8 10 \
    --n_bits 200000 \
    --seed 0
```

### Outputs

The script generates:

* `results/ber_<mod>.csv` — BER values vs SNR
* `results/ber_<mod>.png` — BER vs SNR plot (log-scale)

The `results/` directory is intentionally excluded from version control.
Users are expected to regenerate results locally.

### Notes

* QPSK uses Gray coding and unit symbol energy normalization.
* The SNR is interpreted as **Es/N0** with **Es = 1**.
* A fixed random seed ensures reproducibility across runs.

