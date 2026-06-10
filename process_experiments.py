import numpy as np
from scipy.io import loadmat
import h5py
import os
from util_exp import *
import matplotlib.pyplot as plt

# later matlab data files might just be hdf5

# list of comparison plots to make, supplying settings in dict
# NOTE: loc coordinates provided relative to 2d tps coordinate system
# NOTE: don't actually seem to have the exit data, PIV goes up to below the nozzle
# Best to ask where the coordinates actually are
comp_data = [
    # {
    #     "name": "axial_max_swirl",
    #     "dir": "axial",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.0,                      # line to slice data along
    #     "loc": 0.022,                      # line to slice data along
    #     "range": [0., 0.34],            # line to slice data along
    #     "val": "velocity_z",                 # quantity to plot
    #     "vtype": "max"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },

    {
        "name": "exit_swirl",
        "dir": "transverse",                 # indicate plot along torch flow direction or transverse
        # "loc": 0.321,                       # line to slice data along
        "loc": 0.265,                       # line to slice data along
        "range": [0., 0.02804],             # line to slice data along
        "val": "velocity_z",                 # quantity to plot
        "vtype": "line"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    }
]

home = os.getenv('HOME')

file_exp = home + "/torch_experiments/pivLinesBasic/fullFlowfield"
filenames = ['AboveInlet.mat', 'BelowStep.mat', 'AboveStep.mat', 'BelowNozzle.mat']

file_3d = home + "/bedonian1/fullTorch_cold_Field_Sigfried/data.pvtu" 
file_2d = [home + "/bedonian1/mean_tps2d_newmesh/mean_tps2d_v2_hot_down1cm/output-torch-cold-v2-rm13-3dtke-5/output-torch-colv-v2-rm13-3dtke.pvd",
]

# process experimental data (including conversion to meters)
e_toss = 30 # piv data removal
e_yshift = 0.138201
e_nsamp = 2000
data_exp_ind = {}
data_exp_dict = {}
# for file in os.listdir(file_exp):
for file in filenames:
    if file.endswith(".mat"):
        data_exp_ind[file] = loadmat(file_exp + "/" + file)[file[:-4]][0][0]

        # y shift, convert coord to meters
        data_exp_ind[file]['x'] = data_exp_ind[file]['x']/1000.
        data_exp_ind[file]['y'] = data_exp_ind[file]['y']/1000.  + e_yshift

        # remove bad piv points
        data_exp_ind[file]['x'] = data_exp_ind[file]['x'][:,e_toss:-e_toss]
        data_exp_ind[file]['zerodeg']['vx'][0][0] = data_exp_ind[file]['zerodeg']['vx'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['zerodeg']['vy'][0][0] = data_exp_ind[file]['zerodeg']['vy'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['zerodeg']['vz'][0][0] = data_exp_ind[file]['zerodeg']['vz'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['p60deg']['vx'][0][0] = data_exp_ind[file]['p60deg']['vx'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['p60deg']['vy'][0][0] = data_exp_ind[file]['p60deg']['vy'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['p60deg']['vz'][0][0] = data_exp_ind[file]['p60deg']['vz'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['m60deg']['vx'][0][0] = data_exp_ind[file]['m60deg']['vx'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['m60deg']['vy'][0][0] = data_exp_ind[file]['m60deg']['vy'][0][0][e_toss:-e_toss,:]
        data_exp_ind[file]['m60deg']['vz'][0][0] = data_exp_ind[file]['m60deg']['vz'][0][0][e_toss:-e_toss,:]

        # replicating averaging from matlab script
        data_exp_dict[file[:-4]] = {}
        data_exp_dict[file[:-4]]['x'] = data_exp_ind[file]['x']
        data_exp_dict[file[:-4]]['y'] = data_exp_ind[file]['y']
        data_exp_dict[file[:-4]]['velocity_x'] = (data_exp_ind[file]['zerodeg']['vx'][0][0] +  data_exp_ind[file]['p60deg']['vx'][0][0] +  data_exp_ind[file]['m60deg']['vx'][0][0])/3.0
        data_exp_dict[file[:-4]]['velocity_y'] = (data_exp_ind[file]['zerodeg']['vy'][0][0] +  data_exp_ind[file]['p60deg']['vy'][0][0] +  data_exp_ind[file]['m60deg']['vy'][0][0])/3.0
        data_exp_dict[file[:-4]]['velocity_z'] = (data_exp_ind[file]['zerodeg']['vz'][0][0] +  data_exp_ind[file]['p60deg']['vz'][0][0] +  data_exp_ind[file]['m60deg']['vz'][0][0])/3.0

# TODO: line slicing scheme for data

for comp in comp_data:

    data_in_keys = []

    if comp['dir'] == "axial":
        slice_dir = 'y'
        loc_dir = 'x'
        # find which datasets (multiple) we live in

        # in this case, loc is in all sets, but we need to see which sets the range extends through
        for key in data_exp_dict.keys():
            if contains_in_range(comp['range'], data_exp_dict[key]['y'][0]):
                if lies_in_range(comp['loc'], data_exp_dict[key]['x'][0]):
                    data_in_keys.append(key)

    elif comp['dir'] == "transverse":
        slice_dir = 'x'
        loc_dir = 'y'

        # find which dataset we live in
        for key in data_exp_dict.keys():
            if lies_in_range(comp['loc'], data_exp_dict[key]['y'][0]):
                data_in_keys.append(key)
                break

    
    # linear interpolation of slice line
    e_xp = []
    e_yp = []
    for key in data_in_keys:
        base = data_exp_dict[key]
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

    # plot
    for i in range(len(e_xp)):
        plt.plot(e_xp[i], e_yp[i], color='k')

    plt.grid()
    plt.xlabel(f"{slice_dir} (m)")
    plt.ylabel(f"{comp['vtype']} {comp['val']} (m/s)")
    plt.savefig(f"plots/exp_{comp['name']}_{comp['loc']}.png", bbox_inches='tight', dpi=400)
    plt.clf()
    breakpoint()

# NOTE: next are to overlay uncertainty, and 3d/2d tps solves