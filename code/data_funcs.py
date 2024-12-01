# Functions to calculate range and choose best deep space dish to use
# 3 input elements
# sat_dsn_ranges gives ranges for the four different antennae, some of them NaNs, so it is 2D matrix
#   rows are time in minutes, cols are 'WPSA', 'DS54', 'DS24', 'DS34'
# dsn_viz is the same, except instead of ranges, it gives 1 if visible, 0 if not
# dsn_antennas are the diameters of the dishes in the same order
# 1 output array
# bitrate gives bitrate in kbps with rows are time in minutes and columns are the four dishes
# Does not do cutoff where can't go above 10 Mbps
import numpy as np

def find_best_dsn(sat_dsn_ranges,dsn_viz,dsn_antennas):
    Pt = 10 # dBW
    Gt = 9 # dBi
    losses = 19.43 # dB
    eta = 0.55 # efficiency gain
    lambda_t = 0.136363636 # m, wavelength
    kB = -228.6 # dBW/K/Hz Boltzmann Constant (in Decibel Watts per degree Kelvin per Hertz, dBW/K/Hz)
    Ts = 22 # K

    bitrate = np.zeros((np.size(sat_dsn_ranges,0), np.size(sat_dsn_ranges,1)))
    for (i, slant_ranges) in enumerate(sat_dsn_ranges):
        for (j, slr) in enumerate(slant_ranges):
            if (dsn_viz[i][j] > 0 and slr):
                dB_part1 = Pt + Gt - losses + 10.0*np.log10(eta*(np.pi*dsn_antennas[j]/lambda_t)**2)
                dB_part2 = 20.0*np.log10(4000*np.pi*slr/lambda_t) + kB + 10.0*np.log10(Ts)
                bitrate[i][j] = 10**((1/10.0)*(dB_part1 - dB_part2))/1000.0
            else:
                bitrate[i][j] = 0.0

    return(bitrate)