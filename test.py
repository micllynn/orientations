import orientations as ori
import scipy.stats as sp_stats


bar_distractor = ori.Bars('distract', p_bar = 0.3, bar_width = 1, angle_probdist = sp_stats.uniform,
    angle_dict = {'loc' : 0, 'scale' : 360})
bar_stim = ori.Bars('stim', p_bar = 0.7, bar_width = 2, angle_probdist = sp_stats.norm,
    angle_dict = {'loc' : 90, 'scale' : 10})

ori.plot(bar_distractor, bar_stim, n_bars = 30, jitter = 0.5, contrast = 'inverted',
    fname = 'distractor.pdf', dpi = 300, figsize = (8, 8), zoom = 0)
