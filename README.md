# Orientations #

Orientations generates images comprised of a number of vertical and horizontal bars, for use in mouse behavior testing. Tools providing granularity over the stimulus parameters are built-in. 

## Guide ##

>> orientations(n_bars = 20, p_vertical = 0.1) #generates 20 bars 
	#per side with 10% having a vertical orientation
>> orientations(n_bars = 20, p_vertical = 0, jitter = 0.1) #generates 20 bars
	#per side, none having a vertical orientation, with minimal jitter.

By default, the resulting image is stored in the same folder.

See the function <code> orientations() </code> for more information about stimulus parameters.

