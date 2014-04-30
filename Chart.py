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

import copy

from Section import Section
from Line import Line

class Chart(object):
	'''
	A model of a chart.  Consists of a series of lines along with data
	describing the page breaks and the chart file name.
	'''
	def __init__(self, chart_name):
		self.chart_name = chart_name
		self._lines = []
		self._pages = []
		
		file_handle = open(self.chart_name, 'r')
		self.readChartFile(file_handle)
		file_handle.close()
	
	def lines(self):
		'''
		Return the lines in the chart.
		'''
		return self._lines
		
	def addLine(self, line, pos = None):
		'''
		Adds a line to the list of lines, at optional position, pos.
		'''
		# Note use of copy.copy() here.  We want to make sure that each line
		# item is it's own.  This prevents us from getting a whole chart filled
		# with lines that reference the same memory location.
		
		# TODO: Decide on return value: True/False or the new list?
		if pos:
			self._lines.insert(pos, copy.copy(line))
		else:
			self._lines.append(copy.copy(line))
		
	def removeLine(self, pos):
		'''
		Removes the line at position pos.
		'''
		# TODO: Decide on return value: True/False or the new list?
		del self._lines[pos]
	
	def pages(self):
		'''
		Return the list of pages in the chart.
		'''
		return self._pages
		
	def addPage(self, pg):
		'''
		Appends a page to the number of pages. Returns True on success,
		False otherwise.
		'''
		try:
			self._pages.append(pg)
			return True
		except:
			return False
			
	def removePage(self, pos):
		'''
		Removes a page at position pos.  Returns True on success,
		False otherwise.
		'''
		try:
			del self._pages[pos]
			return True
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
				# chart file is loaded. BUT we DO clear the line sections - the
				# text and ratios or else we continue appending and get all sections
				# is all the lines.
				self.addLine(current_line)
				current_line.clearSections()
				continue
			else:
				print "I don't know how to handle this line: \n#%i, %s" %(i, all_lines[i])
				continue
		return True	
		
		
