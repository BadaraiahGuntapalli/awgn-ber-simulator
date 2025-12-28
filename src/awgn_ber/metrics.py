"""
Metrics for digital communication simulations.
Currently: Bit Error Rate (BER).
"""

from __future__ import annotations
import numpy as np
import math

def ber(bits_tx: np.ndarray, bits_rx: np.ndarray) -> float:
    """
    Compute Bit Error Rate (BER) between transmitted and received bits.

    Args:
        bits_tx (np.ndarray): 
            Transmitted bits (1D array of 0s and 1s).
        bits_rx (np.ndarray): 
            Received bits, 1D array of {0, 1}. Must have same shape as bits_tx.
    Returns:
        float: Bit Error Rate (BER).
    """ 
    tx = np.asarray(bits_tx)
    rx = np.asarray(bits_rx)

    if tx.ndim != 1 or rx.ndim != 1:
        raise ValueError("bits_tx and bits_rx must be 1D arrays")
    if tx.size != rx.size:
        raise ValueError(f"Shape mismatch: bitstx has {tx.shape} bits, bits_rx has {rx.shape} bits")
    if tx.size == 0:
        raise ValueError("Cannot compute BER with empty arrays")

    # Convert to uint8 for robust comparison (also accepts bool/int)
    tx = tx.astype(np.uint8, copy=False)
    rx = rx.astype(np.uint8, copy=False)

    # Optional strict validation (uncomment if you want hard enforcement)
    if np.any((tx != 0) & (tx != 1)) or np.any((rx != 0) & (rx != 1)):
        raise ValueError("bits_tx must contain only 0s and 1s")
    
    errors = np.sum(tx != rx)
    ber_value = errors / tx.size
    return ber_value



def ser(symbols_tx: np.ndarray, symbols_rx: np.ndarray) -> float:
    """
    Optional: Symbol Error Rate (SER) for symbols (useful later).
    For QPSK/constellations, SER compares exact symbol values.

    Note: With noise, exact equality isn't meaningful unless you compare
    post-decision symbols. Keep this for later extensions.

    Provided as a placeholder utility.
    """
    tx = np.asarray(symbols_tx)
    rx = np.asarray(symbols_rx)

    if tx.ndim != 1 or rx.ndim != 1:
        raise ValueError("symbols_tx and symbols_rx must be 1D arrays")
    if tx.size != rx.size:
        raise ValueError("Shape mismatch between symbols_tx and symbols_rx")
    if tx.size == 0:
        raise ValueError("Cannot compute SER on empty arrays")

    errors = np.count_nonzero(tx != rx)
    return errors / tx.size


def qfunc(x: np.ndarray | float) -> np.ndarray | float:
    """
    Q-function: Q(x) = 0.5 * erfc(x / sqrt(2))
    Works for float or Numpy arrays.
    """
    x_arr = np.asarray(x, dtype=np.float64)
    erfc_vec = np.vectorize(math.erfc)
    return 0.5 * erfc_vec(x_arr / np.sqrt(2.0))

def ber_theory_bpsk_awgn(snr_db: np.ndarray | float, *, snr_def: str = "EsN0") -> np.ndarray:
    

    snr_db = np.asarray(snr_db, dtype=np.float64)
    snr = 10.0 ** (snr_db / 10.0)

    if snr_def not in {"EsN0", "EbN0"}:
        raise ValueError("snr_def must be 'EsN0' or 'EbNo'")
    
    return qfunc(np.sqrt(2.0 * snr))


def ber_theory_qpsk_awgn(snr_db: np.ndarray | float, *, snr_def: str = "EsN0") -> np.ndarray:
    snr_db = np.asarray(snr_db, dtype=np.float64)
    snr_es = 10.0 ** (snr_db / 10.0)

    if snr_def == "EbN0":
        ebno = snr_es
    elif snr_def == "EsN0":
        ebno = snr_es / 2.0
    else:
        raise ValueError("snr_def must be 'EsN0' or 'EbN0' ")
    
    return qfunc(np.sqrt(2.0 * ebno))