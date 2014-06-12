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
#
# Indent with TABS. Tabs are 4 spaces.

import pygame

# Define global constants.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
JUMP = 40

class Mask(object):
	'''
	A black mask over some of the letters.
	'''
	
	def __init__(self, r):
		'''
		Initilize a new mask of size r where r is a pygame.Rect object 
		the max size the mask should cover.
		'''
		self._background_surface = pygame.Surface(r)
		self._background_surface.set_colorkey(WHITE)
		self._aperture = pygame.Rect((0, 0), r)
		self._slit = pygame.Rect((0, 0), r)
		self._max_size_rect = r
	
	def surface(self):
		'''
		Returns the masking surface.
		This is a surface with the supplied size that has part of it occluded.
		'''
		# Clip the vertical mask to be inside the horizontal mask.
		mask_rect = self._slit.clip(self._aperture)
		# Fill first with black to clear the old mask. Then paint the new mask.
		self._background_surface.fill(BLACK)
		self._background_surface.fill(WHITE, mask_rect)
		return self._background_surface
	
	def clear(self):
		'''
		Clear the mask.
		Sets the aperture to be the size of the chart, thus clearing the masking.
		'''
		self._aperture = pygame.Rect((0, 0), self._max_size_rect)
		self._slit = pygame.Rect((0, 0), self._max_size_rect)
	
	def increaseAperture(self):
		'''
		Increase the aperture size - make more text visible.
		'''
		self._aperture = self._aperture.inflate(0, JUMP)
	
	def decreaseAperture(self):
		'''
		Decrease the aperture size - make less text visible.
		'''
		self._aperture = self._aperture.inflate(0, -JUMP)
	
	def showLine(self, s):
		'''
		Show only a single line of size s pixels centered in the screen.
		'''
		# Calculate size of black border.
		# Could include a fudge factor, so that text will have space on either side,
		# but we calculate a much larger size when calling this so don't need it.
		y = self._aperture.height - s
		self._aperture = self._aperture.inflate(0, -y)
		# Could use a Snellen ratio, but then would have to account for dpi etc.
	
	def showSlit(self, size, position):
		'''
		Show a vertical slit of letters.
		Takes the horizontal size of the slit in pixels and the pixel location
		of the left edge - the top is always at the top of the screen.
		'''
		self._slit.width = size + 25
		self._slit.left = position
	
	def clearSlit(self):
		'''
		Remove the vertical slit.
		'''
		self._slit = self._max_size_rect
	
	def moveSlitRight(self):
		'''
		Move the vertical slit right.
		'''
		self._slit = self._slit.move(JUMP, 0)
	
	def moveSlitLeft(self):
		'''
		Move the vertical slit left.
		'''
		self._slit = self._slit.move(-JUMP, 0)
	
	def increaseSlitWidth(self):
		'''
		Make the vertical slit wider.
		'''
		self._slit = self._slit.inflate(JUMP, 0)
	
	def decreaseSlitWidth(self):
		'''
		Make the vertical slit narower.
		'''
		self._slit = self._slit.inflate(-JUMP, 0)
	
	def showSpot(self):
		'''
		Shows a spot of ??/?? size.
		'''
		pass
		# TODO: Does this need to be round?
	
	
	
	
