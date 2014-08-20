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
import copy
import pygame

from pygame.locals import KEYDOWN, QUIT
from pygame.locals import K_x, K_q, K_RETURN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.locals import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9
from pygame.locals import K_EQUALS, K_MINUS

from Slide import Slide
from Mask import Mask

# Check if we have an IR Remote Control
try:
	import pylirc
	LIRC_ENABLED = True
	ir_key_map = {
				'Up' : K_UP,
				'Down' : K_DOWN,
				'Left' : K_LEFT,
				'Right' : K_RIGHT,
				'Enter' : K_RETURN,
				'Last' :  K_x,
				'Next' : K_EQUALS,
				'Previous' : K_MINUS,
				'0' : K_0,
				'1' : K_1,
				'2' : K_2,
				'3' : K_3,
				'4' : K_4,
				'5' : K_5,
				'6' : K_6,
				'7' : K_7,
				'8' : K_8,
				'9' : K_9,
				'\x1b' : K_q
				}
except ImportError:
	LIRC_ENABLED = False

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

JUMP = 40

XMAX = 1248
YMAX = 1024

class Projector(object):
	'''
	A digital projector.
	'''
	def __init__(self):
		'''
		Constructor.
		'''
		global XMAX, YMAX
		# Set defaults.
		# These are overwritten by settings in the config file.
		self.chart_dir = 'charts'
		
		self.font_dir = 'fonts'
		self.default_font = 'Sloan.ttf'
		
		# Dimensions in mm.
		# Builtin monitor and lane sizes.
		self.monitor_vert_size = 287.0
		self.lane_length = 6096.0
		
		# Flag for background color - 0 = White, 1 = Red/Green.
		self.background_flag = 0
		
		# Read the config file - possibly overwriting the defaults.
		self.readConfig()
		
		self.start_dir = os.getcwd()
		
		# Set up the default font.
		# TODO: Test the handeling of font pathing.
		# FIXME: Need to have full path.
		self.full_font_name = os.path.join(self.start_dir, self.font_dir, self.default_font)
		
		#Find the chart files.
		full_chart_dir = os.path.join(self.start_dir, self.chart_dir)
		# Change to the chart directory - need to be in this directory or else need
		# to use full path names and that's annoying.
		os.chdir(full_chart_dir)
		self.chart_list = os.listdir(full_chart_dir)
		self.chart_list.sort()
		self.current_chart_index = 0
		self.max_chart_index = len(self.chart_list) - 1 # Need minus one, 'cause count from zero!
		chart_name = self.chart_list[self.current_chart_index]
		
		# Initilize lirc if avialble, and register optichart as the client.
		if LIRC_ENABLED:
			ret_val = pylirc.init('optichart')
			if ret_val <= 0:
				print 'Error with lirc!', ret_val
			# Ensure that pylirc does not block.
			ret_val = pylirc.blocking(0)
			
		# Initilize pygame.
		pygame.init()
		
		# Set keyboard repeat (delay, interval).
		pygame.key.set_repeat(200, 10)
		
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
	#	size = (0, 0)
		size = (1920, 1080) # NOTE! The dpi depends on resolution and physical size if change one other must change too else get funny results.
	#	size = (1280, 768)
		self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
	#	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	#	screen = pygame.display.set_mode((XMAX, YMAX), pygame.FULLSCREEN)
	#	screen = pygame.display.set_mode((XMAX, YMAX))
		
		# Flag for red/green
		self.red_green = 0
		
		# Flag for Enter Button
		# We incriment this when changing from full screen to line mode to
		# character mode. So:
		# 0 - Full Screen.
		# 1 - Line Mode - first time.
		# 2 - Character Mode.
		# 3 - Line Mode - second time.
		self.mode = 0
		
		# Fill the screen with a while background.
		self.screen.fill(WHITE)
		# Must call update to actually display anything.
		pygame.display.update()
		
		# Calculate the vertical dpi.
		width_px, height_px = self.screen.get_size()
		print self.monitor_vert_size
		dpi = height_px / self.monitor_vert_size
		print 'dpi:', dpi
		
		# Asign screen x & y size values to global XMAX and YMAX.
		XMAX = width_px
		YMAX = height_px
		
		# Create a slide of the chart.
		self.slide = Slide()
		self.slide.setDefaultFont(self.full_font_name)
		self.slide.setFontDirectory(self.font_dir)
		self.slide.setDpi(dpi)
		self.slide.setLaneLength(self.lane_length)
		self.slide.setSlideHeight(self.chart_vert_size)
		self.slide.setSlideWidth(self.chart_horz_size)
		
		# Create the default viewport window. Move this to display() function
		# if need slides to reset to the default view when switching.
		# The viewport is the same size as the virtual chart projections size.
		self.viewport = pygame.Rect(0, 0, self.slide.slideWidth(), self.slide.slideHeight())
		# Move the viewport to show the top of the letters surface.
		self.viewport.left = 0
		self.viewport.top = -30
		
		# Creat a mask the same size as the viewport.  This means it only has
		# to mask what is visible, rather than the whole screen.
		self.mask = Mask(self.viewport.size)
		
		self.display(chart_name)
		self.update()
		
		
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
			elif each_line == '':
				continue
			elif each_line.startswith('MonitorVSize'):
				self.monitor_vert_size = each_line.split('=')[1].strip()
				self.monitor_vert_size = float(self.monitor_vert_size) / 25.4 # Convert mm to inches.
			elif each_line.startswith('MonitorHSize'):
				self.monitor_horz_size = each_line.split('=')[1].strip()
				self.monitor_horz_size = float(self.monitor_horz_size) / 25.4 # Convert mm to inches.
			elif each_line.startswith('ChartVSize'):
				self.chart_vert_size = each_line.split('=')[1].strip()
				self.chart_vert_size = float(self.chart_vert_size) / 25.4 # Convert mm to inches.
			elif each_line.startswith('ChartHSize'):
				self.chart_horz_size = each_line.split('=')[1].strip()
				self.chart_horz_size = float(self.chart_horz_size) / 25.4 # Convert mm to inches.
			elif each_line.startswith('LaneLength'):
				self.lane_length = each_line.split('=')[1].strip()
				self.lane_length = float(self.lane_length) / 25.4 # Convert mm to inches.
			elif each_line.startswith('ChartDir'):
				self.chart_dir = each_line.split('=')[1].strip()
			elif each_line.startswith('FontDir'):
				self.font_dir = each_line.split('=')[1].strip()
			elif each_line.startswith('DefaultFont'):
				self.default_font = each_line.split('=')[1].strip()
			else:
				print "I don't know how to handle this Config. line: \n%s" %(each_line)
				continue
		
		
		
	def display(self, chart_name):
		'''
		Takes a chart name, loads it and creates a slide surface.
		
		Must call self.update() after this function to draw the slide on
		the screen.
		'''
		self.slide.setChartName(chart_name)
		self.slide.layout()
		self.slide_surface = self.slide.surface()
		self.slide_surface.set_colorkey(WHITE)
		# Clear the screen.
	#	self.screen.fill(BLUE)
		
		# This creates mirror writing.
	#	self.slide_surface = pygame.transform.flip(self.slide_surface, True, False)
		
	def update(self):
		'''
		Update the screen.
		'''
		# First need to define what we're using.
		
		# Fill the screen background with black - creates a black border when
		# showing views that don't fill up the whole screen.
		self.screen.fill(BLACK)
		
		# Calculate the top left coordinates for positioning the slide.
		# An optimazation might be to have this as an instance variable rather
		# than compute it every time - depends on processor vs. memory tradeoff.
		monitor_height_px = self.screen.get_height()
		monitor_width_px = self.screen.get_width()
		slide_display_height =  self.slide.slideHeight()
		slide_display_width = self.slide.slideWidth()
		
		chart_projection_x = (monitor_width_px - self.viewport.width) / 2
		chart_projection_y = (monitor_height_px - self.viewport.height) / 2
		
		top_left = [chart_projection_x, chart_projection_y]
		
		virt_char_size = pygame.Rect(chart_projection_x, chart_projection_y, \
		                             self.slide.slideWidth(), self.slide.slideHeight())
		
		# Create the background surface for the letters.
		background = pygame.Surface(self.viewport.size)
		
		# Now fix the background for the chart - white or red/green.
		if self.red_green:
			left_rect = pygame.Rect(0, 0, self.viewport.width / 2, self.viewport.height)
			right_rect = pygame.Rect(self.viewport.width / 2, 0,  self.viewport.width, self.viewport.height)
			background.fill(RED, left_rect)
			background.fill(GREEN, right_rect)
		else:
			background.fill(WHITE)
		
		# Put the letters on the background. Only the letters in the viewport will
		# be shown - the viewport acts as a mask.
		background.blit(self.slide_surface, (0, 0), self.viewport)

		# Put the whole works on the screen.
		self.screen.blit(background, top_left)
		
		# Update the display.
		pygame.display.update()
	
	def moveUp(self):
		'''
		Scroll up by one line.
		'''
		# If we are showing a single line or character.
		if self.mode in (1, 2, 3):
			X = 0; Y = 1; SIZE = 2
			view_height = self.viewport.height
			current_coordinates = self.viewport.topleft
			all_coordinates_list = self.slide.defaultCharacters()
			all_y_diffs = []
			# Find the closest line.
			for i, each_coord_set in enumerate(all_coordinates_list):
				y_diff = each_coord_set[Y] - current_coordinates[Y]
				if y_diff < 0:
					continue
				all_y_diffs.append([y_diff, i])
			# Check for end of lines. Always have the current line in the diffs.
			if len(all_y_diffs) == 1:
				return
			all_y_diffs.sort()
			next_top_line = all_coordinates_list[all_y_diffs[1][1]]
			
			# Calculate the new line size.
			scale_factor = next_top_line[SIZE]
			next_line_size = self.slide.calculateSize(self.lane_length, scale_factor, self.slide.dpi())
			
			# Center the next line.
			gap = (view_height - next_line_size) / 2.0
			new_view_y = next_top_line[Y] - gap
			self.viewport.top = new_view_y
			
			# Resize the viewport.
			new_view_size = self.slide.calculateSize(self.lane_length, (scale_factor * 2), self.slide.dpi())
			delta_size  = view_height - new_view_size
			self.viewport = self.viewport.inflate(0, -delta_size)
			
			# Check for single letter isolation.
			if self.mode == 2:
				# We need to shrink the width of the viewport as well.
				self.viewport = self.viewport.inflate(-delta_size, 0)
				# And need to ensure centering is correct.
				chr_x = next_top_line[X]
				chr_width = next_top_line[3]
				gap = (new_view_size - chr_width) / 2.0
				position_x = chr_x - gap
				self.viewport.left = position_x
		
		# Else we will be in full screen mode and jump page wise.
		else:
			self.pageDown()
		
	def moveDown(self):
		# If we are showing a single line or character.
		if self.mode in (1, 2, 3):
			X = 0; Y = 1; SIZE = 2
			view_height = self.viewport.height
			current_coordinates = self.viewport.topleft
			all_coordinates_list = self.slide.defaultCharacters()
			all_y_diffs = []
			# Find the closest line.
			for i, each_coord_set in enumerate(all_coordinates_list):
				y_diff = current_coordinates[Y] - each_coord_set[Y]
				if y_diff < 0:
					continue
				all_y_diffs.append([y_diff, i])
			# Check for end of lines. Current line is negative so not here.
			if len(all_y_diffs) == 0 :
				return
			all_y_diffs.sort()
			next_top_line = all_coordinates_list[all_y_diffs[0][1]]
			
			# Calculate the new line size.
			scale_factor = next_top_line[SIZE]
			next_line_size = self.slide.calculateSize(self.lane_length, scale_factor, self.slide.dpi())
			
			# Center the next line.
			gap = (view_height - next_line_size) / 2.0
			new_view_y = next_top_line[Y] - gap
			self.viewport.top = new_view_y
			
			# Resize the viewport.
			new_view_size = self.slide.calculateSize(self.lane_length, (scale_factor * 2), self.slide.dpi())
			delta_size  = view_height - new_view_size
			self.viewport = self.viewport.inflate(0, -delta_size)
			
			# Check for single letter isolation.
			if self.mode == 2:
				# We need to shrink the width of the viewport as well.
				self.viewport = self.viewport.inflate(-delta_size, 0)
				# And need to ensure centering is correct.
				chr_x = next_top_line[X]
				chr_width = next_top_line[3]
				gap = (new_view_size - chr_width) / 2.0
				position_x = chr_x - gap
				self.viewport.left = position_x
		
		# Else we will be in full screen mode and jump page wise.
		else:
			self.pageUp()
	
	def moveRight(self):
		'''
		Move the viewport right. Moves on a per character basis if a mask is
		active, but in full screen and line modes changes charts.
		'''
		# If in full or line modes, go to next chart.
		if self.mode in (0, 1, 3):
			self.nextChart()
			return
		# If a mask is active:
		if self.viewport.width < self.slide.slideWidth():
			# Move on a per character basis.
			current_line_index = self.findClosestLine()
			default_characters_list = self.slide.defaultCharacters()
			current_line = default_characters_list[current_line_index]
			chr_width = current_line[3]
			space_size = current_line[4]
			JUMP = chr_width + space_size
		else:
			JUMP = 40
		# Check for edge of slide.
		# If the viewport will be off the slide area we want to prevent it from
		# moving any further.  Note that the signs (+/-) for the algebra are
		# reversed between left and right, so the behavior is what the user
		# expects.
		if self.viewport.centerx - JUMP <= 0:
			print 'degug right'
			return
		else:
			self.viewport.move_ip(-JUMP, 0)
	
	def moveLeft(self):
		'''
		Move the viewport left. Moves on a per character basis if a mask is
		active, but in full screen and line modes changes charts.
		'''
		# If in full or line modes, go to previous chart.
		if self.mode in (0, 1, 3):
			self.previousChart()
			return
		# If a mask is active:
		if self.viewport.width < self.slide.slideWidth():
			# Move on a per character basis.
			current_line_index = self.findClosestLine()
			default_characters_list = self.slide.defaultCharacters()
			current_line = default_characters_list[current_line_index]
			chr_width = current_line[3]
			space_size = current_line[4]
			JUMP = chr_width + space_size
		else:
			JUMP = 40
		# Check for edge of screen.
		if (self.viewport.centerx + JUMP) >= self.slide_surface.get_width():
			print 'debug left'
			return
		else:
			self.viewport.move_ip(JUMP, 0)
			
	def findClosestLine(self):
		'''
		Returns the index, in the default characters array, of the line 
		closest to the top of the viewport.
		'''
		X = 0; Y = 1
		current_coordinates = self.viewport.topleft
		default_characters_list = self.slide.defaultCharacters()
		all_y_diffs = []
		for i, each_set in enumerate(default_characters_list):
			y_diff = math.fabs(current_coordinates[Y] - each_set[Y])
			all_y_diffs.append([y_diff, i])
		closest_line = min(all_y_diffs)
		return closest_line[1]
	
	def findCenterLine(self):
		'''
		Returns the index, in the default characters array, of the line closest
		to the center of the viewport.
		'''
		view_center_y = self.viewport.centery
		def_chrs = self.slide.defaultCharacters()
		all_y_diffs = []
		for i, each_chr_position in enumerate(def_chrs):
			y_diff = math.fabs(view_center_y - each_chr_position[1])
			all_y_diffs.append([y_diff, i])
		closest_line = min(all_y_diffs)
		return closest_line[1]
		
	def checkVerticalCentering(self):
		'''
		Here we check that the current lines displayed are centered in the view.
		This ensures that none of them are cut off. Another way to think of it is
		that we check that the viewport displays only full lines.
		'''
		# Get the current top line.
		default_characters_list = self.slide.defaultCharacters()
		max_line_index = len(default_characters_list) - 1
		top_line_index = self.findClosestLine()
		top_line_data = default_characters_list[top_line_index]
		line_y = top_line_data[1]
		scale_factor = top_line_data[2]
		line_height = self.slide.calculateSize(self.lane_length, scale_factor, self.slide.dpi())
		# Check to see how much ot top line is visible.
		amount_visible = (line_y + line_height) - self.viewport.top
		line_half = line_height / 2.0
		if amount_visible >= line_half:
			top_line_y = top_line_data[1]
		else:
			# If less than half the top line is showing we want to use the next
			# line as the top line.
			top_line_index += 1
			# Make sure that we have a valid index.
			if top_line_index > max_line_index:
				top_line_index = max_line_index
			top_line_data = default_characters_list[top_line_index]
			top_line_y = top_line_data[1]
		# Find the bottom-most fully visible line.
		characters_after_current_line = default_characters_list[top_line_index:]
		for i, each_set in enumerate(characters_after_current_line):
			line_y = each_set[1]
			scale_factor = each_set[2]
			line_height = self.slide.calculateSize(self.lane_length, scale_factor, self.slide.dpi())
			page_bottom = line_y + line_height
			page_height = page_bottom - top_line_y
			if page_height < self.viewport.height:
				bottom_line_index = i
				bottom_line_lower_y = page_bottom
				continue
			else:
				break
		page_height = bottom_line_lower_y - top_line_y
		# Calculate total page height compared to viewport and vertical margins.
		top_margin = (self.viewport.height - page_height) / 2.0
		top_position = top_line_y - top_margin
		# Move viewport to correct position.
		self.viewport.top = top_position
		# Remember to call self.update() to actually display the changes.
		
	def isolateSingleLine(self):
		'''
		Isolates a single line in the center of the screen.
		'''
		# Find the closest line.
		view_center_y = self.viewport.centery
		def_chrs = self.slide.defaultCharacters()
		closest_line = self.findCenterLine()
		# Calculate mask size.
		scale_factor = def_chrs[closest_line][2]
		# The mask window should be twice the line size.
		size = self.slide.calculateSize(self.lane_length, (scale_factor * 2), self.slide.dpi())
		# Need to center closest line.
		y_jump = def_chrs[closest_line][1] + (size / 4.0) - view_center_y
		self.viewport = self.viewport.move(0, y_jump)
		# Now that full view is centered, we shrink it down to
		# the size we want, but keeping the same center point.
		y = self.viewport.height - size
		self.viewport.inflate_ip(0, -y)
		
	def isolateCharacter(self):
		'''
		Isolate a single character.
		'''
		# Need to find the closest line - this might be advoided if we kept an
		# instance variable for which line is in the center of the screen.
		def_chrs = self.slide.defaultCharacters()
		closest_line = self.findCenterLine()
		# Calculate size - window is 2x line size.
		scale_factor = def_chrs[closest_line][2]
		mask_size = self.slide.calculateSize(self.lane_length, (scale_factor * 2), self.slide.dpi())
		# Need to make the viewport the correct size first.
		x = self.viewport.width - mask_size
		self.viewport.inflate_ip(-x, 0)
		# Now center the window on the letter. We do this after
		# the window is the correct size.
		chr_x = def_chrs[closest_line][0]
		chr_width = def_chrs[closest_line][3]
		gap = (mask_size - chr_width) / 2.0
		position_x = chr_x - gap
		self.viewport.left = position_x
		
	def toggleRedGreen(self):
		if not self.red_green:
			self.red_green = 1
		else:
			self.red_green = 0
	
	def pageUp(self):
		page_coordinates = self.slide.pageCoordinates()
		view_top_y = self.viewport.top
		# All page markers should be closer than the end of the slide.
		min_diff = self.slide_surface.get_height()
		closest_marker = None
		# Find the closest page marker, 
		for i, each_pair in enumerate(page_coordinates):
			diff = view_top_y - each_pair[1]
			if diff < 51:
				continue
				# If a marker is within a few pixels, we ignore it,
				# also ignore markers where the diff is negative - they are 
				# page down markers (note that we reverse the diff code for pg dwn.
			if diff < min_diff:
				min_diff = diff
				closest_marker = i
	#Maybe can compare cloest marker to top coords and if same continue.??	
		if closest_marker is not None:
			y_jump = page_coordinates[closest_marker][1] - 20
			self.viewport.top = y_jump
		
		
	
	def pageDown(self):
		page_coordinates = self.slide.pageCoordinates()
		view_top_y = self.viewport.top
		min_diff = self.slide_surface.get_height()
		closest_marker = None
		for i, each_pair in enumerate(page_coordinates):
			diff = each_pair[1] - view_top_y
			if diff < 51:
				continue
			if diff < min_diff:
				min_diff = diff
				closest_marker = i
		if closest_marker is not None:
			y_jump = page_coordinates[closest_marker][1] - 20
			self.viewport.top = y_jump
	
	def nextChart(self):
		'''
		Move to the next chart in sequence.
		'''
		self.current_chart_index += 1
		if self.current_chart_index >= self.max_chart_index:
			self.current_chart_index = self.max_chart_index
		chart_name = self.chart_list[self.current_chart_index]
		self.display(chart_name)
		
		# If in single line mode, make sure that mask size is correct on
		# the new chart.
		if self.mode == 1:
			self.isolateSingleLine()
		
		self.checkVerticalCentering()
		self.update()
	
	def previousChart(self):
		'''
		Move to the previous chart in sequence.
		'''
		self.current_chart_index -= 1
		if self.current_chart_index <= 0:
			self.current_chart_index = 0
		chart_name = self.chart_list[self.current_chart_index]
		self.display(chart_name)
		
		if self.mode == 1:
			self.isolateSingleLine()
		
		self.checkVerticalCentering()
		self.update()
	
	def pollLircEvents(self):
		'''
		Create pygame events from lirc events.
		'''
		if not LIRC_ENABLED:
			return
		code_list = pylirc.nextcode()
		if code_list:
			for each_code in code_list:
				key_dict = {'key' : ir_key_map[each_code]}
				new_event = pygame.event.Event(pygame.KEYDOWN, key_dict)
				pygame.event.post(new_event)
	
	def exit(self):
		'''
		Code to clean up before exit.
		'''
		if LIRC_ENABLED:
			pylirc.exit()
		pygame.quit()
		sys.exit()
	
	def startEventLoop(self):
		'''
		The main key handeling event loop.
		'''
		while True:
			self.pollLircEvents()
			for each_event in pygame.event.get():
				if each_event.type == QUIT:
					self.exit()
				if each_event.type == KEYDOWN:
					print each_event.dict # Debugging
					print each_event # Debugging
					if each_event.key == K_q:				# q Quits
						self.exit()
					elif each_event.key == K_EQUALS:		# '=' - Next Chart
						self.nextChart()
					elif each_event.key == K_MINUS:			# '-' - Prev. Chart
						self.previousChart()
					elif each_event.key == K_RIGHT:			# Right Arrow Move Right
						self.moveRight()
					elif each_event.key == K_LEFT:			# Left Arrow Move Left
						self.moveLeft()
					elif each_event.key == K_UP:			# Up Arrow Scroll Up
						self.moveDown()
					elif each_event.key == K_DOWN:			# Down Arrow Scroll Down
						self.moveUp()
					elif each_event.key == K_2:				# 2 - Page up
						self.pageUp()
					elif each_event.key == K_8:				# 8 - Page down
						self.pageDown()
					elif each_event.key == K_x:				# x Toggles Red/Green
						self.toggleRedGreen()
					elif each_event.key == K_7:				# 7 - Bigger Horz. aperture
						self.viewport.inflate_ip(0, JUMP)
					elif each_event.key == K_1:				# 1 - Smaller Horz. aperture
						self.viewport.inflate_ip(0, -JUMP)
						if self.viewport.height < 0:
							self.viewport.height = 0
					elif each_event.key == K_9:				# 9 - Bigger Vert. slit
						self.viewport.inflate_ip(JUMP, 0)
					elif each_event.key == K_3:				# 3 - Smaller Vert. slit
						self.viewport.inflate_ip(-JUMP, 0)
						if self.viewport.width < 0:
							self.viewport.width = 0
					elif each_event.key == K_4:				# 4 - Move Vert. slit left
						self.viewport.move_ip(-JUMP, 0)
					elif each_event.key == K_6:				# 6 - Move Vert. slit right
						self.viewport.move_ip(JUMP, 0)
					elif each_event.key == K_RETURN:		# Enter is center btn.
						self.mode += 1
						if self.mode == 1:
							# Isolate just a single line.
							self.isolateSingleLine()
						elif self.mode == 2:
							# Isolate a single letter.
							self.isolateCharacter()
						elif self.mode == 3:
							# Return to viewing a full line.
							self.viewport.width = self.slide.slideWidth()
							self.viewport.left = 0
						else:
							self.mode = 0
							y = self.slide.slideHeight() - self.viewport.height
							self.viewport.inflate_ip(0, y)
							self.checkVerticalCentering()
							# We clear any mask that has been applied - this allows
							# for a 'return to default screen' ability.
							self.mask.clear()
						# Add additional key presses here...
					# After the screen status is changed by the key press we
					# call update() to draw the screen. At the current indentation
					# level it is only called once per key-press event. If we move
					# it out a level it will be called once per get-event call.
					self.update()

