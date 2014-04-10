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
#    Copyright (C) 2013, Alex Armstrong <AlexRArmstrong@gmail.com>      #
#                                                                       #
#########################################################################
# 
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

SNELLEN_RATIO, TEXT, SCALE_FACTOR = range(3)

def main():
	'''
	Initilize the program and start the main loop.
	'''
	global monitor_vert_size, lane_length, chart, dpi
	global current_chart_index, chart_list
	
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	
	XMAX = 1248
	YMAX = 1024
		
	# Chart array.
#	chart = [] -- I had this as a sortof global, I don't think it needs to be.
	
	monitor_vert_size = 11.0 # Inches
	lane_length = 240.0 # Inches
	
	def readConfig():
		'''
		Read the configuration file.
		'''
		global monitor_vert_size, lane_length
		file_handle = open('config.conf', 'r')
		for each_line in file_handle:
			if each_line.startswith('#'):
				continue
			elif each_line.isspace():
				continue
			elif each_line == '':
				continue
			elif 'monitor_size' in each_line:
					monitor_vert_size = each_line.split(':')[1].strip()
					monitor_vert_size = float(monitor_vert_size) / 24.5 # Convert mm to inches.
			elif 'lane_length' in each_line:
					lane_length = each_line.split(':')[1].strip()
					lane_length = float(lane_length) / 24.5 # Convert mm to inches.
			else:
				continue
		
		
	def readChart(chart_name):
		'''
		'''
		# Chart array.
		chart = []
		file_handle = open(chart_name, 'r')
		for each_line in file_handle:
			if each_line.startswith('#'):
				continue
			elif each_line.isspace():
				continue
			elif each_line == '':
				continue
			elif each_line.startswith('!'):
				continue
