# ME 144L DSC Lab
# Tools based on FFT
import numpy as np
import scipy.fftpack
from scipy.signal import find_peaks

def compare_modes(t,z,zmin):
    #  to compare the magnitude of each response
    Na = len(t)
    dt = t[1]-t[0]
    df = 1/(Na*dt)
    fmax = Na*df//2
    ff = np.linspace(0.0, fmax, Na//2)
    z_mean = np.mean(z)
    z_c = [zc - z_mean for zc in z]
    Z = scipy.fftpack.fft(z_c)
    # compute the one-sided autospectral density
    G = (2.0/Na) * np.abs(Z[:Na//2])
    # the following returns indices in an ndarray
    peak_indices, _ = find_peaks(G, height=zmin)
    # to create a list of these indices
    npk = [peak_indices[i] for i in range(len(peak_indices))]
    # and then freq and angle lists for just the peaks
    fp = [ff[npk[i]] for i in range(len(npk))]
    Gp = [G[npk[i]] for i in range(len(npk))]

    return fp, Gp