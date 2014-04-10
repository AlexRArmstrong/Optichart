#! /usr/bin/env python
#########################################################################
#                                                                       #
#    This program is free software; you can redistribute it and/or      #
#    modify it under the terms of the GNU General Public License        #
#    version 2, as published by the Free Software Foundation.           #
#                                                                       #
#    This program is distributed in the hope that it will be useful,    #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      #
#    GNU General Public License for more details.                       #
#                                                                       #
#    You should have received a copy of the GNU General Public License  #
#    along with this program; if not, write to the Free Software        #
#    Foundation, Inc., 51 Franklin Street, Fifth Floor,                 #
#    Boston, MA  02110-1301, USA.                                       #
#                                                                       #
#    ---                                                                #
#    Copyright (C) 2014, Alex Armstrong <AlexRArmstrong@gmail.com>      #
#                                                                       #
#########################################################################

# Naming convention:
# CONSTANTS
# ClassesLikeThis
# functionLikeThis
# variables_like_this

import sys
import os
import math
import pygame

from pygame.locals import KEYDOWN, QUIT

# Define global constants.
SNELLEN_RATIO, TEXT, SCALE_FACTOR = range(3)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
	
XMAX = 1248
YMAX = 1024

class Section(object):
	'''
	A section of a line.  Consists of a Snellen Ratio and text.  Initilize it
	by passing a Snellen Ratio and text.  If nothing is passed in, it will 
	initilize with empty ratio and text fields.
	'''
	def __init__(self, ratio = None, text = None):
		self.snellen_ratio = ratio
		self.text = text
	
	def snellenRatio(self):
		'''
		Returns the Snellen Ratio.
		'''
		return self.snellen_ratio
		
	def text(self):
		'''
		Returns the text.
		'''
		return self.text
		
	def setSnellenRatio(self, ratio):
		'''
		Sets the Snellen Ratio.  Takes the ratio to set, eg. 20/100.  Returns
		True on success, Flase on failure.
		'''
		try:
			self.snellen_ratio = ratio
			return True
		except:
			return False
		
	def setText(self, text):
		'''
		Sets the sections text.  Returns True on success, False on failure.
		'''
		try:
			self.text = text
			return True
		except:
			return False

class Line(object):
	'''
	A record of each line in a chart file.
	'''
	def __init__(self):
		pass
		
class Chart(object):
	'''
	A model of a chart
	'''
	def __init__(self):
		pass
		
class Projector(object):
	'''
	A digital projector.
	'''
	def __init__(self):
		pass
		
