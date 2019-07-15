import numpy as np
import matplotlib.pyplot as plt


def orientations(n_bars = 20, p_vertical = 0.0, bar_length = 0.8, bar_width = 1,
    jitter = 0.5, contrast = 'normal',  fname = 'orientations.pdf', dpi = 300):
    '''
    Function generates an image comprised of a set of small bars with mixed
    vertical and horizontal orientation, for use in mouse behavior testing.

    Parameters
    -------
    n_bars : int (default 20)
        Number of bars per side of the image
    p_vertical : float (default 0.0)
        Probability of vertical lines
    bar_length : float (default 0.8)
        Length of each bar, expressed as a fraction of the total distance
        between ajacent bars
    bar_width : float (default 1)
        Linewidth of each bar
    jitter : float (default 0.5)
        The amount of jitter in (x,y) coordinates for each bar, expressed as a
        fraction of the distance between ajacent bars
    contrast : str; 'normal' or 'inverted'
        White bars on a black background ('inverted'), or black bars on a White
        background ('normal').

    fname : str
        Filename and extension type to specify
    dpi : int
        Dots per inch of figure to save


    '''
    x = np.linspace(0, 1, n_bars)
    y = np.linspace(0, 1, n_bars)

    abs_bar_length = bar_length/(n_bars)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    if contrast is 'normal':
        bar_color = 'k'
        ax.set_facecolor([1, 1, 1])
    elif contrast is 'inverted':
        bar_color = [1, 1, 1]
        ax.set_facecolor([0, 0, 0])

    x_bar = np.empty((2, len(x) * len(y)))
    y_bar = np.empty_like(x_bar)

    ind_bar = 0

    for ind_x, _x in enumerate(x):
        for ind_y, _y in enumerate(y):
            _vert = np.random.rand() < p_vertical
            _jitter = (np.random.rand() - 0.5) * jitter * abs_bar_length

            if _vert is False:
                x_bar[:, ind_bar] = np.array([x[ind_x] - abs_bar_length/2,
                    x[ind_x] + abs_bar_length/2]) + _jitter
                y_bar[:, ind_bar] = np.array([y[ind_y] - abs_bar_length/8,
                    y[ind_y] + abs_bar_length/8]) + _jitter

            elif _vert is True:
                x_bar[:, ind_bar] = np.array([x[ind_x] - abs_bar_length/8,
                    x[ind_x] + abs_bar_length/8]) + _jitter
                y_bar[:, ind_bar] = np.array([y[ind_y] - abs_bar_length/2,
                    y[ind_y] + abs_bar_length/2]) + _jitter

            ind_bar += 1

    ax.plot(x_bar, y_bar, color = bar_color, linewidth = bar_width)

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(fname, dpi = dpi)

    return



orientations(n_bars = 20, p_vertical = 0.9, jitter = 1,
    contrast = 'inverted', fname = 'orientations.jpg', dpi = 300)
