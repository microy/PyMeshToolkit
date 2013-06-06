# -*- coding:utf-8 -*- 

# ***************************************************************************
#                                 VrmlFile.py
#                             -------------------
#    update               : 2013-06-05
#    copyright            : (C) 2013 by Michaël Roy
#    email                : microygt@gmail.com
# ***************************************************************************

# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************


#
# External dependencies
#
from Mesh import Mesh
from numpy import array
from string import maketrans


#
# Import mesh from a VRML 2.0 file
#
def ReadVrml( filename ) :
	# Initialisation
	vertices = []
	faces = []
	normals = []
	colors = []
	texcoords = []
        material = ""
	nlbrack = 0
	nrbrack = 0
	level = 0
	ixyz = 0
	nodes = []
	vec2d = [0., 0.]
	vec3d = [0., 0., 0.]
	vec3i = [0, 0, 0]
	previous_word = ""
	# Open the file
	vrmlfile = open( filename, 'r' )
	# Check the first line
	line = vrmlfile.readline()
	if "#VRML V2.0" not in line :
		vrmlfile.close()
		return None
	# Read each line in the file
	for line in vrmlfile :
		# Empty line
		if line.isspace() : continue
		# Comment
		if line.startswith( '#' ) : continue
		# Remove comma
		line = line.translate(maketrans( ",", " " ))
		# Buffer
		newline = ""
		for c in line :
			if c in [ '[', ']', '{', '}' ] :
				newline += ' ' + c + ' '
			else :
				newline += c
		# Split values in the line
		for word in newline.split() :
			# Left bracket or brace
			if word in [ "[", "{" ] :
				# Increment left deliminter number
				nlbrack += 1
				# Get level number
				level = nlbrack - nrbrack
				# Save level name
				if level > len(node) : node.append( previous_word )
				else : node[level] = previous_word
				# Initialize coordinate index
				ixyz = 0
			# Right bracket or brace
			else if word in [ "}", "]" ] :
				# Increment right deliminter number
				nrbrack += 1
				# Get level number
				level = nlbrack - nrbrack
				# Sanity check
				if level < 0 : return None
			# Comment
			else if word.startswith('#') :
				# Save current word
				previous_word = word
				# Next line
				break
			# Point
			else if node[level] == "point" :
				# Geometry
				if node[level-1] == "Coordinate" :
					# Get current value
					vec3d[ixyz] = map( float, word )
					# Complete coordinate ?
					if ixyz == 2 :
						vertices.append( vec3d )
						ixyz = 0
					else :
						ixyz += 1
				# Texture
				else if node[level-1] == "TextureCoordinate" :
					# Get current value
					vec2d[ixyz] = map( float, word )
					# Complete coordinate ?
					if ixyz == 1
						texcoords.append( vec2d ) 
						ixyz = 0
					else
						ixyz += 1
			



		# Vertex
		if values[0] == 'v' :
			vertices.append( map( float, values[1:4] ) )
		# Face (index starts at 1)
		elif values[0] == 'f' :
			faces.append( [ x-1 for x in map( int, values[1:4] ) ] )
		# Normal
		elif values[0] == 'n' :
			normals.append( map( float, values[1:4] ) )
		# Color
		elif values[0] == 'c' :
			colors.append( map( float, values[1:4] ) )
		# Texture
		elif values[0] == 'r' :
			texcoords.append( map( float, values[1:3] ) )
		# Texture filename
		elif values[0] == 'text' :
			material = values[1]
	# Return the final mesh
	return Mesh( name=filename, vertices=array(vertices), faces=array(faces),
		vertex_normals=array(normals), colors=array(colors),
		textures=array(texcoords), texture_name=material )

