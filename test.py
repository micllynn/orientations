import orientations as ori
import scipy.stats as sp_stats

bar_stim = ori.Bars('stim', p_bar = 0.99, bar_length = 0.8,
    bar_width = 10, angle_probdist = sp_stats.norm,
    angle_dict = {'loc' : 0, 'scale' : 5})
bar_nonstim = ori.Bars('nonstim', p_bar = 0.01, bar_length = 0.8,
    bar_width = 10, angle_probdist = sp_stats.norm,
    angle_dict = {'loc' : 90, 'scale' : 5})

ori.imgbank(bar_stim, bar_nonstim, n_img = 50, folder_name = 'change', )
