import orientations as ori
import scipy.stats as sp_stats


bar_distractor = ori.Bars('distract', p_bar = 0.3, bar_width = 2, angle_probdist = sp_stats.uniform,
    angle_dict = {'loc' : 0, 'scale' : 360})
bar_stim = ori.Bars('stim', p_bar = 0.7, bar_width = 2, angle_probdist = sp_stats.norm,
    angle_dict = {'loc' : 0, 'scale' : 5})


ori.plot(bar_distractor, bar_stim, n_bars = 20, jitter = 1, contrast = 'inverted',
    fname = 'horiz_change_30pc.pdf', dpi = 300, figsize = (8, 8), zoom = -0.1)
