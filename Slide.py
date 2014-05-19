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

import math
import pygame

from Chart import Chart

# Define global constants.
BLACK = (0, 0, 0)
NOTBLACK = (1, 1, 1)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

class Slide(object):
	'''
	The text of a chart layed out and rendered.
	'''
	def __init__(self, chart_name = None):
		'''
		Initilize a Slide Class. Call Slide([chart-name]) to create a Slide
		object.  Optionally passing a fully pathed chart name.
		'''
		# These variables are created in Slide.
		# The chart object to display.
		self._chart = None
		self._chart_name = ''
		if chart_name:
			self.setChartName(chart_name)
		# The coordinates of pages breaks.
		self._pages = [[0, 0]]
		# TODO: def chrs. ???
		self._default_characters = []
		# The text of the chart layed out and rendered.
		self._surface = None
		
		# These variables must be set before calling slide.layout()
		# The width and height of the slide display surface.
		self._width = 0 # Pixels
		self._height = 0 # Pixels
		# Fonts.
		self._default_font = ''
		self._font_dir = ''
		# Factors for size calculations.
		self._dpi = 72 # dots/inch
		self._lane_length = 240 # inches
		
		
	def chart(self):
		'''
		Returns a chart object.
		'''
		return self._chart
	
	def chartName(self):
		'''
		Return the current chart name.
		'''
		return self._chart_name
	
	def setChartName(self, chart_name):
		'''
		Takes the path to a chart file and creates a chart object. Additionally
		sets the chart name variable.
		'''
		try:
			self._chart_name = chart_name
			self._chart = Chart(chart_name)
			return True
		except:
			return False
	
	def pageCoordinates(self):
		'''
		Return a list of the (x,y) coordinates of the page breakes.
		'''
		return self._pages
	
	def defaultCharacters(self):
		'''
		Return a list of the default characters coordinates, and size.
		Data Structure:
		list = [[x, y, size],
				[x, y, size]]
		'''
		return self._default_characters
	
	def surface(self):
		'''
		Returns the rendered surface.
		'''
		return self._surface
		# TODO: Maybe calling layout() should return the rendered surface?
	
	def slideWidth(self):
		'''
		Returns the slide width in inches.
		'''
		return self._width / self._dpi
	
	def setSlideWidth(self, w):
		'''
		Set the width for the slide to w. This is the
		slide's display area in inches.  If using a custom dpi,
		Must call setDpi first - else will have the default 72 dpi.
		Returns True on succes, False otherwise.
		'''
		try:
			w_px = w * self._dpi
			self._width = int(w_px)
			return True
		except:
			return False
	
	def slideHeight(self):
		'''
		Returns the height of the slide.
		'''
		return self._height / self._dpi
	
	def setSlideHeight(self, h):
		'''
		Set the height of the slides display area to h.
		Takes the height in inches to set.
		Returns True on succes, False otherwise.
		'''
		try:
			h_px = h * self._dpi
			self._height = int(h_px)
			return True
		except:
			return False
	def dpi(self):
		'''
		Returns the slide's current dpi.
		'''
		return self._dpi
	
	def setDpi(self, dpi):
		'''
		Set the dpi for the slide.
		Returns True on succes, False otherwise.
		'''
		try:
			self._dpi = dpi
			return True
		except:
			return False
	
	def laneLength(self):
		'''
		Return the length of the lane for this slide.
		'''
		return self._lane_length
	
	def setLaneLength(self, length):
		'''
		Set the lane length for the slide.
		Returns True on succes, False otherwise.
		'''
		try:
			self._lane_length = int(length)
			return True
		except:
			return False
	
	def defaultFont(self):
		'''
		Return the default font used by this slide.
		'''
		return self._default_font
	
	def setDefaultFont(self, font_name):
		'''
		Sets the default font to use for this slide.
		Returns True on succes, False otherwise.
		'''
		try:
			self._default_font = font_name
			return True
		except:
			return False
	
	def fontDirectory(self):
		'''
		Returns the directory searched for fonts.
		'''
		return self._font_dir
	
	def setFontDirectory(self, font_dir):
		'''
		Sets the directory containing the fonts to 'font_dir'.
		Returns True on succes, False otherwise.
		'''
		try:
			self._font_dir = font_dir
			return True
		except:
			return False
	
	def fixFontName(self, font_name):
		'''
		Takes a font name and fixes the path so it can be used with pygame.
		Returns the full path name of the font.
		'''
		import os.path
		# First check to see if we have a font specified or should use default.
		if not font_name:
			return self._default_font
		elif os.path.isabs(font_name):
			return font_name
		elif os.path.exists(os.path.join(self._font_dir, font_name)):
			return os.path.join(self._font_dir, font_name)
		else:
			return self._default_font
	
	def calculateSize(self, lane_length, scale_factor, dpi):
		'''
		Calculates the vertical size for a letter with a given scale factor at
		a distance on a specified resoulation monitor.
		'''
		# TODO: Question? Should this be here or part of a line?
		vertical_inch_size = float(lane_length) * math.tan(math.radians(5.0 / 60.0)) * float(scale_factor)
		vertical_dpi_size = vertical_inch_size * dpi
		return vertical_dpi_size	
	
	def layout(self):
		'''
		Lays out the currently set chart.
		This needs to be called before trying to display the anything.
		Does display layout and renders the text onto a big surface.  Also
		checks for pages and default characters while doing this.
		'''
