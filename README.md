# Orientations #

Orientations generates images comprised of a number of vertical and horizontal bars, for use in mouse behavior testing. Tools providing granularity over the stimulus parameters are built-in.

## Introduction ##

### Making two types of bars with normally distributed angles

```python
>>> import orientations as ori
>>> import scipy.stats as sp_stats

#Let's construct two bar classes, each with normally distributed angles. Note
#that any probability distribution from sp_stats can be specified, along with a
#dictionary of kwargs specifying e.g. mean and s.d.
>>> bar_h = Bars('horiz', p_bar = 0.1, angle_probdist = sp_stats.norm,
  angle_dict = {'loc' : 0, 'scale' : 10})
>>> bar_v = Bars('vert', p_bar = 0.9, angle_probdist = sp_stats.norm,
  angle_dict = {'loc' : 90, 'scale' : 10})
#Now let's plot the results.
>>> plot(bar_h, bar_v, n_bars = 20)

```

### Making one type of 'distractor' bar and another stimulus bar

```python
>>> bar_distractor = Bars('distract', p_bar = 0.8, angle_probdist = sp_stats.uniform,
    angle_dict = {'loc' : 0, 'scale' : 1})
>>> bar_stim = Bars('stim', p_bar = 0.2, angle_probdist = sp_stats.alpha,
    angle_dict = {'a' : 1, 'loc' : 0, 'scale' : 1})
#Plotting can also take more parameters...
>>> plot(bar_distractor, bar_stim, n_bars = 40, jitter = 1.5, contrast = 'normal',
    fname = 'distractor.pdf', dpi = 300, figsize = (10, 10), zoom = 0.9)
```

## More information

The image, as well as a text file corresponding to all image and bar parameters,
is stored in the /figs file.

See the class <code> Bars() </code> for more information about stimulus parameters.
(<code> print(ori.Bars.__init__.__doc__) </code>).

Additionally, <code> print(ori.plot.__doc__) </code> contains a substantial
amount of information on the plotting parameters.