#				each_line.lower()
#				split_line = each_line.split(',')
#				for each_part in split_line:
#					key, value = each_part.strip('! ').split(':')
#					if key == 's':
#						size = int(value)
#				continue
			else:
				# Get the line.
				# split_line = each_line.split(':')
				# Then would parse the results, starting with the first one beign
				# a ratio, next letters, and repeiting. Might be able to add
				# control characters, but that would then require reworking the display function.
				ratio, text = each_line.split(':')
				ratio = ratio.strip()
				text = text.strip()
				# Figure out the scale factor - is the inverse of the Snellen ratio.
				numerator, denomerator = ratio.split('/')
				numerator = float(numerator)
				denomerator = float(denomerator)
				scale_factor = denomerator / numerator
				# Create a line record.
				line_record = [ratio, text, scale_factor]
				# Append the line to our chart arrary.
				chart.append(line_record)
			
		file_handle.close()
		return chart
		
	def setupDisplay():
		pass
		
	def findDpi():
		'''
		Find the display resoulition.
		'''
		try:
			args = ['xrandr', '-q', '-d', ':0']
			process = subprsocess.Popen(args, stdout=subprocess.PIPE)
			for line in iter(process.stdout.readline, ''):
				if isinstance(line, bytes):
					line = line.decode('utf-8')
				if 'primary' in line:
					print line #width_px = int(line.split()[3][:-])
		except:
			raise NotImplementedError('Not working.')
		
		
	def calculateSize(lane_length, scale_factor, dpi):
		'''
		Calculates the vertical size for a letter with a given scale factor at
		a distance on a specified resoulation monitor.
		'''
		vertical_inch_size = float(lane_length) * math.tan(math.radians(5.0 / 60.0)) * float(scale_factor)
		vertical_dpi_size = vertical_inch_size * dpi
		return vertical_dpi_size
		
	def disp2(chart_name):
		'''
		Takes a chart, loads and displays it.
		'''
		global lane_length, dpi
		global big_surf, top_left, viewport
		
		# Some initial values.
		size = 10
		position = [XMAX / 2, YMAX / 2]
		visible_size = 0
		visible_lines = []
		
		
		# Clear the screen.
		screen.fill(WHITE)
		
		# Read the chart and make an array with the data.
		chart = readChart(chart_name)
		
		# TODO: Need to render each letter with space between to make columns
		# correctly sized.
		all_rendered_text = []
		for each_line in chart:
			# Get the scaling factor and calculate the size in pixels
			size_factor = each_line[SCALE_FACTOR]
			line_size = calculateSize(lane_length, size_factor, dpi)
			# Create a font.
			font = pygame.font.Font(full_font_name, int(line_size))
			# Get the text to render.
			text = each_line[TEXT]
			# Create a rendered surface.
			text_surface = font.render(text, True, BLACK, WHITE)
			# Add the rendered surface to the list of all surfaces.
			all_rendered_text.append(text_surface)
		
		# Calculate the space between each line - a 20/80 line.
		line_spacing = calculateSize(lane_length, (80/20), dpi)
		
		# Find the total size of the chart.
		total_chart_heigh_px = 0
		total_chart_width_px = 0
		for each_line in all_rendered_text:
			ln_width, ln_height = each_line.get_size()
			total_chart_heigh_px = total_chart_heigh_px + ln_height + line_spacing
			if total_chart_width_px < ln_width:
				total_chart_width_px = ln_width
		# Make a big surface.
		#total_size = [total_chart_width_px, total_chart_heigh_px]
		total_size = [XMAX, total_chart_heigh_px]
		big_surf = pygame.Surface(total_size)
		big_surf.fill(WHITE)
		
		# Now render all the text to the big surface.
		position = [XMAX / 2, 0]
		for each_line in all_rendered_text:
			x_r, y_r = each_line.get_size()
			position[0] = position[0] - (x_r / 2)
			#position[1] = position[1] - (y_r / 2)
			
			big_surf.blit(each_line, position)
			position[0] = XMAX / 2
	#			print 'sur getsize', y_r
	#			print 'get ht', font.get_height()
	#			print 'line size', font.get_linesize()
	#			print 'font size', font.size('E')
			position[1] += y_r + line_spacing
		
		# This creates mirror writing.
	#	flip_surf = pygame.transform.flip(big_surf, True, False)
	#	big_surf.blit(flip_surf, (0, 0))
		
		top_left = [0, 0]
		viewport = pygame.Rect(0, -line_spacing, XMAX, YMAX)
		screen.blit(big_surf, top_left, viewport)
		
		pygame.display.update()
		
		
	def moveUp():
		global big_surf, top_left, viewport
		jump_dist = 40 # Pix
		screen.fill(WHITE)
		viewport = viewport.move(0, jump_dist)
		screen.blit(big_surf, top_left, viewport)
		pygame.display.update()
		
	def moveDown():
		global big_surf, top_left, viewport
		jump_dist = -40 # Pix
		screen.fill(WHITE)
		viewport = viewport.move(0, jump_dist)
		screen.blit(big_surf, top_left, viewport)
		pygame.display.update()
		
	def display(chart_name):
		'''
		Takes a chart, loads and displays it.
		'''
		global lane_length, dpi
		
		# Some initial values.
		size = 10
		position = [XMAX / 2, YMAX / 2]
		visible_size = 0
		visible_lines = []
		
		
		# Clear the screen.
		screen.fill(WHITE)
		
		# Read the chart and make an array with the data.
		chart = readChart(chart_name)
		
		
		all_rendered_text = []
		for each_line in chart:
			# Get the scaling factor and calculate the size in pixels
			size_factor = each_line[SCALE_FACTOR]
			line_size = calculateSize(lane_length, size_factor, dpi)
			# Create a font.
			font = pygame.font.Font(full_font_name, int(line_size))
			# Get the text to render.
			text = each_line[TEXT]
			# Create a rendered surface.
			text_surface = font.render(text, True, BLACK, WHITE)
			# Add the rendered surface to the list of all surfaces.
			all_rendered_text.append(text_surface)
		
		# Calculate the space between each line - a 20/80 line.
		line_spacing = calculateSize(lane_length, (80/20), dpi)
		
		# Now figure out how many lines we are going to display.
		for each_line in all_rendered_text:
			print visible_size
			print each_line.get_size()
			visible_size += each_line.get_height()
			if visible_size <= height_px:
				visible_size += line_spacing
				visible_lines.append(each_line)
			else:
				visible_size -= each_line.get_height()
				visible_size -= line_spacing
				break
				
		
			

		
		# Set up the vertical centering.
		extra_white_space = height_px - visible_size
		first_y = extra_white_space / 2
		position[1] = first_y
				
		# Now do the rendering.
		for each_line in visible_lines:
			x_r, y_r = each_line.get_size()
			position[0] = position[0] - (x_r / 2)
			#position[1] = position[1] - (y_r / 2)
			
			screen.blit(each_line, position)
			position[0] = XMAX / 2
	#			print 'sur getsize', y_r
	#			print 'get ht', font.get_height()
	#			print 'line size', font.get_linesize()
	#			print 'font size', font.size('E')
			position[1] += y_r + line_spacing
			
			
			
	#	flip_surf = pygame.transform.flip(screen, True, False)
	#	screen.blit(flip_surf, (0, 0))
		
		pygame.display.update()
		
		
		
	def mainLoop():
		global current_chart_index, chart_list
		while True:
			for each_event in pygame.event.get():
				if each_event.type == KEYDOWN:
					print each_event.dict # Debugging
					print each_event # Debugging
					if each_event.dict['key'] == 27:		# Esc Quits
						sys.exit()
					elif each_event.dict['key'] == 113:		# Q Quits
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
						# Add additional key presses here...
				if each_event.type == QUIT:
					sys.exit()
					
					
	# Set default directories and files.
	# These should probably be read in from the config file.
	# Charts
	chart_dir = 'charts'
	default_chart = '01-default-chart.chart'
	# Fonts
	font_dir = 'fonts'
	default_font = 'Sloan.ttf'
	
	start_dir = os.getcwd()
	
	# Read the config file.
	readConfig()
	
	# Set up the default font.
	full_font_name = os.path.join(start_dir, font_dir, default_font)
	
	# DEBUG
	#lf = pygame.font.get_fonts()
	#print lf
	#font_name = pygame.font.match_font('dejavusansmono')
	#font_name = '/home/alex/programing/optichart/Sloan.ttf'
	
	
	#Find the chart files.
	full_chart_dir = os.path.join(start_dir, chart_dir)
	# Change to the chart directory - need to be in this directory or else need
	# to use full path names and that's annoying.
	os.chdir(full_chart_dir)
	chart_list = os.listdir(full_chart_dir)
	chart_list.sort()
	current_chart_index = 0
	max_chart_index = len(chart_list) - 1 # Need minus one, 'cause count from zero!
	chart_name = chart_list[current_chart_index]
	
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
	disp2(chart_name)
	
	# Call the control loop
	mainLoop()
	
	

if __name__ == '__main__':
	main()
