#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

import os

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

def getFrame(mediaId, frameId):
	"""
	Returns serialized image frameId of the media mediaId and id of the next available frame id.
	frameId is an integer representing the offset in the frame list.
	"""
	if mediaId not in _resources:
		_loadFrames(mediaId)
		print("media {} is now in cache.".format(mediaId))
	image = {
				'size'  : os.path.getsize(_paths[mediaId][frameId]),
				'bytes' : _resources[mediaId][frameId],
				'nextId': getNextFrameId(mediaId, frameId)
			}
	return image

def getNextFrameId(mediaId, frameId):
	"""
	Returns the next available frame id for this media.
	If we reach the last frame available or a non-existing frame, we loop back to the beginning
	"""
	if frameId < len(_resources[mediaId]) - 1:
		return frameId + 1
	else:
		return 0

def _loadFrames(mediaId):
	"""
	Loads all frames for the media mediaId (into _resources).
	"""
	imageList = []
	for path in _paths[mediaId]:
		imageFile = open(path, 'rb')
		image = b''
		byte = imageFile.read(1)
		while b'' != byte:
			image += byte
			byte = imageFile.read(1)
		imageList.append(image)
		# TODO : handle resource not found
	_resources[mediaId] = imageList