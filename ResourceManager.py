#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

class ResourceManager:
	"""
	ResourceManager gets the images and loads them in memory whenever they are
	accessed via getFrame.
	"""

	_resources = { }
	_paths = { }

	@staticmethod
	def addResource(mediaId, framePaths):
		"""
		Saves all given paths under the id mediaId WITHOUT loading the files.
		Once a resource is added, it can be retrieved via the getFrame.
		"""
		ResourceManager._paths[mediaId] = framePaths

	@staticmethod
	def getFrame(mediaId, frameId):
		"""
		Returns serialized image frameId of the media mediaId.
		frameId is an integer representing the offset in the frame list.
		"""
		if mediaId not in ResourceManager._resources:
			_loadFrames(mediaId)
		return ResourceManager._resources[mediaId][frameId]

	@staticmethod
	def _loadFrames(mediaId):
		"""
		Loads all frames for the media mediaId (into _resources).
		"""
		imageList = []
		for path in ResourceManager._paths[mediaId]:
			imageList.append(open(path, 'rb+'))
		ResourceManager._resources[mediaId] = imageList