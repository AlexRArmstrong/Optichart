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
		# Set defaults.
		# These are overwritten by settings in the config file.
		self.chart_dir = 'charts'
		
		self.font_dir = 'fonts'
		self.default_font = 'Sloan.ttf'
		
		# Dimensions in mm.
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
		self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
	#	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	#	screen = pygame.display.set_mode((XMAX, YMAX), pygame.FULLSCREEN)
	#	screen = pygame.display.set_mode((XMAX, YMAX))
		
		# Flag for red/green
		self.red_green = 0
		# Fill the screen with a while background.
		self.screen.fill(WHITE)
		# Must call update to actually display anything.
		pygame.display.update()
		
		# Calculate the vertical dpi.
		width_px, height_px = self.screen.get_size()
		XMAX = width_px
		YMAX = height_px
		print height_px #DEBUG
		print self.monitor_vert_size
		dpi = height_px / self.monitor_vert_size
		print 'dpi:', dpi
		
		# Create a slide of the chart.
		self.slide = Slide()
		self.slide.setDefaultFont(self.full_font_name)
		self.slide.setFontDirectory(self.font_dir)
		self.slide.setDpi(dpi)
		self.slide.setLaneLength(self.lane_length)
		self.slide.setSlideHeight(self.chart_vert_size)
		self.slide.setSlideWidth(self.chart_horz_size)
		
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
		
		# Clear the screen.
		self.screen.fill(BLUE)
		
		# This creates mirror writing.
	#	flip_surf = pygame.transform.flip(big_surf, True, False)
		
		top_left = [0, 0]
		#self.viewport = pygame.Rect(0, -line_spaceing, XMAX, YMAX)
		self.viewport = pygame.Rect(0, -80, XMAX, YMAX)
		self.screen.blit(self.slide_surface, top_left, self.viewport)
		
		pygame.display.update()
		
	def update(self):
		'''
		Update the screen.
		'''
		# First need to define what we're using.
		xc = (self.screen.get_width() - self.slide_surface.get_width()) / 2
		top_left = [xc, 0]
		background = pygame.Surface((XMAX, YMAX))
		letters = pygame.Surface((XMAX, YMAX))
		letters.blit(self.slide_surface, top_left, self.viewport)
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
	#	background.blit(mask)
		# Put the whole works on the screen.
		self.screen.blit(background, [0, 0])
		# Update the display.
		pygame.display.update()
	
	def moveUp(self):
		jump_dist = 40 # Pix
		self.viewport = self.viewport.move(0, jump_dist)
		self.update()
		
	def moveDown(self):
		jump_dist = -40 # Pix
		self.viewport = self.viewport.move(0, jump_dist)
		self.update()
	
	def toggleRedGreen(self):
		self.slide_surface.set_colorkey(WHITE)
		if not self.red_green:
			self.red_green = 1
			self.update()
		else:
			self.red_green = 0
			self.update()
	
	def pageUp(self):
		pass
	
	def pageDown(self):
		pass
	
	def startEventLoop(self):
		'''
		'''
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
						
					elif each_event.dict['key'] == 114:
						self.toggleRedGreen()
						# Add additional key presses here...
				if each_event.type == QUIT:
					sys.exit()
		
	
if __name__ == '__main__':
	# If we are executed, we start up a projector.
	#projector = Projector()
	#projector.startEventLoop()
	cn = '/home/alex/programing/optichart/charts/10-chart.chart'
	chart = Chart(cn)
	print chart
	for el in chart.lines():
		print el
		for es in el.sections():
			print es
			print es.text()
