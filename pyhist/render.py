import matplotlib.pyplot as plt
import numpy as np
import read_roi

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
        return f"roi.x={self.x}, roi.y={self.y}, roi.h={self.h}, roi.w={self.w}"
        

def show_crop_xy(hist, xy:tuple=(None,None), size=None, vmax=None, zx=False, zy=False, show=False):
    z_proj = hist.max(axis=0)
    if xy[0] and xy[1] and size:
        z_proj = z_proj[xy[1]-size//2: xy[1]+size//2, xy[0]-size//2: xy[0]+size//2]
    if show:
        plt.imshow(z_proj, 
               vmax=vmax, 
               cmap='hot')
        plt.show()

def show_crop_xz(hist, xz:tuple=(None,None), size=None, vmax=None, zx=False, zy=False, show=False):
    y_proj = hist.max(axis=1)
    if xz[0] and xz[1] and size:
        y_proj = y_proj[xz[1]-size//2: xz[1]+size//2, xz[0]-size//2: xz[0]+size//2]
    plt.imshow(y_proj, 
               vmax=vmax, 
               cmap='hot')
    if show: plt.show()

def show_crop_yz(hist, yz:tuple=(None,None), size=None, vmax=None, zx=False, zy=False, show=False):
    x_proj = hist.max(axis=2)
    if yz[0] and yz[1] and size:
        x_proj = x_proj[yz[1]-size//2: yz[1]+size//2, yz[0]-size//2: yz[0]+size//2]
    plt.imshow(x_proj.T, 
               vmax=vmax, 
               cmap='hot')
    if show: plt.show()

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
    

def show_crop_roi(hist:np.ndarray, roi:IJroi, z_lim=0, vmax=None, size=(3,3), title=None):
    print('hist shape: ', hist.shape)
    print('roi: ', roi)
    try:
        xy_crop = hist[:, roi.y:roi.y+roi.h, roi.x:roi.x+roi.w] 
    except TypeError as e:
        print('hist shape: ', hist.shape)
        print(roi)
        raise e
    xy_proj = xy_crop.max(axis=0)
    if z_lim:
        z_max = np.argmax(xy_crop.max(axis=(1,2)))
        zyx_proj = xy_crop[z_max-z_lim//2: z_max+z_lim//2]
    else:
        zyx_proj = xy_crop
    zx_proj = zyx_proj.max(axis=1)
    #zy_proj = zyx_proj.max(axis=2)
    render_xy_xz(xy_proj, zx_proj, vmax, size, title=title)

def render_xyz(xy_proj:np.ndarray, zy_proj:np.ndarray, zx_proj:np.ndarray, vmax=None, size=(5,5)):
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
    


def render_xy_xz(xy_proj:np.ndarray, zx_proj:np.ndarray, vmax=None, size=(5,5), title=None):
    fig = plt.figure(figsize=size)
    plt.title(title)
    fig.add_subplot(211)
    plt.imshow(xy_proj, 
               vmax=vmax, 
               cmap='hot')
    plt.title('xy')
    plt.axis('off')
    fig.add_subplot(212)
    plt.imshow(zx_proj, 
               origin='bottom', 
               vmax=vmax, 
               cmap='hot')
    plt.title('xz')
    plt.axis('off')
    
    plt.tight_layout()
    #plt.show()
    print('vmax = ', xy_proj.max())
    


