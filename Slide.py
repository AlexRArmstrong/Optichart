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

class Slide(object):
	'''
	The text of a chart layed out and rendered.
	'''
	def __init__(self):
		'''
		Constructor.
		'''
		# These variables are created in Slide.
		# The chart object to display.
		self._chart = None
		# The coordinates of pages breaks.
		self._pages = []
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
	
	def setChartName(self, chart_name):
		'''
		Takes the path to a chart file and creates a chart object.
		'''
		try:
			self._chart = Chart(chart_name)
			return True
		except:
			return False
	
	def slideWidth(self):
		'''
		Returns the slide width in pixels.
		'''
		return self._width
	
	def setSlideWidth(self, width):
		'''
		Set the width for the slide to width (int). This is the
		number of pixels wide the slide's display area is.
		Returns True on succes, False otherwise.
		'''
		try:
			self._width = int(width)
			return True
		except:
			return False
	
	def slideHeight(self):
		'''
		Returns the height of the slide.
		'''
		return self._height
	
	def setSlideHeight(self, h):
		'''
		Set the height of the slides display area.
		Takes the height in pixels to set.
		Returns True on succes, False otherwise.
		'''
		try:
			self._height = int(h)
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

		all_rendered_lines = []
		all_lines = self._chart.lines()
		page_numbers = self._chart.pages()
		line_numbers = range(len(all_lines))
		slide_width = self._width # the width of the slide display area from config file.
		lane_length = self._lane_length
		dpi = self._dpi
		
		for current_line in all_lines:
			line_font = current_line.font()
			full_font_name = self.fixFontName(line_font)
			num_sections = len(current_line.sections())
			section_width = slide_width / num_sections
			sect_x = 0
			sect_y = 0
			all_rendered_sections = []
			line_height = 0
			for each_section in current_line:
				# Get the scaling factor and calculate the size in pixels
				scale_factor = each_section.scaleFactor()
				line_size = calculateSize(lane_length, scale_factor, dpi)
				# Create a font.
				section_font = pygame.font.Font(full_font_name, int(line_size))
				# Get the text for this section.
				text = each_section.text()
				num_chrs = len(text)
				text_width, text_height = section_font.size(text)
				space_width = (slide_width - text_width) / (num_chrs + 1.0)
				section_surface = pygame.Surface([section_width, text_height])
				if text_height > line_height:
					line_height = text_height
				x_pos = 0
				y_pos = 0
				x_pos += space_width
				for each_chr in text:
					chr_surface = section_font.render(each_chr, True, BLACK, YELLOW)
					chr_surface.set_colorkey(YELLOW)
					chr_position = [x_pos, y_pos]
					section_surface.blit(chr_surface, chr_position)
					x_pos += space_width
				all_rendered_sections.append(section_surface)
			line_surface = pygame.Surface([slide_width, line_height])
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
			# Calculate the space between each line - varies per line.
			scale_factor = all_lines[i].lineSpaceingScaleFactor()
			line_spaceing = calculateSize(lane_length, scale_factor, dpi)
			total_chart_heigh_px = total_chart_heigh_px + ln_height + line_spaceing
				
		# Make a big surface.
		#total_size = [total_chart_width_px, total_chart_heigh_px]
		total_size = [slide_width, total_chart_heigh_px]
		big_surf = pygame.Surface(total_size)
		big_surf.fill(WHITE)
		
		# Now render all the text to the big surface.
		position = [slide_width / 2, 0]
		for line_no, each_line in enumerate(all_rendered_text):
			x_r, y_r = each_line.get_size()
			position[0] = position[0] - (x_r / 2)
			big_surf.blit(each_line, position)
			
			position[0] = slide_width / 2
			position[1] += y_r + line_spaceing
			if line_no in page_numbers:
				x = 0
				y = position[1]
				pg_coords = [x, y]
				self._pages.append(pg_coords)
		
		
