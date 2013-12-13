# -*-coding:Utf-8 -*
"""
ResourceManager gets the images and loads them in memory whenever they are
accessed via getFrame.
"""

_resources = { }
_paths = { }
BATCH_SIZE = 5

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
		_loadFramesBatch(mediaId, int(frameId / BATCH_SIZE))
		print("media {} (frames {} to {}) is now in cache."
			.format(mediaId, frameId, frameId + BATCH_SIZE))

	return (_resources[mediaId][frameId], getNextFrameId(mediaId, frameId))

def getNextFrameId(mediaId, frameId):
	"""
	Returns the next available frame id for this media.
	If we reach the last frame available or a non-existing frame, we loop back to the beginning
	"""
	if frameId < len(_paths[mediaId]) - 1:
		return frameId + 1
	else:
		return 0

def _loadFramesBatch(mediaId, batchNumber):
	"""
	Loads all frames for the media mediaId (into _resources),
	BATCH_SIZE by BATCH_SIZE (ex: 5 by 5).
	"""
	if mediaId not in _resources:
			_resources[mediaId] = {}

	# TODO : handle resource not found
	index = batchNumber * BATCH_SIZE
	i = index
	for path in _paths[mediaId][index:index + BATCH_SIZE]:
		imageFile = open(path, 'rb')
		# We load our images as bytestreams
		_resources[mediaId][i] = bytes(imageFile.read())
		i += 1
