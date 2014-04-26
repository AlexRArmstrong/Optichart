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

class Section(object):
	'''
	A section of a line.  Consists of a Snellen Ratio and text.  Initilize it
	by passing a Snellen Ratio and text.  If nothing is passed in, it will 
	initilize with empty ratio and text fields.
	'''
	def __init__(self, ratio = None, text = None):
		self.snellen_ratio = ratio
		self._text = text
	
	def snellenRatio(self):
		'''
		Returns the Snellen Ratio.
		'''
		return self.snellen_ratio
		
	def text(self):
		'''
		Returns the text.
		'''
		return self._text
		
	def scaleFactor(self):
		'''
		Returns the decmial scale factor- the inverse of the Snellen ratio.  If
		no Snellen ratio has been defined returns False.
		'''
		if not self.snellen_ratio:
			return False
		numerator, denomerator = self.snellen_ratio.split('/')
		numerator = float(numerator)
		denomerator = float(denomerator)
		scale_factor = denomerator / numerator
		return scale_factor
		
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
			self._text = text
			return True
		except:
			return False

