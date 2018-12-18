import numpy as np
import pandas as pd

def import_zola(path):
    dtype = dict(id='float',
             frame='float',
             x='float',
             y='float',
             z='float',
             intensity='float',
             background='float',
             chi2='float',
             crlbX='float',
             crlbY='float',
             crlbZ='float',
             driftX='float',
             driftY='float',
             driftZ='float',
             occurrenceMerging='float'
                )
    return np.loadtxt(path, delimiter=',', skiprows=1, dtype=[(i, v) for i,v in zip(dtype,dtype.values())])

def import_csv(path):
    return pd.read_csv(path)