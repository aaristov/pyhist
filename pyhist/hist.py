import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from pyhist.iotools import import_zola
import read_roi


def get_hist(path, shift=1):
    print(f'reading {path}')
    table = import_zola(path)
    
    hist, _ = hist3d(table)
    while shift:
        hist = average_shift_hist(hist)
        shift -=1
    return hist


def average_shift_hist(a):
    for i in range(a.ndim):
        a = ndimage.convolve1d(a,(1,2,1),i)
    return a

def get_zyx_from_zola(zola_table:np.ndarray):
    col = lambda n: zola_table[n].reshape(-1,1)
    zyx = np.concatenate(list(map(col,'zyx')),axis=1)
    return zyx

def hist3d(zyx, px:int=20, shift:int=0):
    min_lim = zyx.min(axis=0)
    max_lim = zyx.max(axis=0)
    limits = zip(min_lim, max_lim)
    bins = np.floor((max_lim - min_lim)//px)
    print(f'pixel: {px}')
    print(f'limits: {limits}')
    print(f'nbins: {bins}')
    hist, bins = np.histogramdd(zyx, bins=bins, range=limits)
    while shift: 
        shift -= 1
        hist = average_shift_hist(hist)
    return hist, bins


def hist3d_from_zola_table(zola_table, px:int=20, shift:int=0):
    zyx = get_zyx_from_zola(zola_table)
    hist3d(zyx, px, shift)

    