import orientations as ori
import scipy.stats as sp_stats

# Define stim bar
bar_vert = ori.Bars('vert', p_bar=0.4, bar_length=0.8,
                    bar_width=3, angle=0)
bar_horiz = ori.Bars('horiz', p_bar=0.4, bar_length=0.8,
                     bar_width=3, angle=90)

# Make a stochastically generated image out of the bar instances
ori.plot_with_coords(bar_vert, bar_horiz,
                     coords={'vert': [[0, 0], [0, 1], [1, 2], [2, 0], [2, 1]],
                             'horiz': [[0, 2], [1, 0], [1, 1], [2, 2]]},
                     n_bars=3, jitter=0, fname='test_coords.png',
                     zoom=0)
