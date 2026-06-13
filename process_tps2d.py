import numpy as np
import pyvista as pv

def process_tps2d(comp, data_t2, axi_x, axi_y):

    n_samp = 1000
    n_rad = 1000

    t2_xp = []
    t2_yp = []

    r_0   = comp['range'][0]
    r_len = comp['range'][1]-comp['range'][0]
    loc = comp['loc']

    val = comp['val']
    vind = 0
    if val == "velocity_x":
        val = 'velocity'
    if val == "velocity_y":
        val = 'velocity'
        vind = 1
    if val == "velocity_z":
        val = 'swirl'

    #NOTE: time averaging?
    for k, cfile in enumerate(data_t2):
        sol2 = pv.get_reader(cfile)
        tf = sol2.time_values[-1]
        sol2.set_active_time_value(tf)
        sol2g = sol2.read()['Block-00']
        t2_xp.append(np.zeros(n_samp))
        t2_yp.append(np.zeros(n_samp))

        for i in range(n_samp):
            # print(f"Point {i}")
            sloc = r_0 + (i/n_samp)*r_len

            if comp['dir'] == "axial":
                pind = 0
                line_coords = np.array([[0., sloc, 0],
                                        [axi_x, sloc, 0]  ])
            elif comp['dir'] == "transverse":
                pind = 1
                line_coords = np.array([[sloc, axi_y[0], 0],
                                        [sloc, axi_y[1], 0]  ])

            sold = sol2g.sample_over_line(line_coords[0], line_coords[1], resolution=n_rad-1)
            sws = np.atleast_2d(sold[val])[vind,:]

            if comp["vtype"] == "max": # should only use this for axial measurements
                t2_yp[-1][i] = np.max(abs(sws))
            elif comp["vtype"] == "avg": # should only use this for axial measurements
                t2_yp[-1][i] = np.avg(sws)
            else: # comp["vtype"] == "line"
                p_dir = sold.points[:,pind]
                loc_ind = np.searchsorted(p_dir, loc)
                wt = (comp['loc'] - p_dir[loc_ind-1]) / (p_dir[loc_ind] - p_dir[loc_ind-1])
                t2_yp[-1][i] = wt*sws[loc_ind-1] + (1-wt)*sws[loc_ind]

            t2_xp[-1][i] = sloc

    return t2_xp, t2_yp