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

from Slide import Slide
from Mask import Mask

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
		# Flag for center/Enter button
		self.enter = 0
		
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
		
		self.mask = Mask(size)
		
		# Create the default viewport window. Move this to display if need
		# slides to reset to the default view when switching.
		self.viewport = pygame.Rect(0, -80, XMAX, YMAX)
		
		self.display(chart_name)
		
		
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
		Takes a chart name, loads and displays it.
		'''
		self.slide.setChartName(chart_name)
		self.slide.layout()
		self.slide_surface = self.slide.surface()
		self.slide_surface.set_colorkey(WHITE)
		# Clear the screen.
	#	self.screen.fill(BLUE)
		
		# This creates mirror writing.
	#	self.slide_surface = pygame.transform.flip(self.slide_surface, True, False)
		
		self.update()
		
	def update(self):
		'''
		Update the screen.
		'''
		# First need to define what we're using.
		
		# Fill the screen background with black - creates a black border when
		# showing charts that don't fill up the whole screen.
		self.screen.fill(BLACK)
		
		# Calculate the top left coordinates for positioning the slide.
		monitor_height_px = self.screen.get_height()
		monitor_width_px = self.screen.get_width()
		slide_display_height =  self.slide.slideHeight()
		slide_display_width = self.slide.slideWidth()
		
		chart_projection_x = (monitor_width_px - slide_display_width) / 2
		chart_projection_y = (monitor_height_px - slide_display_height) / 2
		
		top_left = [chart_projection_x, chart_projection_y]
		
		virt_char_size = pygame.Rect(chart_projection_x, chart_projection_y, self.slide.slideWidth(), self.slide.slideHeight())
		
		# Create the background surface for the letters.
		background = pygame.Surface((XMAX, YMAX))
		
		# Now fix the background for the chart - white or red/green.
		if self.red_green:
			left_rect = pygame.Rect(0, 0, XMAX / 2, YMAX)
			right_rect = pygame.Rect(XMAX / 2, 0,  XMAX, YMAX)
			background.fill(RED, left_rect)
			background.fill(GREEN, right_rect)
		else:
			background.fill(WHITE)
		# Put the letters on the background.
		background.blit(self.slide_surface, top_left, self.viewport)
		# Put the mask (if any) on the letters.
		mask_surface = self.mask.surface()
		background.blit(mask_surface, [0, 0])
		# Put the whole works on the screen.
		self.screen.blit(background, top_left, virt_char_size)
		# Update the display.
		pygame.display.update()
	
	def moveUp(self):
		jump_dist = 20 # Pix
		self.viewport = self.viewport.move(0, jump_dist)
		self.update()
		
	def moveDown(self):
		jump_dist = -20 # Pix
		self.viewport = self.viewport.move(0, jump_dist)
		self.update()
	
	def toggleRedGreen(self):
		if not self.red_green:
			self.red_green = 1
			self.update()
		else:
			self.red_green = 0
			self.update()
	
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
		
		if closest_marker is not None:
			y_jump = page_coordinates[closest_marker][1] - 50
			self.viewport.top = y_jump
		
		self.update()
		
	
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
			y_jump = page_coordinates[closest_marker][1] - 50
			self.viewport.top = y_jump
		self.update()
	
	def startEventLoop(self):
		'''
		'''
		while True:
			for each_event in pygame.event.get():
				if each_event.type == QUIT:
					sys.exit()
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
						self.current_chart_index += 1
						if self.current_chart_index >= self.max_chart_index:
							self.current_chart_index = self.max_chart_index
						chart_name = self.chart_list[self.current_chart_index]
						self.display(chart_name)
					elif each_event.dict['key'] == 276:		# Left Arrow Prev. Chart
						print 'LEFT' # Debug
						self.current_chart_index -= 1
						if self.current_chart_index <= 0:
							self.current_chart_index = 0
						chart_name = self.chart_list[self.current_chart_index]
						self.display(chart_name)
					elif each_event.dict['key'] == 273:		# Up Arrow Scroll Up
						print 'UP' # Debug
						self.moveUp()
					elif each_event.dict['key'] == 274:		# Down Arrow Scroll Down
						print 'DOWN' # Debug
						self.moveDown()
					elif each_event.dict['key'] == 264:		# 8 - Page up
						self.pageUp()
					elif each_event.dict['key'] == 258:		# 2 - Page down
						self.pageDown()
					elif each_event.dict['key'] == 114:		# r Toggles Red/Green
						self.toggleRedGreen()
					elif each_event.dict['key'] == 263:		# 7 - Bigger Horz. aperture
						self.mask.increaseAperture()
						self.update()
					elif each_event.dict['key'] == 257:		# 1 - Smaller Horz. aperture
						self.mask.decreaseAperture()
						self.update()
					elif each_event.dict['key'] == 265:		# 9 - Bigger Vert. slit
						self.mask.increaseSlitWidth()
						self.update()
					elif each_event.dict['key'] == 259:		# 3 - Smaller Vert. slit
						self.mask.decreaseSlitWidth()
						self.update()
					elif each_event.dict['key'] == 260:		# 4 - Move Vert. slit left
						self.mask.moveSlitLeft()
						self.update()
					elif each_event.dict['key'] == 262:		# 6 - Move Vert. slit right
						self.mask.moveSlitRight()
						self.update()
					elif each_event.dict['key'] == 13:		# Enter is center btn.
						self.enter += 1
						if self.enter == 1 or self.enter == 3:
							# Find the closest line.
							view_center_y = self.viewport.centery
							def_chrs = self.slide.defaultCharacters()
							all_y_diffs = []
							for i, each_chr_position in enumerate(def_chrs):
								y_diff = math.fabs(view_center_y - each_chr_position[1])
								all_y_diffs.append([y_diff, i])
							closest_line = min(all_y_diffs)
							# Calculate mask size and apply mask.
							scale_factor = def_chrs[closest_line[1]][2]
							size = self.slide.calculateSize(self.lane_length, scale_factor, self.slide.dpi())
							self.mask.clear()
							self.mask.showLine(size)
							# Need to center closest line.
							y_jump = def_chrs[closest_line[1]][1] + (size / 2.0) - view_center_y
							self.viewport = self.viewport.move(0, y_jump)
						elif self.enter == 2:
							# Need to find the closest line, 
							view_center_y = self.viewport.centery
							def_chrs = self.slide.defaultCharacters()
							all_y_diffs = []
							for i, each_chr_position in enumerate(def_chrs):
								y_diff = math.fabs(view_center_y - each_chr_position[1])
								all_y_diffs.append([y_diff, i])
							closest_line = min(all_y_diffs)
							# Calculate size and apply mask.
							scale_factor = def_chrs[closest_line[1]][2]
							size = self.slide.calculateSize(self.lane_length, scale_factor, self.slide.dpi())
							position = (self.viewport.width - self.slide.surface().get_width()) / 2 + def_chrs[closest_line[1]][0]
							self.mask.showSlit(size, position)
						else:
							self.enter = 0
							self.mask.clear()
						self.update()
					# Add additional key presses here...
				
