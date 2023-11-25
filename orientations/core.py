import numpy as np
import matplotlib.pyplot as plt
import os, sys


def assign(items, group_names, num, return_inds=False):
    """Assigns items to named groups, each with defined capacities.

    Parameters
    ------
    items : 1-D array-like
        An input array of items. Must be np.ndarray or list.
    group_names : list
        A list of string names for each group.
    num : list
        The number of members of each group. Can also be probabilities of group
        assignment.
    return_inds : bool, optional
        If true, returns the indices of values in val instead of the values
        themselves.

    Returns
    ------
    inds : dict
        Dictionary containg mapping between each group and the indices of its
        assigned values.
    groups : dict
        Dictionary containing the values assigned to each group.

    Example
    ------

    Assign people to two groups with 4 and 3 members, respectively:
    >>> groups = assign(['Mike', 'Elo', 'Seb', 'JC', 'JF', 'Philippe', 'Lea'],
        ['Red', 'Blue'], [4, 3])

    Assign people to two groups with 0.4 and 0.6 fractional occupancy,
    respectively, and returns indices in the items vector for each group:
    >>> inds = assign(['Mike', 'Elo', 'Seb', 'JC', 'JF', 'Philippe', 'Lea'],
        ['Red', 'Blue'], [0.4, 0.6], return_inds = True)


    """

    # Normalize num (group capacity)
    p_group = num / np.sum(
        np.array(num))  # Normalize probability to ensure they sum to 1.
    n_items = len(items)
    group_size = np.round(p_group * n_items).astype(np.int)

    # Generate shuffled array from which to assign items to groups.
    shuffled = np.random.choice(
        np.arange(n_items), size=n_items, replace=False).astype(
            np.int)  # Shuffle inds of vals to pick groups from

    # Choose items for each group.
    inds = {}
    groups = {}

    _n_picked = 0  # Stores how many of shuffled have been picked

    for ind_gr, group in enumerate(group_names):
        # Compute lower and upper bounds in shuffled ind set
        _lower_pick = _n_picked
        _upper_pick = _n_picked + group_size[ind_gr]

        # assign inds and vals for this group from shuffled
        _inds_assigned = shuffled[_lower_pick:_upper_pick]

        if type(items) is np.ndarray:
            _items_assigned = items[_inds_assigned]
        elif type(items) is list:
            _items_assigned = [items[i] for i in _inds_assigned]
        else:
            raise TypeError('items must be either a list or np.ndarray.')

        # Update the dicts (inds, groups) with the new values for this group.
        _update_inds = {group: _inds_assigned}
        _update_items = {group: _items_assigned}

        inds.update(_update_inds)
        groups.update(_update_items)

        _n_picked = _upper_pick  # Set number of picked values to new val.

    if return_inds is True:
        return inds
    elif return_inds is False:
        return groups


class Bars(object):
    """
    Generator class for a set of bars with a given set of characteristics.

    Instances are passed to plot() and are used to probabilistically generate
    images.
    """
    def __dir__(self):
        return [
            'name', 'bar_length', 'bar_width', 'p_bar',
            'angle', 'angle_probdist', 'angle_dict'
        ]

    def __init__(self,
                 name,
                 bar_length=0.9,
                 bar_width=2,
                 p_bar=0,
                 angle=None,
                 angle_probdist=None,
                 angle_dict=None):
        """
        Parameters
        ------
        name : str
            A name for the Bar object.
        angle : float or None
            Angle in degress from horizontal. If angle is None, angle_probdist
            is used to draw the angle.
        bar_length : float
        bar_width : float
        p_bar : float
            Gives the probability of this bar instance appearing at each
            location in an image (with plot())
        angle_probdist : None or object from [scipy.stats._continuous_distns],
        optional
            If angle is None and angle_probdist is not None: draw I.I.D
            angles from angle_probdist for each generated bar from Bar() in
            the graph.
                e.g. angle_probdist = sp.stats.norm;
                or angle_probdist = sp.stats.uniform
        angle_dict : None or dict, optional
            A dictionary containing kwargs to pass to angle_probdist. Must be
            comprised of kwargs which are associated with the particular
            sp.stats distribution used.
                e.g. angle_dict = {'loc' : 20, 'scale' : 10}
        """
        self.name = name
        self.angle = angle
        self.bar_length = bar_length
        self.bar_width = bar_width
        self.p_bar = p_bar
        self.angle_probdist = angle_probdist
        self.angle_dict = angle_dict

        return


