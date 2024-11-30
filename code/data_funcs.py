# Functions to calculate range and choose best deep space dish to use
import numpy as np

def find_best_dsn(sat_dsn_ranges,dsn_viz,dsn_antennas):
    Pt = 10 # dBW
    Gt = 9 # dBi
    losses = 19.43 # dB
    eta = 0.55 # efficiency gain
    lambda_t = 0.136363636 # m, wavelength
    kB = 228.6 # dBW/K/Hz Boltzmann Constant (in Decibel Watts per degree Kelvin per Hertz, dBW/K/Hz)
    Ts = 22 # K

    bitrate = np.zeros((np.size(sat_dsn_ranges,0), np.size(sat_dsn_ranges,1)))
    for (i, slant_ranges) in enumerate(sat_dsn_ranges):
        for (j, slr) in enumerate(slant_ranges):
            if (dsn_viz[i][j] > 0 and slr):
                dB_part1 = Pt + Gt - losses + 10.0*np.log10(eta*(np.pi*dsn_antennas[j]/lambda_t)**2)
                dB_part2 = 20.0*np.log10(4000*slr) + kB + 10.0*np.log10(Ts)
                bitrate[i][j] = 10**((1/10.0)*(dB_part1 - dB_part2))/1000.0
            else:
                bitrate[i][j] = 0.0

    return(bitrate)