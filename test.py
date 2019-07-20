import orientations as ori
import scipy.stats as sp_stats

bar_h = ori.Bars('horiz', bar_length = 0.9, bar_width = 2, p_bar = 0.1,
    angle_probdist = sp_stats.norm, angle_dict = {'loc' : 0, 'scale' : 10})
bar_v = ori.Bars('vert', bar_length = 0.9, bar_width = 2, p_bar = 0.9,
    angle_probdist = sp_stats.norm, angle_dict = {'loc' : 90, 'scale' : 10})

ori.plot(bar_h, bar_v, n_bars = 20, jitter = 1, zoom = -0.05)
