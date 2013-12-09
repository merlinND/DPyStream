#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

"""
ResourceManager gets the images and loads them in memory whenever they are
accessed via getFrame.
"""

_resources = { }
_paths = { }

def addResource(mediaId, framePaths):
	"""
	Saves all given paths under the id mediaId WITHOUT loading the files.
	Once a resource is added, it can be retrieved via the getFrame.
	"""
	_paths[mediaId] = framePaths
	print(framePaths)

def getFrame(mediaId, frameId):
	"""
	Returns serialized image frameId of the media mediaId.
	frameId is an integer representing the offset in the frame list.
	"""
	if mediaId not in _resources:
		_loadFrames(mediaId)
	return _resources[mediaId][frameId]

def _loadFrames(mediaId):
	"""
	Loads all frames for the media mediaId (into _resources).
	"""
	imageList = []
	for path in _paths[mediaId]:
		imageList.append(open(path, 'rb+'))
	_resources[mediaId] = imageList