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
    '''Loads csv table with pandas'''
    table = pd.read_csv(path)
    return table

def get_zyx_array(pd_table):
    try:
        expected = ['frame', 'x [nm]', 'y [nm]', 'z [nm]']
        for v in expected:
            assert v in pd_table.columns.values, f'{v} column is missing. Table must contain {expected} columns'
    except AssertionError:
        print(f'{v} column is missing. Table must contain {expected} columns')
        return False 
    return pd_table[expected[-1:0:-1]].values
