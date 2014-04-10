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
	A record of each line in a chart file.  Each line consists of line sections,
	with some extra data describing the line - the font, the default 
	character for that line and the line spacing between this line and the next.
	
	Can be initilized with a list of sections, a default character position 
	and a font name.  All are optional,	and if omitted the class will 
	return an empty line.
	'''
	def __init__(self, sections = [], def_chr = 0, font = None, line_space = '20/80'):
		# Sections is a list of all the sections that make up a line.
		self.sections = sections
		
		# The font for this line, if none should use default font.
		self.font_name = font
		
		# The default character to use when centering. If none supplied, use the
		# first character in the line.  This value the interger position of the
		# letter in the line - count from 0.
		self.default_character_position = def_chr
		
		# The distance between this and the next line.
		self.line_spaceing = line_space
		
	def sections(self):
		'''
		Return the sections that make up the line.
		'''
		return self.sections
		
	def font(self):
		'''
		Return the font use for this line, if any.
		'''
		return self.font_name
		
	def defaultCharacterPosition(self):
		'''
		Return the position of the Default Character.  This is the position of
		the character in the text of the line.  Start counting from 0.
		'''
		return self.default_character_position
		
	def lineSpaceing(self):
		'''
		Return the line spacing ratio.
		'''
		return self.line_spaceing
		
	def setFont(self, font):
		'''
		Set the font name for the line to font.  Return Ture on success, False
		otherwise.
		'''
		try:
			self.font_name = font
			return True
		except:
			return False
		
	def setDefaultCharacter(self, position):
		'''
		Set the position of the Default Character.  Takes an interger value.
		Returns True on succes, False otherwise.
		'''
		try:
			self.default_character_position = position
			return True
		except:
			return False
	
	def setLineSpacing(self, spacing):
		'''
		Sets the line spacing.  Is proper Snellen ratio. eg. 20/80.  Returns
		True on success, False otherwise.
		'''
		try:
			self.line_spaceing = spacing
			return True
		except:
			return False
	
	def addSection(self, section, position = None):
		'''
		Add a line section - consisting of a ratio and text. Position is optional
		and counts from 0.  If omitted the new section will be added to the end.
		'''
		# TODO: Decide on return value: True/False or the new list?
		if position:
			self.sections.insert(position, section)
		else:
			self.sections.append(section)
			
	def removeSection(self, section_position):
		'''
		Remove a ratio:text section at position section_position.
		'''
		del self.sections[section_position]
		# TODO: Decide on return value: True/False or the new list?
		
		
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
		
