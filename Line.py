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
		self._sections = sections
		
		# The font for this line, if none should use default font.
		self.font_name = font
		
		# The default character to use when centering. If none supplied, use the
		# first character in the line.  This value the interger position of the
		# letter in the line - count from 0.
		self.default_character_position = def_chr
		
		# The distance between this and the next line.
		self.line_spaceing = line_space
		
	def __getitem__(self, offset):
		return self._sections[offset]
		
	def sections(self):
		'''
		Return the sections that make up the line.
		'''
		return self._sections
		
	def font(self):
		'''
		Return the font use for this line.  If no font has been specified,
		it will return None.
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
		Return the line spacing snellen ratio.
		'''
		return self.line_spaceing
		
	def lineSpaceingScaleFactor(self):
		'''
		Returns the decmial scale factor- the inverse of the Snellen ratio.  If
		no Snellen ratio has been defined returns False.
		'''
		if not self.line_spaceing:
			return False
		numerator, denomerator = self.line_spaceing.split('/')
		numerator = float(numerator)
		denomerator = float(denomerator)
		scale_factor = denomerator / numerator
		return scale_factor
		
	def setFont(self, font):
		'''
		Set the font name for the line to font.  Return True on success, False
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
			self._sections.insert(position, section)
		else:
			self._sections.append(section)
			
	def removeSection(self, section_position):
		'''
		Remove a ratio:text section at position section_position.
		'''
		del self._sections[section_position]
		# TODO: Decide on return value: True/False or the new list?
		
	def clearSections(self):
		'''
		Clear the line of ratio/text sections, but perserving the formating,
		spacing, font and default character.
		'''
		self._sections = []
		
		
