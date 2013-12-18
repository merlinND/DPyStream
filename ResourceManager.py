# -*-coding:Utf-8 -*
"""
ResourceManager gets the images and loads them in memory whenever they are
accessed via getFrame.
"""

_resources = { } # { '/fh/path' : [b'', b'', b''] }
_paths = { } # { 1 : ['/fh/path1', '/fh/path2'] }
BATCH_SIZE = 2

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
	if _paths[mediaId][frameId] not in _resources:
		_loadFrameBatch(mediaId, int(frameId / BATCH_SIZE))

	return (_resources[_paths[mediaId][frameId]], getNextFrameId(mediaId, frameId))

def getNextFrameId(mediaId, frameId):
	"""
	Returns the next available frame id for this media.
	If we reach the last frame available or a non-existing frame, we loop back to the beginning
	"""
	if frameId < len(_paths[mediaId]) - 1:
		return frameId + 1
	else:
		return 0

def _loadFrameBatch(mediaId, batchNumber):
	"""
	Loads all frames for the media mediaId (into _resources),
	BATCH_SIZE by BATCH_SIZE (ex: 5 by 5).
	"""

	# TODO : handle resource not found
	index = batchNumber * BATCH_SIZE
	for path in _paths[mediaId][index:index + BATCH_SIZE]:
		if path not in _resources:
			imageFile = open(path, 'rb')
			# We load our images as bytestreams
			_resources[path] = bytes(imageFile.read())
