
import numpy as np
from util_exp import *

def process_exp(comp, data_exp):

    data_in_keys = []

    if comp['dir'] == "axial":
        slice_dir = 'y'
        loc_dir = 'x'
        # find which datasets (multiple) we live in

        # in this case, loc is in all sets, but we need to see which sets the range extends through
        for key in data_exp.keys():
            if contains_in_range(comp['range'], data_exp[key]['y'][0]):
                if lies_in_range(comp['loc'], data_exp[key]['x'][0]):
                    data_in_keys.append(key)

    elif comp['dir'] == "transverse":
        slice_dir = 'x'
        loc_dir = 'y'

        # find which dataset we live in
        for key in data_exp.keys():
            if lies_in_range(comp['loc'], data_exp[key]['y'][0]):
                data_in_keys.append(key)
                break

    
    # linear interpolation of slice line
    e_xp = []
    e_yp = []
    for key in data_in_keys:
        base = data_exp[key]
        loc_ind = np.searchsorted(base[loc_dir][0], comp['loc'])
        wt =  (comp['loc'] - base[loc_dir][0][loc_ind-1]) / (base[loc_dir][0][loc_ind] - base[loc_dir][0][loc_ind-1])
        yw = base[comp["val"]]
        if comp['dir'] == "axial":
            yw = yw.T

        e_xp.append(base[slice_dir][0])
        if comp["vtype"] == "max":
            e_yp.append(np.max(abs(yw), axis=1))
        elif comp["vtype"] == "avg":
            e_yp.append(np.avg(yw, axis=1))
        else: # comp["vtype"] == "line"
            e_yp.append(wt*yw[:,loc_ind-1] + (1-wt)*yw[:,loc_ind])
    
    # e_xp = np.concatenate(e_xp)
    # e_yp = np.concatenate(e_yp)
        # remove invalid
        mask =  abs(e_yp[-1]) > 1e-10
        e_xp[-1] = e_xp[-1][mask]
        e_yp[-1] = e_yp[-1][mask]

    return e_xp, e_yp