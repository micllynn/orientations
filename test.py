import orientations as ori
import scipy.stats as sp_stats


bar_distractor = ori.Bars('distract', p_bar = 0.4, bar_width = 2, angle_probdist = sp_stats.uniform,
    angle_dict = {'loc' : 0, 'scale' : 360})
bar_stim = ori.Bars('stim', p_bar = 0.6, bar_width = 2, angle_probdist = sp_stats.alpha,
    angle_dict = {'a' : 1, 'loc' : 90, 'scale' : 1})

ori.plot(bar_distractor, bar_stim, n_bars = 40, jitter = 1, contrast = 'inverted',
    fname = 'distractor.pdf', dpi = 300, figsize = (8, 8), zoom = -0.1)
