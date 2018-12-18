import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


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

    def show_crop_xy(hist, xy:tuple, size=20, vmax=None, zx=False, zy=False):
        plt.imshow(hist.max(axis=0)[xy[1]-size//2: xy[1]+size//2, xy[0]-size//2: xy[0]+size//2], 
               vmax=vmax, 
               cmap='hot')
    plt.show()

def show_crop_xyz(hist, yx:tuple=None, crop=20, vmax=None, size=(5,5), origin='center'):
    if origin=='center': a, b = crop//2, crop//2
    elif origin=='corner': a, b = 0, crop
    else: raise(ValueError)
    y,x = yx
    xy_crop = hist[:, y-a: y+b, x-a: x+b] 
    xy_proj = xy_crop.max(axis=0)
    
    z_max = np.argmax(xy_crop.max(axis=(1,2)))
    zyx_proj = xy_crop[z_max-crop//2: z_max+crop//2]
    zx_proj = zyx_proj.max(axis=1)
    zy_proj = zyx_proj.max(axis=2)
    render_xyz(xy_proj, zy_proj, zx_proj, vmax, size)
    
class IJroi:
    def __init__(self, path):
        roi = read_roi.read_roi_file(path)
        specs = roi[list(roi)[0]]
        assert specs['type'] == 'rectangle'
        self.x = specs['left']
        self.y = specs['top']
        self.w = specs['width']
        self.h = specs['height']
        
    def __repr__(self):
        print(roi)
        
        
def show_crop_roi(hist, roi:IJroi, z_lim=0, vmax=None, size=(10,3)):
    xy_crop = hist[:, roi.y:roi.y+roi.h, roi.x:roi.x+roi.w] 
    xy_proj = xy_crop.max(axis=0)
    if z_lim:
        z_max = np.argmax(xy_crop.max(axis=(1,2)))
        zyx_proj = xy_crop[z_max-z_lim//2: z_max+z_lim//2]
    else:
        zyx_proj = xy_crop
    zx_proj = zyx_proj.max(axis=1)
    zy_proj = zyx_proj.max(axis=2)
    render_xy_xz(xy_proj, zx_proj, vmax, size)

def render_xyz(xy_proj, zy_proj, zx_proj, vmax=None, size=(5,5)):
    fig = plt.figure(figsize=size)
    
    fig.add_subplot(221)
    plt.imshow(xy_proj, 
               vmax=vmax, 
               cmap='hot')
    plt.title('xy')
    plt.axis('off')
    fig.add_subplot(222)
    plt.imshow(zy_proj.T, 
               vmax=vmax, 
               cmap='hot')
    plt.title('zy')
    plt.axis('off')
    
    fig.add_subplot(223)
    plt.imshow(zx_proj, 
               origin='bottom', 
               vmax=vmax, 
               cmap='hot')
    plt.title('xz')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    print('vmax = ', xy_proj.max())
    


def render_xy_xz(xy_proj, zx_proj, vmax=None, size=(5,5)):
    fig = plt.figure(figsize=size)
    
    fig.add_subplot(121)
    plt.imshow(xy_proj, 
               vmax=vmax, 
               cmap='hot')
    plt.title('xy')
    plt.axis('off')
    fig.add_subplot(122)
    plt.imshow(zx_proj, 
               origin='bottom', 
               vmax=vmax, 
               cmap='hot')
    plt.title('xz')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    print('vmax = ', xy_proj.max())
    


