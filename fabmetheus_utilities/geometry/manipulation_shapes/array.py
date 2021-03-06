"""
Boolean geometry array.

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.geometry_tools import matrix4x4
from fabmetheus_utilities.geometry.geometry_tools import vertex
from fabmetheus_utilities.geometry.geometry_utilities import evaluate
from fabmetheus_utilities import euclidean


__author__ = "Enrique Perez (perez_enrique@yahoo.com)"
__credits__ = 'Art of Illusion <http://www.artofillusion.org/>'
__date__ = "$Date: 2008/02/05 $"
__license__ = "GPL 3.0"


def getExecutionOrder():
	"Get the execution order."
	return 200

def getManipulatedPaths( close, loop, prefix, xmlElement ):
	"Get array path."
	arrayPaths = evaluate.getPathsByKeys( [ prefix + 'path', prefix + 'paths' ], xmlElement )
	manipulatedByPaths = []
	for arrayPath in arrayPaths:
		for arrayPoint in arrayPath:
			manipulatedByPath = []
			for point in loop:
				manipulatedByPath.append( point + arrayPoint )
			manipulatedByPaths.append( manipulatedByPath )
	manipulatedByVertices = []
	vertices = getVerticesByKey( prefix + 'vertices', xmlElement )
	for vertex in vertices:
		manipulatedByVertex = []
		for point in loop:
			manipulatedByVertex.append( point + vertex )
		manipulatedByVertices.append( manipulatedByVertex )
	manipulatedPaths = manipulatedByPaths + manipulatedByVertices
	if len( manipulatedPaths ) == 0:
		print( 'Warning, in getManipulatedPaths in array there are no paths or vertices for:' )
		print( xmlElement )
		return [ loop ]
	return manipulatedPaths

def getVerticesByKey( key, xmlElement ):
	"Get the vertices by key."
	return euclidean.getConcatenatedList( evaluate.getPathsByKey( key, xmlElement ) )

def processXMLElement( xmlElement, xmlProcessor ):
	"Process the xml element."
	target = evaluate.getXMLElementByKey( 'target', xmlElement )
	if target == None:
		print( 'Warning, array could not get target for:' )
		print( xmlElement )
		return
	vertices = getVerticesByKey( 'vertices', xmlElement )
	if len( vertices ) == 0:
		print( 'Warning, array could not get vertices for:' )
		print( xmlElement )
		return
	arrayDictionary = xmlElement.attributeDictionary.copy()
	targetMatrix4X4Copy = matrix4x4.Matrix4X4().getFromXMLElement( target )
	matrix4x4.setAttributeDictionaryToMatrix( target.attributeDictionary, targetMatrix4X4Copy )
	xmlElement.className = 'group'
	for vector3Index in xrange( len( vertices ) ):
		vector3 = vertices[ vector3Index ]
		vector3Matrix4X4 = matrix4x4.Matrix4X4( targetMatrix4X4Copy.matrixTetragrid )
		lastChild = target.getCopy( xmlElement.getIDSuffix( vector3Index ), xmlElement )
		euclidean.overwriteDictionary( xmlElement.attributeDictionary, [ 'id' ], [ 'visible' ], lastChild.attributeDictionary )
		vertexElement = vertex.getUnboundVertexElement( vector3 )
		matrix4x4.setXMLElementDictionaryToOtherElementDictionary( vertexElement, vector3Matrix4X4, lastChild )
	xmlProcessor.processXMLElement( xmlElement )
