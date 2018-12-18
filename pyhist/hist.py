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



def hist3d(table, px:int=20, shift:int=0):
    col = lambda n: table[n].reshape(-1,1)
    lim = lambda n: (col(n).min(), col(n).max())
    nbins = lambda limits: np.floor((limits[1] - limits[0])//px)
    xyz = np.concatenate(list(map(col,'zyx')),axis=1)
    limits = list(map(lim, 'zyx'))
    bins = list(map(nbins, limits))
    print(f'pixel: {px}')
    print(f'limits: {limits}')
    print(f'nbins: {bins}')
    hist, bins = np.histogramdd(xyz, bins=bins, range=limits)
    while shift: 
        shift -= 1
        hist = average_shift_hist(hist)
    return hist, bins

class IJroi:
    def __init__(self, path):
        roi = read_roi.read_roi_file(path)
        self.roi = roi
        specs = roi[list(roi)[0]]
        assert specs['type'] == 'rectangle'
        self.x = specs['left']
        self.y = specs['top']
        self.w = specs['width']
        self.h = specs['height']
        
    def __repr__(self):
        print(self.roi)
        
        
