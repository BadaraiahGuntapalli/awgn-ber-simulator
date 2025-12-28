"""
Run BER vs SNR experiment for BPSK/QPSK over AWGN

Example:
    python scripts/run_ber_vs_snr.py --mod bpsk --n_bits 200000 --snr_db 0 2 4 6 8 10
    python scripts/run_ber_vs_snr.py --mod bpsk --n_bits 200000 --snr_db 0 2 4 6 8 10
"""


from __future__ import annotations
import argparse
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt

from awgn_ber.modulation import modulate, demodulate
from awgn_ber.channel import awgn
from awgn_ber.metrics import ber, ber_theory_bpsk_awgn, ber_theory_qpsk_awgn





def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="BER vs SNR for BPSK/QPSK over AWGN")
    p.add_argument(
        "--mod",
        type=str,
        choices=["bpsk", "qpsk"],
        required = True,
        help="Modulation scheme"
    )
    
    p.add_argument(
        "--snr_db",
        type=float,
        nargs="+",
        required=True,
        help="List of SNR(dB) points, e.g., --snr_db 0 2 4 6 8 10",
    )
    p.add_argument(
        "--n_bits",
        type=int,
        default=200_000,
        help="Number of bits for Monte Carlo BER estimation (default: 200000)",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for reproducibility (default: 0)",
    )
    p.add_argument(
        "--results_dir",
        type=str,
        default="results",
        help="Directory to save CSV/plot (default: results)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    
    rng = np.random.default_rng(args.seed)

    n_bits = int(args.n_bits)
    
    if n_bits <= 0:
        raise ValueError("--n_bits must be positive")
    
    # QPSK needs even number of bits (2 bits/symbol)
    if args.mod == "qpsk" and n_bits%2 != 0:
        n_bits += 1     # minimal adjustment
        print(f"[info] QPSK requires even bits. Using n_bits={n_bits} instead.")  
        
    snr_db_list = [float(x) for x in args.snr_db]
    
    # Generate a single bitstream reused for all SNR points (fair comparision)
    bits_tx = rng.integers(0, 2, size = n_bits, dtype=np.uint8)
    
    # Modulate once (Es=1 normalization handledin modulation)
    x = modulate(bits_tx, scheme = args.mod)
    
    ber_list: list[float] = []
    for snr_db in snr_db_list:
        y = awgn(x, snr_db=snr_db, rng=rng)
        bits_rx = demodulate(y, scheme=args.mod)
        ber_val = ber(bits_tx, bits_rx)
        ber_list.append(float(ber_val))
        print(f"SNR={snr_db:>6.2f} dB | BER= {ber_val:6e}")
        
    #save results
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = results_dir / f"ber_{args.mod}.csv"
    data = np.column_stack([np.round(np.array(snr_db_list, dtype=float), 2), np.round(np.array(ber_list, dtype=float), 2)])
    header="snr_db,ber"
    np.savetxt(csv_path, data, delimiter=",", header=header, comments="")
    print(f"saved {csv_path}")


    # calculating the theorictal ber for bpsk and qpsk 
    snr_arr = np.array(snr_db_list, dtype=float )

    if args.mod == "bpsk":
        ber_th = ber_theory_bpsk_awgn(snr_arr, snr_def="EbN0")
    else:
        ber_th = ber_theory_qpsk_awgn(snr_arr, snr_def="EsN0")
    
    # plot (semilogy is standard for BER curves)
    plt.figure()
    plt.semilogy(snr_db_list, ber_list, marker='*', label='Simulated BER')
    plt.semilogy(snr_db_list, ber_th, linestyle='--', linewidth=1.5, label='Theoritical BER')
    plt.xlabel("SNR (dB)")
    plt.ylabel("BER")
    plt.title(f"BER vs SNR over AWGN ({args.mod.upper()})")
    plt.grid(True, which="both")
    plt.legend()
    

    
    fig_path = results_dir / f"ber_{args.mod}.png"
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    
    plt.close()
    
    
if __name__ == "__main__":
    main()
    
    
       