def plot(*args,
         n_bars=20,
         jitter=0.5,
         contrast='inverted',
         fname='orientations.pdf',
         dpi=300,
         figsize=None,
         zoom=0,
         **kwargs):
    """Generates an image consisting of multiple angled bars, and an
    associated textfile of parameters.

    Parameters
    ------
    *args : list
        Any number of Bar() class instances, used to generate bars on the image.
    n_bars: int (optional)
        The number of bars per side of the image.
    jitter : float (optional)
        The jitter in bar center coordinates, expressed as a fraction of the
        total bar length.
    contrast : str, 'inverted' or 'normal' (optional)
        If 'inverted', the bars are white and the background is black.
        Otherwise, the bars are black and the background is white.
    fname : str (optional)
        The filename of the saved image.
    dpi : int (optional)
        the dots per inch of the figure.
    figsize : tuple (optional)
        Figsize in inches, to pass to plt.savefig()
    zoom : float (optional)
        The zoom factor. 0 is no zoom, while positive values indicate zooming in
        and negative values indicate zooming out.

    """
    __params = locals()

    # Pre-analysis housework: store names, normalize p_bar, calculate expected
    # n for each class
    # ----------------
    p_bar_tot = sum([bar.p_bar for bar in args])
    names = []
    n_bar = []
    max_bar_length = 0  # Used for setting axis lims

    for ind, bar in enumerate(args):
        names.append(bar.name)
        bar.p_bar /= p_bar_tot
        bar._n_bar = int(bar.p_bar * n_bars**2)
        n_bar.append(bar._n_bar)
        if bar.bar_length >  max_bar_length:
            max_bar_length = bar.bar_length

    # Determine center coordinates for each bar including jitter
    center_x = np.linspace(0, 1, n_bars)
    center_y = np.linspace(0, 1, n_bars)

    # Assign bars to each position
    n_bars_sq = n_bars**2
    groups = assign(np.arange(n_bars_sq), names, n_bar, return_inds=True)

    assigned_x = {}
    assigned_y = {}

    # Initialize plot
    # ------------------
    if figsize is None:
        figsize = (8, 8)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)

    if contrast == 'normal':
        bar_color = 'k'
        ax.set_facecolor([1, 1, 1])
    elif contrast == 'inverted':
        bar_color = [1, 1, 1]
        ax.set_facecolor([0, 0, 0])

    # Iterate through bars, plotting inds for each one
    # -----------------------
    for ind_name, name in enumerate(names):
        _bar = args[ind_name]
        _assigned_bars = groups[name]
        _x, _y = np.unravel_index(_assigned_bars, (n_bars, n_bars))

        assigned_x[name] = _x
        assigned_y[name] = _y

        # Now calculate the xcoords and ycoords of the bar tips.
        x_coords = np.empty((2, len(assigned_x[name])))
        y_coords = np.empty_like(x_coords)

        _ind_bar = 0

        for ind_assigned in range(len(assigned_x[name])):
            # Center coordinates for x for this particular bar
            _x = center_x[assigned_x[name][ind_assigned]]
            _y = center_y[assigned_y[name][ind_assigned]]

            # Jitter the center point depending on class params
            _center_x = _x + ((np.random.rand() - 0.5)
                              * jitter * _bar.bar_length/n_bars * 0.5)
            _center_y = _y + ((np.random.rand() - 0.5)
                              * jitter * _bar.bar_length/n_bars * 0.5)

            # Calculate a deltax / deltay based on angle
            if _bar.angle is None:
                _angle = _bar.angle_probdist.rvs(size=1, **_bar.angle_dict)[0]
            elif _bar.angle is not None:
                _angle = _bar.angle

            _dx = (np.cos(np.radians(_angle)) * _bar.bar_length / n_bars * 0.5)
            _dy = (np.sin(np.radians(_angle)) * _bar.bar_length / n_bars * 0.5)

            x_coords[:, _ind_bar] = np.array(
                [_center_x - _dx, _center_x + _dx])
            y_coords[:, _ind_bar] = np.array(
                [_center_y - _dy, _center_y + _dy])

            _ind_bar += 1

        ax.plot(x_coords, y_coords, color=bar_color, linewidth=_bar.bar_width)

    # Adjust figure params
    # ----------------
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticks([])
    ax.set_yticks([])

    # Implement zooming
    xlim_min, xlim_max = ax.get_xlim()
    ylim_min, ylim_max = ax.get_ylim()
    ax.set_xlim([xlim_min+zoom, xlim_max-zoom])
    ax.set_ylim([ylim_min+zoom, ylim_max-zoom])
    plt.tight_layout()

    if 'fname_full' in kwargs:
        fname_full = kwargs.pop('fname_full')
        plt.savefig(fname_full, dpi=dpi)
    else:
        fname_full = os.path.join(os.getcwd(), 'figs') + fname
        plt.savefig(fname_full, dpi=dpi)

    # Save textfile
    fname_txt = os.path.splitext(fname_full)[0] + '.txt'
    with open(fname_txt, 'w') as f:
        f.write('-------\nImg params\n-------')
        for item in __params.items():
            f.write('\n\t' + str(item))
        f.write('\n\n\n--------\nBar Class Instances\n--------')
        for bar in args:
            f.write('\n**Bar: ' + bar.name + '**')
            for item in bar.__dict__.items():
                f.write('\n\t' + str(item))
            f.write('\n\n')

    return


