import numpy as np
from scipy.io import loadmat
import h5py
import os
from util_exp import *
import matplotlib.pyplot as plt

from process_experiments import process_exp#, setup_exp
from process_exp_uncertainty import process_exp_uncertainty
from process_tps2d import process_tps2d
from process_tps3d import process_tps3d

# later matlab data files might just be hdf5

# list of comparison plots to make, supplying settings in dict
# NOTE: loc coordinates provided relative to 2d tps coordinate system
# NOTE: don't actually seem to have the exit data, PIV goes up to below the nozzle
# Best to ask where the coordinates actually are
comp_data = [
    
    # {
    #     "name": "exit_swirl",
    #     "dir": "transverse",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.321,                       # line to slice data along
    #     "loc": 0.265,                       # line to slice data along
    #     "range": [0., 0.02804],             # line to slice data along
    #     "val": "velocity_z",                 # quantity to plot
    #     "vtype": "line"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },
    # {
    #     "name": "core_swirl",
    #     "dir": "transverse",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.321,                       # line to slice data along
    #     "loc": 0.119,                       # 5mm
    #     "range": [0., 0.02804],             # line to slice data along
    #     "val": "velocity_z",                 # quantity to plot
    #     "vtype": "line"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },
    # {
    #     "name": "core_y",
    #     "dir": "transverse",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.321,                       # line to slice data along
    #     "loc": 0.119,                       # 5mm
    #     "range": [0., 0.02804],             # line to slice data along
    #     "val": "velocity_y",                 # quantity to plot
    #     "vtype": "line"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },
    # {
    #     "name": "exit_y",
    #     "dir": "transverse",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.321,                       # line to slice data along
    #     "loc": 0.265,                       # 5mm
    #     "range": [0., 0.02804],             # line to slice data along
    #     "val": "velocity_y",                 # quantity to plot
    #     "vtype": "line"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },


    # FOR PAPER

    # {
    #     "name": "axial_max_swirl",
    #     "dir": "axial",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.0,                      # line to slice data along
    #     "loc": 0.022,                      # line to slice data along
    #     "range": [0.01, 0.34],            # line to slice data along
    #     "val": "velocity_z",                 # quantity to plot
    #     "vtype": "max"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },
    # {
    #     "name": "axial_max_y",
    #     "dir": "axial",                 # indicate plot along torch flow direction or transverse
    #     # "loc": 0.0,                      # line to slice data along
    #     "loc": 0.022,                      # line to slice data along
    #     "range": [0.01, 0.34],            # line to slice data along
    #     "val": "velocity_y",                 # quantity to plot
    #     "vtype": "max"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    # },


    {
        "name": "exit_y",
        "dir": "transverse",                 # indicate plot along torch flow direction or transverse
        # "loc": 0.321,                       # line to slice data along
        "loc": 0.265,                       # line to slice data along
        "range": [0., 0.02804],             # line to slice data along
        "val": "velocity_y",                 # quantity to plot
        "vtype": "line"                 # max, avg, line: plot exact quant on line, or maximum/avg of transverse
    },
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

xdiff = 0.0145

# universal torch coord system
# 124 mm (axi 2d) -> 0 mm (universal)
def tc_transform(x):
    
    return round(1000*(x - .124))

xlabel_map = {
    "transverse": 'r',
    "axial": 'z'
}

ylabel_map_1 = {
    "line": '',
    "max": r'Max'
}

ylabel_map_2 = {
    "velocity_z": r'Swirl ($u_\theta$)',
    "velocity_y": r'Axial Vel. ($u_z$)'
}

home = os.getenv('HOME')

# exp settings
file_exp = home + "/torch_experiments/pivLinesBasic/fullFlowfield"
file_exp_unc = home + "/torch_experiments/pivLinesBasic/Uncertainty/Uncertainty.mat"
filenames = ['AboveInlet.mat', 'BelowStep.mat', 'AboveStep.mat', 'BelowNozzle.mat']
e_toss = 30 # piv data removal
e_yshift = 0.138201

# 3d settings
file_3d = home + "/bedonian1/tps3d_sols/fullTorch_cold_Field_Sigfried/data.pvtu" 

# 2d settings
# file_2d = [home + "/bedonian1/mean_tps2d_newmesh/mean_tps2d_v2_hot_down1cm_zetaf/output-torch-cold-v2-rm13-3dtke-4/output-torch-cold-v2-rm13-3dtke.pvd",
# ]
# name_map_2d = [r'2D v2f']
# color_map_2d = ['b']#, 'm', 'g']
# alpha_map_2d = [1.0]#, 1.0, 1.0]
# t2_xlim = 0.028040 # max torch radius
# t2_ylim = [0.01, 0.345] # max torch length to consider (not really applicable for transverse)
# axi_l = 0.34 # given in the axial range or transverse loc

# file_2d = [home + "/bedonian1/mean_tps2d_newmesh/mean_tps2d_v2_hot_down1cm_zetaf/output-torch-cold-v2-rm13-3dtke-4/output-torch-cold-v2-rm13-3dtke.pvd", home + "/bedonian1/mean_tps2d_newmesh/mean_tps2d_cold_down1cm_turb/output-torch/output-torch.pvd"]
file_2d = [home + "/bedonian1/mean_tps2d_newmesh/mean_tps2d_v2_hot_down1cm_zetaf/output-torch-cold-v2-rm13-3dtke-reset-1/output-torch-cold-v2-rm13-3dtke.pvd", home + "/bedonian1/mean_tps2d_newmesh/mean_tps2d_cold_down1cm_turb/output-torch/output-torch.pvd"]
name_map_2d = [r'2D v2f', r'2D algebraic']
color_map_2d = ['b', 'r']#, 'm', 'g']
alpha_map_2d = [1.0, 1.0] #, 1.0]
t2_xlim = 0.028040 # max torch radius
t2_ylim = [0.01, 0.345]

# process experimental data (including conversion to meters)
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

# uncertainty
data_exp_unc_ind = loadmat(file_exp_unc)['U']
# y shift, convert coord to meters
data_exp_unc_ind['x'] = data_exp_unc_ind['x']/1000.
data_exp_unc_ind['y'] = data_exp_unc_ind['y']/1000.  + e_yshift

data_exp_unc_dict = {}
data_exp_unc_dict['x'] = data_exp_unc_ind['x'][0][0]
data_exp_unc_dict['y'] = data_exp_unc_ind['y'][0][0]
data_exp_unc_dict['velocity_x'] = (data_exp_unc_ind['zero'][0][0]['vx'][0][0] +  data_exp_unc_ind['p60'][0][0]['vx'][0][0] +  data_exp_unc_ind['m60'][0][0]['vx'][0][0])/3.0
data_exp_unc_dict['velocity_y'] = (data_exp_unc_ind['zero'][0][0]['vy'][0][0] +  data_exp_unc_ind['p60'][0][0]['vy'][0][0] +  data_exp_unc_ind['m60'][0][0]['vy'][0][0])/3.0
data_exp_unc_dict['velocity_z'] = (data_exp_unc_ind['zero'][0][0]['vz'][0][0] +  data_exp_unc_ind['p60'][0][0]['vz'][0][0] +  data_exp_unc_ind['m60'][0][0]['vz'][0][0])/3.0




# process tps2d data


# TODO: line slicing scheme for data

for comp in comp_data:

    t3_xp, t3_yp = process_tps3d(comp, file_3d, t2_xlim, t2_ylim)

    e_xp, e_yp = process_exp(comp, data_exp_dict)

    _, e_up = process_exp_uncertainty(comp, e_xp, data_exp_unc_dict)

    t2_xp, t2_yp = process_tps2d(comp, file_2d, t2_xlim, t2_ylim)

    if comp["dir"] == "transverse":
        plt.figure(figsize=(4.8, 4.8))
        plt.xlim(-0.03, 0.03)

        t2_xpa = t2_xp
        t3_xpa = t3_xp
        e_xpa = e_xp
    else:
        plt.figure(figsize=(6.8, 4.8))
        
        t2_xpa = []
        for i in range(len(t2_xp)):
            t2_xpa.append(np.array(t2_xp[i]) + xdiff)
            t2_xpa[i] = t2_xpa[i] - 0.124
        t3_xpa = []
        for i in range(len(t3_xp)):
            t3_xpa.append(np.array(t3_xp[i]) - 0.124)
        e_xpa = []
        for i in range(len(e_xp)):
            e_xpa.append(np.array(e_xp[i]) - 0.124)

    # plot
    for i in range(len(e_xpa)):
        plt.plot(e_xpa[i], e_yp[i], color='k')
        plt.fill_between(e_xpa[i], e_yp[i] + e_up[i], e_yp[i] - e_up[i], color='k', alpha = 0.25)
    plt.plot([], [], color='k', label='Exp.')

    for i in range(len(t2_xpa)):
        plt.plot(t2_xpa[i], t2_yp[i], color=color_map_2d[i], label=name_map_2d[i])

    for i in range(len(t3_xpa)):
        plt.plot(t3_xpa[i], t3_yp[i], color='m', label="3D LES")

    plt.grid()
    if comp["dir"] == "transverse":
        # plt.text(0.5*max(t2_xpa[0]), 0.5*max(t2_yp[0]), f"{tc_transform(comp['loc'])} mm")
        plt.text(0.3*max(t2_xpa[0]), 0.0, f"{tc_transform(comp['loc'])} mm")
        ym = max([abs(max(t3_yp[0])), abs(min(t3_yp[0]))])
        plt.ylim([-1.1*ym, 1.1*ym])
    plt.xlabel(f"{xlabel_map[comp['dir']]} (m)")
    # plt.ylabel(f"{comp['vtype']} {comp['val']} (m/s)")
    plt.ylabel(f"{ylabel_map_1[comp['vtype']]} {ylabel_map_2[comp['val']]} (m/s)")
    plt.legend()
    plt.savefig(f"plots/r2_exp_{comp['name']}_{comp['loc']}.png", bbox_inches='tight', dpi=400)
    plt.clf()

    # breakpoint()

# NOTE: next are to overlay uncertainty, and 3d/2d tps solves