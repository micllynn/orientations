# Orientations #

Orientations generates images comprised of a number of vertical and horizontal bars, for use in mouse behavior testing. Tools providing granularity over the stimulus parameters are built-in.

## Introduction ##

### Making two types of bars with normally distributed angles

```python
>>> import orientations as ori
>>> import scipy.stats as sp_stats

#Let's construct two bar classes, each with normally distributed angles.
bar_h = ori.Bars('horiz', p_bar = 0.1, angle_probdist = sp_stats.norm,
  angle_dict = {'loc' : 0, 'scale' : 10})
bar_v = ori.Bars('vert', p_bar = 0.9, angle_probdist = sp_stats.norm,
  angle_dict = {'loc' : 90, 'scale' : 10})

#Now let's plot the results.
ori.plot(bar_h, bar_v, n_bars = 20)

```
Note that any probability distribution from sp_stats can be specified, along with a dictionary of kwargs specifying e.g. mean and s.d. This allows for complex stimulus parameters to be specified.

### Making one type of 'distractor' bar and another stimulus bar
```python
#Make one kind of disctractor bar-type, and another stimulus.
bar_distractor = ori.Bars('distract', p_bar = 0.4, bar_width = 2, angle_probdist = sp_stats.uniform,
  angle_dict = {'loc' : 0, 'scale' : 360})
bar_stim = ori.Bars('stim', p_bar = 0.6, bar_width = 2, angle_probdist = sp_stats.alpha,
  angle_dict = {'a' : 2, 'loc' : 90, 'scale' : 5})

#Plotting can also take more parameters...
ori.plot(bar_distractor, bar_stim, n_bars = 40, jitter = 1, contrast = 'inverted',
  fname = 'distractor.pdf', dpi = 300, figsize = (8, 8), zoom = -0.1)
```

## More information

The image, as well as a text file corresponding to all image and bar parameters, is stored in the /figs file.

See the class <code>Bars()</code> for more information about stimulus parameters.
(<code>help(ori.Bars.\__init__.)</code>).

Additionally, <code>help(ori.plot)</code> contains a substantial amount of information on the plotting parameters.