def plot_with_coords(*args,
                     n_bars=20,
                     coords=None,
                     jitter=0.5,
                     contrast='inverted',
                     fname='orientations.pdf',
                     dpi=300,
                     figsize=None,
                     zoom=0,
                     **kwargs):
    """Generates an image consisting of multiple angled bars, and an
    associated textfile of parameters.

    Here, instead of probabilistically generating locations of each bar type,
    we can give precise coordinates for each instance of the Bar class
    (ie specify that (1, 1) will be a vertical bar, (1, 2) is horizontal,
    and so forth.)

    Note that for this function, the p_bar argument for each Bar() class
    instance passed to *args is ignored, and instead the precise numbers
    of each Bar() instance is defined by coords (described below).

    Parameters
    ------
    *args : list
        Any number of Bar() class instances, used to generate bars on the image.
    n_bars: int (optional)
        The number of bars per side of the image.
    coords: dict
        A dictionary consisting of named Bar() classes as keys, and lists of
        coordinates (x,y) as values associated with those keys.
            ex: coords = {'horiz': [[0, 1], [1, 0], [1, 2]],
                        'vert': [[0, 0], [1, 1], [2, 0], [2, 1]]}
    jitter : float (optional)
        The jitter in bar center coordinates, expressed as a fraction of the
        total bar length.
    contrast : str, 'inverted' or 'normal' (optional)
        If 'inverted', the bars are white and the background is black.
        Otherwise, the bars are black and the background is white.
    fname : str (optional)
        The filename of the saved image.
    dpi : int (optional)
        the dots per inch of the figure.
    figsize : tuple (optional)
        Figsize in inches, to pass to plt.savefig()
    zoom : float (optional)
        The zoom factor. 0 is no zoom, while positive values indicate zooming in
        and negative values indicate zooming out.

    """
    __params = locals()

    # Pre-analysis housework: store names, normalize p_bar, calculate expected
    # n for each class
    # ----------------
    p_bar_tot = sum([bar.p_bar for bar in args])
    names = []
    n_bar = []
    max_bar_length = 0  # Used for setting axis lims

    for ind, bar in enumerate(args):
        names.append(bar.name)
        bar.p_bar /= p_bar_tot
        bar._n_bar = int(bar.p_bar * n_bars**2)
        n_bar.append(bar._n_bar)
        if bar.bar_length >  max_bar_length:
            max_bar_length = bar.bar_length

    # Determine center coordinates for each bar including jitter
    center_x = np.linspace(0, 1, n_bars)
    center_y = np.linspace(0, 1, n_bars)

    # Assign bars to each position
    n_bars_sq = n_bars**2
    groups = assign(np.arange(n_bars_sq), names, n_bar, return_inds=True)

    assigned_x = {}
    assigned_y = {}

    # Initialize plot
    # ------------------
    if figsize is None:
        figsize = (8, 8)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)

    if contrast == 'normal':
        bar_color = 'k'
        ax.set_facecolor([1, 1, 1])
    elif contrast == 'inverted':
        bar_color = [1, 1, 1]
        ax.set_facecolor([0, 0, 0])

    # Iterate through bars, plotting inds for each one
    # -----------------------
    for ind_name, name in enumerate(names):
        _bar = args[ind_name]
        # _assigned_bars = groups[name]
        # _x, _y = np.unravel_index(_assigned_bars, (n_bars, n_bars))

        # assigned_x[name] = _x
        # assigned_y[name] = _y

        # # Now calculate the xcoords and ycoords of the bar tips.
        _x_coords = np.empty((2, len(coords[name])))
        _y_coords = np.empty_like(_x_coords)

        _ind_bar = 0

        for ind_assigned in coords[name]:
            # Center coordinates for x/y for this particular bar
            _ind_assigned_norm = np.array(ind_assigned) / n_bars
            _x = _ind_assigned_norm[0]
            _y = _ind_assigned_norm[1]

            # Jitter the center point depending on class params
            _center_x = _x + ((np.random.rand() - 0.5)
                              * jitter * _bar.bar_length/n_bars * 0.5)
            _center_y = _y + ((np.random.rand() - 0.5)
                              * jitter * _bar.bar_length/n_bars * 0.5)

            # Calculate a deltax / deltay based on angle
            if _bar.angle is None:
                _angle = _bar.angle_probdist.rvs(size=1, **_bar.angle_dict)[0]
            elif _bar.angle is not None:
                _angle = _bar.angle

            _dx = (np.cos(np.radians(_angle)) * _bar.bar_length / n_bars * 0.5)
            _dy = (np.sin(np.radians(_angle)) * _bar.bar_length / n_bars * 0.5)

            _x_coords[:, _ind_bar] = np.array(
                [_center_x - _dx, _center_x + _dx])
            _y_coords[:, _ind_bar] = np.array(
                [_center_y - _dy, _center_y + _dy])

            _ind_bar += 1

        ax.plot(_x_coords, _y_coords, color=bar_color,
                linewidth=_bar.bar_width)

    # Adjust figure params
    # ----------------
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticks([])
    ax.set_yticks([])

    # Implement zooming
    xlim_min, xlim_max = ax.get_xlim()
    ylim_min, ylim_max = ax.get_ylim()
    ax.set_xlim([xlim_min+zoom, xlim_max-zoom])
    ax.set_ylim([ylim_min+zoom, ylim_max-zoom])
    plt.tight_layout()

    if 'fname_full' in kwargs:
        fname_full = kwargs.pop('fname_full')
        plt.savefig(fname_full, dpi=dpi)
    else:
        fname_full = os.path.join(os.getcwd(), 'figs', fname)
        plt.savefig(fname_full, dpi=dpi)

    # Save textfile
    fname_txt = os.path.splitext(fname_full)[0] + '.txt'
    with open(fname_txt, 'w') as f:
        f.write('-------\nImg params\n-------')
        for item in __params.items():
            f.write('\n\t' + str(item))
        f.write('\n\n\n--------\nBar Class Instances\n--------')
        for bar in args:
            f.write('\n**Bar: ' + bar.name + '**')
            for item in bar.__dict__.items():
                f.write('\n\t' + str(item))
            f.write('\n\n')

    return


def imagebank(*args, n_img=50, folder_name='imagebank', **kwargs):
    """Constructs an imagebank of slightly different images, all generated
    using the same parameters, and stores them in folder_name.
    Can take any arguments from plot().

    Parameters:
    ----------------
    n_img : int (optional)
        Number of distinct images in the databank to generate.
    folder_name : string (optional):
        Name of new folder (within /figs/) to store the databank.
    """
    # Check that the folder exists
    path = os.path.join(os.getcwd(), 'figs', folder_name)
    if not os.path.exists(path):
        os.makedirs(path)

    print(f'directory to store images in: {path}')

    # Plot and save
    for reps in range(n_img):
        print(f'\rgenerating image {reps+1} of {n_img}...', end='')
        fname_full = os.path.join(path, folder_name + '_' + str(reps) + '.jpg')
        plot(*args, fname_full=fname_full, **kwargs)
        plt.close()

    return
