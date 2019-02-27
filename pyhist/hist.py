import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from pyhist.iotools import import_zola
import read_roi
import logging

logger = logging.getLogger(__name__)



def get_hist_zola(path, px=20, shift=1):
    print(f'reading {path}')
    table = import_zola(path)


def get_hist3d(zyx, px:int=20, shift:int=0):
    return hist3d(zyx, px, shift)[0]

def average_shift_hist(a):
    for i in range(a.ndim):
        a = ndimage.convolve1d(a,(1,2,1),i)
    return a

def get_zyx_from_zola(zola_table:np.ndarray):
    col = lambda n: zola_table[n].reshape(-1,1)
    zyx = np.concatenate(list(map(col,'zyx')),axis=1)
    return zyx

def hist3d(zyx, px:int=20, shift:int=0):
    '''
    Generates 3D histogram using numpy with given px and shift.
    Returns histogram, bins
    '''
    if px <=0: raise(ValueError(f'px must be positive number, got {px}'))
    min_lim = zyx.min(axis=0)
    max_lim = zyx.max(axis=0)
    limits = list(zip(min_lim, max_lim))
    bins = list(np.floor((max_lim - min_lim)/px))
    logger.debug(f'pixel: {px}')
    logger.debug(f'limits: {limits}')
    logger.debug(f'nbins: {bins}')
    hist, bins = np.histogramdd(zyx, bins=bins, range=limits)
    logger.debug(f'hist shape: {hist.shape}')
    while shift: 
        shift -= 1
        hist = average_shift_hist(hist)
    return hist, bins

def hist2d(xy, px:int=20, shift:int=0, plot=False, vmax=None, cmap='hot'):
    '''
    Generates 2D histogram using numpy with given px and shift.
    Returns histogram, bins
    '''
    if px <=0: raise(ValueError(f'px must be positive number, got {px}'))
    logger.debug(f'data shape: {xy.shape}')
    assert xy.shape[0] > 0, 'data empty'
    assert xy.shape[1] == 2, 'data shape wrong'
    min_lim = xy.min(axis=0)
    max_lim = xy.max(axis=0)
    
    limits = list(zip(min_lim, max_lim))
    
    bins = list(np.floor((max_lim - min_lim)/px))
    
    logger.debug(f'pixel: {px}')
    logger.debug(f'limits: {limits}')
    logger.debug(f'nbins: {bins}')
    
    hist, xedges, yedges = np.histogram2d(x=xy[:,0].ravel(), y=xy[:,1].ravel(), bins=bins, range=limits)
    logger.debug(f'hist shape: {hist.shape}')
    while shift: 
        shift -= 1
        hist = average_shift_hist(hist)

    if plot:
        import itertools
        merged = list(itertools.chain(*limits))
        try:
            plt.imshow(hist,
                       cmap=cmap,
                       vmax=vmax,
                       interpolation=None,
                       extent=[i/1000. for i in merged])
            plt.xlabel('x, µm')
            plt.ylabel('y, µm')
            plt.axis('square')
            plt.colorbar()
            plt.show()
        except ValueError as e:
            print('plot canceled: ', e)
            print(f'merged bins: {merged}')

    return hist, limits


def hist_from_zola_table(zola_table, px:int=20, shift:int=0):
    zyx = get_zyx_from_zola(zola_table)
    hist, bins = hist3d(zyx, px, shift)
    return hist, bins