"""
Docstring for awgn_ber.modulation
Modulaation and demodulation blocks for AWGN BER simulations.

Conventions:
- Bits are numpy arrays of dtype uint8 containing {0, 1}.
- BPSK symbols are real float64 values in {-1.0, +1.0}.
- QPSK symbols are complex128 with Gray mapping and unit average symbol energy (Es=1).

QPSK Gray mapping (2 bits -> 1 symbol):
    b0 b1 : symbol
    0  0  : +1 + j
    0  1  : -1 + j
    1  1  : -1 - j
    1  0  : +1 - j

Normalization: divide by sqrt(2) so Es = E[|s|^2] = 1.
"""

from __future__ import annotations


import numpy as np

def _validate_bits(bits: np.ndarray) -> np.ndarray:
    """
    Args:
        bits (np.ndarray): 
            Input of shape (N,).

    Raises:
        ValueError: bits must be a 1D array of shape (N,)
        ValueError: bits array must contain only 0s and 1s

    Returns:
        np.ndarray: 
            bits of shape (N,), values in {0, 1}.
    """
    bits = np.asarray(bits)
    if bits.ndim != 1:
        raise ValueError("bits must be a 1D array of shape (N,)")
    # Accept bool or integer, convert to uint8
    if bits.dtype == np.bool_:
        bits = bits.astype(np.uint8)
    else:
        bits = bits.astype(np.uint8, copy=False)

    if np.any((bits != 0) & (bits != 1)):
        raise ValueError("bits array must contain only 0s and 1s")
    return bits

def bpsk_modulate(bits: np.ndarray) -> np.ndarray:
    """
    BPSK modulation.

    Parameters
    ----------
    bits : np.ndarray
        Input bits of shape (N,).

    Returns
    -------
    np.ndarray
        BPSK symbols of shape (N,), values in {-1.0, +1.0}.
    """
    bits = _validate_bits(bits)
    symbols = 1.0 - 2.0 * bits.astype(np.float64)
    return symbols

def bpsk_demodulate(symbols: np.ndarray) -> np.ndarray:
    """
    BPSK demodulation.

    Parameters
    ----------
    symbols : np.ndarray
        BPSK symbols of shape (N,), values in {-1.0, +1.0}.

    Returns
    -------
    np.ndarray
        Demodulated bits of shape (N,).
    """
    symbols = np.asarray(symbols, dtype=np.float64)
    if symbols.ndim != 1:
        raise ValueError("symbols must be a 1D array of shape (N,)")
    bits = (symbols < 0).astype(np.uint8)
    return bits

def qpsk_modulate(bits: np.ndarray) -> np.ndarray:
    """
    QPSK modulation with Gray mapping and unit average symbol energy.

    Parameters
    ----------
    bits : np.ndarray
        Input bits of shape (N,), where N is even.

    Returns
    -------
    np.ndarray
        QPSK symbols of shape (N/2,), complex128 with unit average symbol energy.
    """
    bits = _validate_bits(bits)
    if bits.size % 2 != 0:
        raise ValueError("Number of bits must be even for QPSK modulation")
    
    bit_pairs = bits.reshape(-1, 2)
    mapping = {
        (0, 0): 1 + 1j,
        (0, 1): -1 + 1j,
        (1, 1): -1 - 1j,
        (1, 0): 1 - 1j,
    }
    
    symbols = np.array([mapping[tuple(pair)] for pair in bit_pairs], dtype=np.complex128)
    symbols /= np.sqrt(2.0) # Normalize to unit average symbol energy
    return symbols


def qpsk_demodulate(symbols: np.ndarray) -> np.ndarray:
    """
    Hard-decision Gray-coded QPSK demodulation.
    
    Parameters
    ----------
    symbols : np.ndarray
        QPSK symbols of shape (N/2,), complex128.
    Returns
    ------- 
    np.ndarray
        Demodulated bits of shape (N,).
    """
    s = np.asarray(symbols, dtype=np.complex128)
    if s.ndim != 1:
        raise ValueError("symbols must be a 1D array")

    # Undo normalization (optional, decision works either way)
    s = s * np.sqrt(2.0)

    real = np.real(s)
    imag = np.imag(s)

    b0 = (imag < 0).astype(np.uint8)
    b1 = (real < 0).astype(np.uint8)

    bits = np.empty(2 * s.size, dtype=np.uint8)
    bits[0::2] = b0
    bits[1::2] = b1
    return bits

    
    
    
def modulate(bits: np.ndarray, scheme:str) -> np.ndarray:
    """
    General modulation dispatcher.
    scheme: 'bpsk' or 'qpsk'

    """
    scheme = scheme.lower().strip()
    if scheme == 'bpsk':
        return bpsk_modulate(bits)
    
    if scheme == 'qpsk':
        return qpsk_modulate(bits)
    
    raise ValueError(f"Unsupported modulation scheme: {scheme}")


def demodulate(symbols: np.ndarray, scheme:str) -> np.ndarray:
    """
    General demodulation dispatcher.
    scheme: 'bpsk' or 'qpsk'

    """
    scheme = scheme.lower().strip()
    if scheme == 'bpsk':
        return bpsk_demodulate(symbols)
    
    if scheme == 'qpsk':
        return qpsk_demodulate(symbols)
    
    raise ValueError(f"Unsupported modulation scheme: {scheme}")