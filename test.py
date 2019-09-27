import orientations as ori
import scipy.stats as sp_stats

# Define stim bar
bar_stim = ori.Bars('stim', p_bar=0.4, bar_length=0.8,
                    bar_width=3, angle_probdist=sp_stats.norm,
                    angle_dict={'loc':0, 'scale':10})
bar_distractor = ori.Bars('dist', p_bar=0.4, bar_length=0.8, bar_width=3,
                          angle_probdist=sp_stats.uniform,
                          angle_dict={'loc':0, 'scale':360})
bar_omit = ori.Bars('omit', p_bar=0.2, bar_length=0.8, bar_width=0, angle=0)

# Make a stochastically generated image out of the bar instances
ori.plot(bar_stim, bar_distractor, bar_omit, n_bars=15, jitter=0.8, fname = 'test.pdf',
         zoom=0)
