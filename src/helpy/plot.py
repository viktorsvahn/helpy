#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def color_label(
		ax,
		labels,
		width,
		height,
		position, 
		fontcolor='black',
		fontsize=8, 
		rel_size=True, 
		cmap='tab20', 
		alpha=1, 
		halign='left',
		valign='bottom',
		orientation='horizontal',
		zorder=None,
		clip_on=True
	):
	"""Adds a series of annotated color patches to an axis object.

	Keyword arguments:
	ax -- axis object
	labels -- list of string labels
	width -- width of patch
	height -- of patch
	position -- starting position of patches
	fontcolor -- color of label font( default black)
	fontsize -- size of annotation (default 8)
	rel_size -- sets size relative to plot limits (default True)
	cmap -- color set of patches (default 'tab20', pyplot default)
	alpha -- opacity of patches
	halign -- horizontal alignment of patch series (default left)
	valign -- vertical alignment of patch series (default bottom)
	orientation -- sets the orientation of the patch series (default horizontal)
	zorder -- assigns the layer that the patches are a part of (one above 
	          current max of figure)
	clip_on -- allow/disallow crossing of axis borders (default False)

	The color 'bright', 'light' and 'medium_contrast' were created by Paul Tol.	
	For more information, please refer to:
	https://personal.sron.nl/~pault/
	"""
	posx, posy = position

	# Sets zorder to one above max in figure
	if zorder == None:
		zorder = max([_.zorder for _ in ax.get_children()])+1
	
	# If labels is a single string, create only one patch
	if type(labels) is not str:
		assert isinstance(labels, list),\
		'Specify a string or a list of strings as labels.'
	else: labels = [labels]

	# Size relative to plot limits
	if rel_size:
		width *= (ax.get_xlim()[1]-ax.get_xlim()[0])
		height *= (ax.get_ylim()[1]-ax.get_ylim()[0])
	
	# Color selection (Paul Tol)
	bright = [
		'#4477AA',
		'#EE6677',
		'#228833',
		'#CCBB44',
		'#66CCEE',
		'#AA3377',
		'#BBBBBB'
	]
	medium_contrast = [
		'#6699CC',
		'#004488',
		'#EECC66',
		'#994455',
		'#997700',
		'#EE99AA',
		'#000000'
	]
	light = [
		'#77AADD',
		'#EE8866',
		'#EEDD88',
		'#FFAABB',
		'#99DDFF',
		'#44BB99',
		'#BBCC33',
		'#AAAA00',
		'#DDDDDD'
	]
	cmaps ={'bright':bright, 'light':light, 'medium_contrast':medium_contrast}

	## Select colormap from custom list
	if isinstance(cmap, list):
		color = cmap

	## Select Paul Tol colormaps defined above
	elif cmap in cmaps.keys():
		color = cmaps[cmap]
	
	## Use matplotlib default colors
	else:
		if cmap is not None:
			from cycler import cycler
			plt.rcParams['axes.prop_cycle'] = cycler('color', plt.get_cmap(cmap).colors)
		prop_cycle = plt.rcParams['axes.prop_cycle']
		color = prop_cycle.by_key()['color']

	# Alignment offsets
	if halign == 'left':
		posx += 0
	elif halign == 'right': 
		posx -= len(labels)*width
	elif halign == 'center':
		posx -= len(labels)*width/2

	if valign == 'bottom':
		posy += 0
	elif valign == 'top':
		posy -= height
	elif valign == 'center':
		posy -= height/2

	# Orientation control
	if orientation == 'horizontal':
		k=1
		a=0
		oriented_width, oriented_height = width, height
	elif orientation == 'vertical':
		k=-1
		a=90
		oriented_width, oriented_height = height, width

	# Add patches with labels
	for i, label in enumerate(labels):
		rect = ax.add_patch(
			Rectangle(
				(posx+width*i, posy)[::k],
				oriented_width,
				oriented_height,
				color=color[i],
				alpha=alpha,
				zorder=zorder,
				clip_on=clip_on
			)
		)
		ax.annotate(
			f'{label}',
			(posx+oriented_width*i, posy)[::k],
			(posx+width*i+width*1/2, posy+height/2)[::k],
			color=fontcolor,
			fontsize=fontsize,
			ha='center',
			va='center',
			zorder=zorder,
			annotation_clip=clip_on,
			rotation=a
		)
