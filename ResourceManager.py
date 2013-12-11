# -*-coding:Utf-8 -*

import os

"""
ResourceManager gets the images and loads them in memory whenever they are
accessed via getFrame.
"""

_resources = { }
_paths = { }
CHUNK_SIZE = 5

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
	if mediaId not in _resources or frameId not in _resources.get(mediaId, []):
		_loadFramesChunk(mediaId, int(frameId / CHUNK_SIZE))
		print("media {} (frames {} to {}) is now in cache."
			.format(mediaId, frameId, frameId + CHUNK_SIZE))
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
	if frameId < len(_paths[mediaId]) - 1:
		return frameId + 1
	else:
		return 0

def _loadFramesChunk(mediaId, chunkNumber):
	"""
	Loads all frames for the media mediaId (into _resources),
	CHUNK_SIZE by CHUNK_SIZE (ex: 5 by 5).
	"""
	# TODO : handle resource not found
	imageList = []
	index = chunkNumber * CHUNK_SIZE
	i = index
	for path in _paths[mediaId][index:index + CHUNK_SIZE]:
		if mediaId not in _resources:
			_resources[mediaId] = {}
		imageFile = open(path, 'rb')
		image = b''
		byte = imageFile.read(1)
		while b'' != byte:
			image += byte
			byte = imageFile.read(1)
		_resources[mediaId][i] = image
		i += 1