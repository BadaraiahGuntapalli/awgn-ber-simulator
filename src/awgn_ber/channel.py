"""
AWGN channel utilities.

Conventions (aligned with modulation.py):
-BPSK symbols: real-valued, Es=1 (symbols in {-1.0, +1.0}).
-QPSK symbols: complex-valued, Es=1 (Gray mapping, normalized by sqrt(2)).

We interpret the provided SNR as Es/N0 (symbol SNR) under Es=1. 


Noise:
- For real (BPSK), n ~ N(0, sigma2) where sigma2 = 1 / (2 * SNR_linear)
- For complex (QPSK), n ~ CN(0, sigma2) where sigma2 = 1 / (2 * SNR_linear)
    i.e., each of the real and imaginary parts has variance sigma2/2.
    
"""


from __future__ import annotations
import numpy as np


def snr_db_to_linear(snr_db: float | np.ndarray) -> float | np.ndarray:
    """ Convert SNR from dB to linear scale."""
    return np.power(10.0, np.asarray(snr_db, dtype=np.float64)/10.0)


def noise_variance_awgn(snr_db: float, *, complex_noise: bool)-> float:
    """
    Compute AWGN noise variance given SNR in dB.

    Args:
        snr_db (float): SNR in dB (interpreted as Es/N0 with Es=1)
        complex_noise (bool): 
        - If True, return variance for complex circular noise CN(0, sigma2).
        - If False, return variance for real noise N(0, sigma2).
    Returns:
        float: Noise variance sigma^2.
    """
    
    snr_lin = float(snr_db_to_linear(snr_db))
    if snr_lin <= 0.0:
        raise ValueError("snr_db must correpond to a positve linear SNR")
    
    if complex_noise:
        # CN(0, sigma2) -> E[|n|^2] = sigma2, Re/Im var = sigma2/2
        return 1.0/snr_lin
    else:
        # N(0, sigma2) for real BPSK with Es=1: sigma2 = N0/2 = 1/(2*SNR)
        return 1.0/(2.0 * snr_lin)
    
def awgn(
        x: np.ndarray,
        snr_db: float,
        rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Pass signal x through AWGN channel at given SNR (dB)
    
    If x is complex -> used complex circular AWGN.
    if x is real -> uses real AWGN.

    Args:
        x (np.ndarray): Input signal (1D array). Can be real or complex.
        snr_db (float): SNR in dB (interpreted as Es/N0 with Es=1)
        rng (np.random.Generator | None, optional
        Random generator for reproducibility. If None, uses default_rng().

    Returns:
        np.ndarray: Noisy observation y = x + n, same dtype kind as x.
    """
    x = np.asarray(x)
    if x.ndim != 1:
        raise ValueError("x must be a 1D array")
    
    if rng is None:
        rng = np.random.default_rng()
        
    if np.iscomplexobj(x):
        sigma2 = noise_variance_awgn(snr_db, complex_noise=True)
        sigma = np.sqrt(sigma2 / 2.0) 
        n = rng.normal(0.0, sigma, size=x.shape) + 1j * rng.normal(0.0, sigma, size=x.shape)
        return (x.astype(np.complex128, copy=False) + n.astype(np.complex128))
    else:
        sigma2 = noise_variance_awgn(snr_db, complex_noise=False)
        sigma = np.sqrt(sigma2)
        n = rng.normal(0.0, sigma, size=x.shape)
        return x.astype(np.float64, copy=False) + n.astype(np.float64)
    
    
    