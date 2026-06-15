
import numpy as np
from util_exp import *

def process_exp_uncertainty(comp, e_xp, data_exp_unc):


    if comp['dir'] == "axial":
        slice_dir = 'y'
        loc_dir = 'x'


    elif comp['dir'] == "transverse":
        slice_dir = 'x'
        loc_dir = 'y'

    
    # linear interpolation of slice line, which are the supplied experimental lines
    e_upx = [] # must interpolate from this
    e_up = [] # plus-minus value
    for line in e_xp:

        loc_ind = np.searchsorted(data_exp_unc[loc_dir][0], comp['loc'])
        wt =  (comp['loc'] - data_exp_unc[loc_dir][0][loc_ind-1]) / (data_exp_unc[loc_dir][0][loc_ind] - data_exp_unc[loc_dir][0][loc_ind-1])
        yw = data_exp_unc[comp["val"]]
        if comp['dir'] == "axial":
            yw = yw.T

        e_upx.append(data_exp_unc[slice_dir][0])
        # find end points
        start = np.searchsorted(data_exp_unc[slice_dir][0], line[0])
        end = np.searchsorted(data_exp_unc[slice_dir][0], line[-1])

        if comp["vtype"] == "max":
            # find uncertainty at the max
            # e_up.append(np.max(abs(yw[start:end,:]), axis=1))
            # NOTE: don't have the max arg location yet
            # interpret as average uncertainty
            e_up.append(np.nanmean(yw[start:end,:], axis=1))
        elif comp["vtype"] == "avg":
            # interpret as average uncertainty
            e_up.append(np.nanmean(yw[start:end,:], axis=1))
        else: # comp["vtype"] == "line"
            e_up.append(wt*yw[start:end,loc_ind-1] + (1-wt)*yw[start:end,loc_ind])
    
        e_up[-1][np.isnan(e_up[-1])] = 0.0
        # breakpoint()
        e_up[-1] = np.interp(line, data_exp_unc[slice_dir][0][start:end], e_up[-1])
        e_up[-1][e_up[-1] < 0.0] = 0.0

        # remove invalid
        # mask =  abs(e_up[-1]) > 1e-10
        # e_up[-1] = e_up[-1][mask]

    return e_xp, e_up