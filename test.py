import orientations as ori
import scipy.stats as sp_stats

# Define stim bar
bar_stim = ori.Bars('stim', p_bar = 0.6, bar_length = 0.8,
                    bar_width = 10, angle_probdist = sp_stats.norm,
                    angle_dict = {'loc' : 0, 'scale' : 5})

# Define nonstim bar
bar_nonstim = ori.Bars('nonstim', p_bar = 0.2, bar_length = 0.8,
                       bar_width = 10, angle_probdist = sp_stats.norm,
                       angle_dict = {'loc' : 90, 'scale' : 5})

# Define an empty space
bar_none = ori.Bars('none', p_bar=0.2, bar_length=0.8,
                    bar_width=0, angle=0)

# Make a randomly generated image with all bar types
ori.plot(bar_stim, bar_nonstim, bar_none, n_bars=6, fname = 'test.pdf')

# Make an entire dataset of randomly generated images
locals = ori.imagebank(bar_stim, bar_nonstim, bar_none, n_img = 50, folder_name = 'change',
                       n_bars = 5, jitter = 0.5)