#		# Clear per slide/chart variables.
		self._pages = [[0, 0]]
		self._default_characters = []
		self._surface = None
		
		all_rendered_lines = []
		all_lines = self._chart.lines()
		page_numbers = self._chart.pages()
		slide_width = self._width # the width of the slide display area from config file.
		lane_length = self._lane_length
		dpi = self._dpi
		
		for line_no, current_line in enumerate(all_lines):
			line_font = current_line.font()
			full_font_name = self.fixFontName(line_font)
			num_sections = len(current_line.sections())
			section_width = slide_width / num_sections
			sect_x = 0
			sect_y = 0
			all_rendered_sections = []
			line_height = 0
			default_chr_position = 0
			for each_section in current_line.sections():
				# Get the scaling factor and calculate the size in pixels
				scale_factor = each_section.scaleFactor()
				line_size = self.calculateSize(lane_length, scale_factor, dpi)
				# Create a font.
				section_font = pygame.font.Font(full_font_name, int(line_size))
				# Get the text for this section.
				text = each_section.text()
				# Calculate the spacing of the letters for this section.
				num_chrs = len(text)
				text_width, text_height = section_font.size(text)
				chr_width = text_width / num_chrs
				space_width = (section_width - text_width) / (num_chrs + 1.0)
				# Create a surface for this section.
				section_surface = pygame.Surface([section_width, text_height])
				section_surface.fill(WHITE)
				# Keep track of how big the line is - different sections will change this.
				if text_height > line_height:
					line_height = text_height
				# Render each character onto a surface at the correctly spaced position.
				x_pos = 0
				y_pos = 0
				x_pos += space_width
				for each_chr in text:
					chr_surface = section_font.render(each_chr, True, BLACK, NOTBLACK)
					chr_surface.set_colorkey(NOTBLACK)
					chr_position = [x_pos, y_pos]
					section_surface.blit(chr_surface, chr_position)
					if default_chr_position == current_line.defaultCharacterPosition():
						self._default_characters.append([x_pos, y_pos, scale_factor])
					x_pos = x_pos + chr_width + space_width
					default_chr_position += 1
				all_rendered_sections.append(section_surface)
			# Now blit all the section surfaces onto a line surface.
			line_surface = pygame.Surface([slide_width, line_height])
			line_surface.fill(WHITE)
			for each_sect_surf in all_rendered_sections:
				section_position = [sect_x, sect_y]
				line_surface.blit(each_sect_surf, section_position)
				sect_x += section_width
			all_rendered_lines.append(line_surface)
		
		# Find the total height of the chart.
		total_chart_heigh_px = 0
		total_chart_width_px = 0
		num_lines = range(len(all_rendered_lines))
		for i in num_lines:
			cur_ren_line = all_rendered_lines[i]
			ln_width, ln_height = cur_ren_line.get_size()
			# Calculate the space between each line - can vary per line.
			scale_factor = all_lines[i].lineSpaceingScaleFactor()
			line_spaceing = self.calculateSize(lane_length, scale_factor, dpi)
			total_chart_heigh_px = total_chart_heigh_px + ln_height + line_spaceing
				
		# Make a big surface to hold all the lines.
		#total_size = [total_chart_width_px, total_chart_heigh_px]
		total_size = [slide_width, total_chart_heigh_px]
		self._surface = pygame.Surface(total_size)
		self._surface.fill(WHITE)
		
		# Now render all the text to the big surface.
		position = [slide_width / 2, 0]
		for line_no, each_line in enumerate(all_rendered_lines):
			x_r, y_r = each_line.get_size()
			position[0] = position[0] - (x_r / 2)
			self._surface.blit(each_line, position)
			# Y for def chrs.
			self._default_characters[line_no][1] = position[1]
			# Figure out the coordinates for the page breaks.
			if line_no in page_numbers:
				x = 0
				y = position[1]
				pg_coords = [x, y]
				self._pages.append(pg_coords)
			# Incriment the position for the next line.
			position[0] = slide_width / 2
			position[1] += y_r + line_spaceing
			
		# Add an end coordinate to the pages.
		max_y = self._surface.get_height()
		chart_end = [0, max_y]
		self._pages.append(chart_end)
