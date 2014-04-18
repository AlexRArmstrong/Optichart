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
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

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
	A model of a chart.  Consists of a series of lines along with data
	describing the page breaks and the chart file name.
	'''
	def __init__(self, chart_name):
		self.chart_name = chart_name
		self.lines = []
		self.pages = []
		
		file_handle = open(self.chart_name, 'r')
		self.readChartFile(file_handle)
		file_handle.close()
	
	def lines(self):
		'''
		Return the lines in the chart.
		'''
		return self.lines
		
	def addLine(self, line, pos = None):
		'''
		Adds a line to the list of lines, at optional position, pos.
		'''
		# TODO: Decide on return value: True/False or the new list?
		if pos:
			self.lines.insert(pos, line)
		else:
			self.lines.append(line)
		
	def removeLine(self, pos):
		'''
		Removes the line at position pos.
		'''
		# TODO: Decide on return value: True/False or the new list?
		del self.lines[pos]
	
	def pages(self):
		'''
		Return the list of pages in the chart.
		'''
		return self.pages
		
	def addPage(self, pg):
		'''
		Appends a page to the number of pages. Returns True on success,
		False otherwise.
		'''
		try:
			self.pages.append(pg)
			return True
		except:
			return False
			
	def removePage(self, pos):
		'''
		Removes a page at position pos.  Returns True on success,
		False otherwise.
		'''
		try:
			del self.pages[pos]
			return Ture
		except:
			return False
		# TODO: Is this a good way to do return values?
		
	def readChartFile(self, file_handle):
		'''
		Here we do the heavy lifting of parsing the chart file. Should only be
		called from the constructor, and takes a file handle as argument.
		'''
		# Read the file into memory.
		all_lines = file_handle.readlines()
		# Now create an itteratible array so we know which line we're on.
		line_numbers = range(len(all_lines))
		# Create a line.
		current_line = Line()
		# Now read the lines.
		for i in line_numbers:
			# Ignore comments.
			if all_lines[i].startswith('#'):
				continue
			# Ignore blank lines.
			elif all_lines[i].isspace():
				continue
			# When we find ! set that line in the pages array.
			elif all_lines[i].startswith('!'):
				self.addPage(i)
				continue
			# If we find a Font, set the line font.
			elif all_lines[i].upper().startswith('FONT'):
				line = all_lines[i]
				key, value = line.split('=')
				current_line.setFont(value.strip())
				continue
			# If we find a Linesize spec., set line spacing.
			elif all_lines[i].upper().startswith('LINESIZE'):
				line = all_lines[i]
				key, value = line.split('=')
				current_line.setLineSpacing(value.strip())
				continue
			# If we have a data line...
			elif all_lines[i].upper().startswith('20'):
				line = all_lines[i]
				# Check for multiple columns.
				line_sections = line.split('|')
				for each_section in line_sections:
					ratio, text = each_section.split(':')
					ratio = ratio.strip()
					text = text.strip()
					if text.startswith('"') or text.startswith("'"):
						text = text.strip('"\'')
					# Add a section to the current line.
					a_section = Section(ratio, text)
					current_line.addSection(a_section)
					# Check for default character
					default_chr_pos = 0
					num_chrs = range(len(text))
					for n in num_chrs:
						if text[n] == '*':
							default_chr_pos = n + 1
							if default_chr_pos >= len(text):
								default_chr_pos = len(text) - 1
							current_line.setDefaultCharacter(default_chr_pos)
							break
						else:
							current_line.setDefaultCharacter(default_chr_pos)
							continue
				# Done parsing line. Now add it to the chart.
				# Note we do NOT creat a new line, as this would clear the spacing
				# and font and those are only cleared if specified again or a new
				# chart file is loaded.
				self.addLine(current_line)
				continue
			else:
				print "I don't know how to handle this line: \n#%i, %s" %(i, all_lines[i])
				continue
		return True	
		
class Projector(object):
	'''
	A digital projector.
	'''
	def __init__(self):
		'''
		Constructor.
		'''
		# Set defaults.
		# These are overwritten by settings in the config file.
		self.chart_dir = 'charts'
		
		self.font_dir = 'fonts'
		self.default_font = 'Sloan.ttf'
		
		self.monitor_vert_size = 287
		self.lane_length = 6096
		
		# Flag for background color - 0 = White, 1 = Red/Green.
		self.background_flag = 0
		
		# Read the config file - possibly overwriting the defaults.
		readConfig()
		
		self.start_dir = os.getcwd()
		
		# Set up the default font.
		self.full_font_name = os.path.join(self.start_dir, self.font_dir, self.default_font)
		
		#Find the chart files.
		full_chart_dir = os.path.join(start_dir, chart_dir)
		# Change to the chart directory - need to be in this directory or else need
		# to use full path names and that's annoying.
		os.chdir(full_chart_dir)
		self.chart_list = os.listdir(full_chart_dir)
		self.chart_list.sort()
		self.current_chart_index = 0
		self.max_chart_index = len(self.chart_list) - 1 # Need minus one, 'cause count from zero!
		chart_name = self.chart_list[current_chart_index]
		
		# Initilize pygame.
		pygame.init()
		
		# Find DPI
		# Some versions of xrandr will return a resolution in pixles and a size in mm.
		# However this dosesn't work on all systems.
		# So we are going to ask SDL for a full screen window at whatever size happens
		# to be the current size.  We then figure out what dpi we are dealing with
		# based on a physical measurement entered in the config file and the returned
		# SDL surface size.
		# May need (on some systems) to actually specifiy what size we want.
		
		# Create a screen.
		# Calling set_mode with zeros will return a surface the same size as the
		# current display.
		screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
	#	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	#	screen = pygame.display.set_mode((XMAX, YMAX), pygame.FULLSCREEN)
	#	screen = pygame.display.set_mode((XMAX, YMAX))
		
		# Fill the screen with a while background.
		screen.fill(WHITE)
		# Must call update to actually display anything.
		pygame.display.update()
		
		# Calculate the vertical dpi.
		width_px, height_px = screen.get_size()
		XMAX = width_px
		YMAX = height_px
		print height_px #DEBUG
		print monitor_vert_size
		dpi = height_px / monitor_vert_size
		print 'dpi:', dpi
		
		# Show the first chart.
		#display(chart_name)
		display(chart_name)
		
		# Call the control loop
		#mainLoop() - not here, should call this from where class is created.
		# - this would imideatly take over and that might not be desirable.
		
	def readConfig(self):
		'''
		Read the configuration file. Should only be called from the init function.
		'''
		file_handle = open('config.conf', 'r')
		for each_line in file_handle:
			each_line = each_line.strip()
			if each_line.startswith('#'):
				continue
			elif each_line.isspace():
				continue
			elif each_line.startswith('MonitorVSize'):
				self.monitor_vert_size = each_line.split('=')[1].strip()
				self.monitor_vert_size = float(self.monitor_vert_size) / 24.5 # Convert mm to inches.
			elif each_line.startswith('MonitorHSize'):
				self.monitor_horz_size = each_line.split('=')[1].strip()
				self.monitor_horz_size = float(self.monitor_horz_size) / 24.5 # Convert mm to inches.
			elif each_line.startswith('ChartVSize'):
				self.chart_vert_size = each_line.split('=')[1].strip()
				self.chart_vert_size = float(self.chart_vert_size) / 24.5 # Convert mm to inches.
			elif each_line.startswith('ChartHSize'):
				self.chart_horz_size = each_line.split('=')[1].strip()
				self.chart_horz_size = float(self.chart_horz_size) / 24.5 # Convert mm to inches.
			elif each_line.startswith('LaneLength'):
				self.lane_length = each_line.split('=')[1].strip()
				self.lane_length = float(self.lane_length) / 24.5 # Convert mm to inches.
			elif each_line.startswith('ChartDir'):
				self.chart_dir = each_line.split('=')[1].strip()
			elif each_line.startswith('FontDir'):
				self.font_dir = each_line.split('=')[1].strip()
			elif each_line.startswith('DefaultFont'):
				self.default_font = each_line.split('=')[1].strip()
			else:
				print "I don't know how to handle this line: \n%s" %(each_line)
				continue
		
		
		
	def display(self):
		pass
	
	def eventLoop(self):
		'''
		'''
		global current_chart_index, chart_list
		while True:
			for each_event in pygame.event.get():
				if each_event.type == KEYDOWN:
					print each_event.dict # Debugging
					print each_event # Debugging
					if each_event.dict['key'] == 27:		# Esc Quits
						pygame.quit()
						sys.exit()
					elif each_event.dict['key'] == 113:		# Q Quits
						pygame.quit()
						sys.exit()
					elif each_event.dict['key'] == 275:		# Right Arrow Next Chart
						print 'RIGHT' #Debug
						current_chart_index += 1
						if current_chart_index >= max_chart_index:
							current_chart_index = max_chart_index
						chart_name = chart_list[current_chart_index]
						disp2(chart_name)
					elif each_event.dict['key'] == 276:		# Left Arrow Prev. Chart
						print 'LEFT' # Debug
						current_chart_index -= 1
						if current_chart_index <= 0:
							current_chart_index = 0
						chart_name = chart_list[current_chart_index]
						disp2(chart_name)
					elif each_event.dict['key'] == 273:		# Up Arrow Scroll Up
						print 'UP' # Debug
						moveUp()
						
					elif each_event.dict['key'] == 274:		# Down Arrow Scroll Down
						print 'DOWN' # Debug
						moveDown()
						
					elif each_event.dict['key'] == 114:
						togleRedGreen()
						# Add additional key presses here...
				if each_event.type == QUIT:
					sys.exit()
		
	
if __name__ == '__main__':
	# If we are executed, we start up a projector.
	projector = Projector()
	projector.eventLoop()
