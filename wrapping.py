# @author: Micha Burkhardt, 27.05.2020
# This script contains a simple Python implementation of the "wrapping" method from the cellWise R-toolbox: https://cran.r-project.org/web/packages/cellWise/index.html
# It is licensed under the GPL V3 License.
# Please check the README before using this script!

import numpy as np
from math import sqrt, tanh, ceil
from scipy import stats

###############################
# Main functions
###############################

# Splits the array into individual columns and performs the wrapping with the corresponding location and scale parameters
def wrap(x, params=1):
    """
    Main function
    inputs:
        x: time series as a (n,d) array (n timepoints, d dimensions)
        params: [1,2,3] for parameter sets used in the manuscript
    
    returns: Wrapped time series, location and scale
    """
    b=1.5; c=4.0; k = 4.1517212; A = 0.7532528; B = 0.8430849

    if params == 2:
        b=1.25; c= 3.5; k = 3.856305; A = 0.6119228; B = 0.7354239
    elif params == 3:
        b=1.25; c = 3.0; k = 4.357096; A = 0.5768820; B = 0.6930791

    xW = np.zeros(x.shape)
    try:
        loc = np.zeros(x.shape[1])
        scale = np.zeros(x.shape[1])
        for i in range(x.shape[1]):
            l, s = estLocScale(x[:,i], b, c, k, A, B)
            loc[i] = l
            scale[i] = s
            xW[:,i] = perform_wrapping(x[:,i], loc[i], scale[i], b, c, k, A, B)

    except:
        loc = np.zeros(1)
        scale = np.zeros(1)
        l, s = estLocScale(x, b, c, k, A, B)
        loc = l
        scale = s
        xW = perform_wrapping(x, loc, scale, b, c, k, A, B)

    return xW, loc, scale

# Robust location and scale parameters
def estLocScale(x, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):
    m1 = loc1StepM(x, b, c, k, A, B)
    s1 = scale1StepM(x-m1, b, c, k, A, B)

    return m1,s1

# Performs the wrapping with the psiTanh function
def perform_wrapping(x, loc, scale, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):
    u = x - loc
    u = u / scale
    xW = psiTanh(u, b, c, k, A, B)
    xW = xW * scale + loc

    return xW

###############################
# Scale
###############################

def scale1StepM(x, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):
    s0 = 1.482602218505602 * np.median(abs(x))
    rho = x / s0
    w = rhoTanh154(rho, b, c, k, A, B)
    s1 = s0 * sqrt(sum(w) / (0.5 * len(x))) 
    
    cn = len(x) / (len(x) - 1.208) # finite sample correction

    s1 *= cn
    return s1

# Hyperbolic tangent rho function
def rhoTanh154(x, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):  
    x = psiTanh(x, b, c, k, A, B)
    x = pow(x,2) / 1.506506

    return x

# Psi-function of the hyperbolic tangent estimator. Default k, A, B for b= 1.5 and c=4.0
def psiTanh(x, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):    
    for i in range(len(x)):  
        x[i] = 0.0 if abs(x[i]) > c else x[i]
    
    for i in range(len(x)):                                                
        x[i] = sqrt(A*(k-1.0)) * tanh(0.5*sqrt((k-1.0)*pow(B,2.0)/A) * (c - abs(x[i]))) * np.sign(x[i]) if abs(x[i]) > b else x[i]

    return x

###############################
# Location
###############################

def loc1StepM(x, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):
    med = np.median(x)
    mad = stats.median_abs_deviation(x, scale='normal')
    z = (x-med)/mad
    weights = locTanh154(z, b, c, k, A, B)
    mu = sum(x*weights) / sum(weights)

    return mu

# Hyperbolic Tangent weight function to be used in location M-estimators
def locTanh154(x, b=1.5, c=4.0, k=4.1517212, A=0.7532528, B=0.8430849):
    for i in range(len(x)):
        if abs(x[i]) < b:
            x[i] = 1.0
        elif abs(x[i]) > c:
            x[i] = 0.0
        else:
            x[i] = sqrt(A*(k-1.0)) * tanh(0.5*sqrt((k-1.0)*pow(B,2.0)/A) * (c - abs(x[i]))) / abs(x[i])

    return x