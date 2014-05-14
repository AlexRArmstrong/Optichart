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
#
# Indent with TABS. Tabs are 4 spaces.

import argparse

def main():
	'''
	The main entry point.
	'''
	parser = argparse.ArgumentParser(description = 'Run an optichart projector.\
									If no arguments are given will run a projector.\
									Options allow testing of different modules.')
	parser.add_argument('-c','--chart', action = 'store_true', help = 'Run the Chart class test code.')
	args = parser.parse_args()
	
	if args.chart:
		# Test the Chart class.
		from Chart import Chart
		cn = '/home/alex/programing/optichart/charts/10-chart.chart'
		chart = Chart(cn)
		print chart
		for el in chart.lines():
			print el
			for es in el.sections():
				print es
				print es.text()
	else:
		# If we are executed, we start up a projector.
		from Projector import Projector
		projector = Projector()
		projector.startEventLoop()


if __name__ == '__main__':
	main()
