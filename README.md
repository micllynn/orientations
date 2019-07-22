# Orientations #

Orientations generates arbitrarily complex images comprised of bars with varying orientations. A generator class <code>Bar()</code> is introduced, where each instance can have complex probability distributions specified to draw orientations from. Multiple <code>Bar()</code> class instances can be combined to form orientation-tuned bars with jitter, stimuli in the midst of distractors, etc.

## Introduction ##


### Two bar types with simple, fixed angles
```python
import orientations as ori
import scipy.stats as sp_stats

#Construct bar generator classes.
bar_h = ori.Bars('horiz', p_bar = 0.1, angle = 0)
bar_v = ori.Bars('vert', p_bar = 0.9, angle = 90)

#Now let's plot the results with 20 bars generated per image side.
ori.plot(bar_h, bar_v, n_bars = 20)
```

Note that an image along with a .txt file storing all chosen stimulus parameters has been saved.

### Two bar types each with normally distributed angles

```python
#Let's choose probability functinos from sp_stats as angles:
bar_h = ori.Bars('horiz', p_bar = 0.1, angle_probdist = sp_stats.norm,
  angle_dict = {'loc' : 0, 'scale' : 10})
bar_v = ori.Bars('vert', p_bar = 0.9, angle_probdist = sp_stats.norm,
  angle_dict = {'loc' : 90, 'scale' : 10})

#Now let's plot the results with lower jitter and more bars per image side.
ori.plot(bar_h, bar_v, n_bars = 40, jitter = 0.8)
```

Note that any probability distribution from <code>scipy.stats</code> can be specified, along with a dictionary of kwargs specifying e.g. mean and s.d. This allows for complex stimulus parameters to be chosen.

### Making one 'distractor' bar type and another stimulus bar type
```python
#Make one kind of disctractor bar-type, and another stimulus. Make the distractor bars thinner.
bar_distractor = ori.Bars('distract', p_bar = 0.4, bar_width = 1,
  angle_probdist = sp_stats.uniform, angle_dict = {'loc' : 0, 'scale' : 360})
bar_stim = ori.Bars('stim', p_bar = 0.6, bar_width = 2,
  angle_probdist = sp_stats.alpha, angle_dict = {'a' : 2, 'loc' : 90, 'scale' : 5})

#Plotting can also take more parameters...
ori.plot(bar_distractor, bar_stim, n_bars = 40, jitter = 0.5, contrast = 'inverted',
  fname = 'distractor.pdf', dpi = 300, figsize = (8, 8), zoom = -0.1)
```

### Generating an arbitrary number of bar types which tile the angle space
```python
bars = []
angles = np.linspace(0, 180, 5)

for angle in angles:
  bars.append(ori.Bars(str(angle), p_bar = 1/len(angles),
  angle_probdist = sp_stats.norm, angle_dict = {'loc' : angle, 'scale' : 5}))

ori.plot(*bars, n_bars = 30, jitter = 0.5)

```


## More information

The image, as well as a text file corresponding to all image and bar parameters, is stored in the /figs file.

See the class <code>Bars()</code> for more information about stimulus parameters.
(<code>help(ori.Bars.\__init__.)</code>).

Additionally, <code>help(ori.plot)</code> contains a substantial amount of information on the plotting parameters.
