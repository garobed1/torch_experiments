import numpy as np
import pyvista as pv

def process_tps3d(comp, data_t3, axi_x, axi_y, hot = False):

    n_samp = 1000
    n_rad = 1000
    n_avg = 6

    t3_xp = []
    t3_yp = []

    r_0   = comp['range'][0]
    r_len = comp['range'][1]-comp['range'][0]
    loc = comp['loc']

    val = comp['val']
    if val.startswith("velocity"):
        vind = 0
        if val == "velocity_y":
            vind = 1
        if val == "velocity_z":
            vind = 2

        if hot:
            val = 'velocity'
        else:
            val = 'vel'

    # for k, cfile in enumerate(data_t3):
    sol3 = pv.get_reader(data_t3)
    # tf = sol.time_values[-1]
    # sol.set_active_time_value(tf)
    sol3g = sol3.read()
    t3_xp.append(np.zeros(n_samp))
    t3_yp.append(np.zeros(n_samp))

    for i in range(n_samp):
        # print(f"Point {i}")
        sloc = r_0 + (i/n_samp)*r_len

        # angle average
        sws = np.zeros(n_rad)
        for s in range(n_avg):

            angle = (s/n_avg)*2*np.pi


            if comp['dir'] == "axial":
                pind = 0
                line_coords = np.array([[0., sloc, 0],
                                        [axi_x*np.cos(angle), sloc, axi_x*np.sin(angle)]  ])
            elif comp['dir'] == "transverse":
                pind = 1
                line_coords = np.array([[sloc*np.cos(angle), axi_y[0], sloc*np.sin(angle)],
                                        [sloc*np.cos(angle), axi_y[1], sloc*np.sin(angle)]  ])

            sold = sol3g.sample_over_line(line_coords[0], line_coords[1], resolution=n_rad-1)

            if vind == 0:
                sws += sold[val][:,0]*np.cos(angle) + sold[val][:,2]*np.sin(angle)
            elif vind == 1:
                sws += np.atleast_2d(sold[val])[vind,:]
            else:
                sws += -sold[val][:,0]*np.sin(angle) + sold[val][:,2]*np.cos(angle)
        sws /= n_avg

        if comp["vtype"] == "max": # should only use this for axial measurements
            t3_yp[-1][i] = np.max(abs(sws))
        elif comp["vtype"] == "avg": # should only use this for axial measurements
            t3_yp[-1][i] = np.avg(sws)
        else: # comp["vtype"] == "line"
            p_dir = sold.points[:,pind]
            loc_ind = np.searchsorted(p_dir, loc)
            # breakpoint()
            wt = (comp['loc'] - p_dir[loc_ind-1]) / (p_dir[loc_ind] - p_dir[loc_ind-1])
            t3_yp[-1][i] = wt*sws[loc_ind-1] + (1-wt)*sws[loc_ind]

        t3_xp[-1][i] = sloc

    return t3_xp, t3_yp