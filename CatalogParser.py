#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

#import ResourceManager

class CatalogParser:
	"""
	This class is in charge of parsing a catalog file. 
	It first loads a file which contains the server address, the server port (on which it should serve the catalog) and a list of media descriptor files.
	It then goes through the list of descriptor files and parses each file.
	"""

	ENDL = "\n" # "\r\n"

	def __init__(self, pathToCatalogFolder = None):
		self._catalog = {}

		self.PATH_TO_CATALOG_FOLDER = "catalog/"
		if pathToCatalogFolder is not None:
			self.PATH_TO_CATALOG_FOLDER = pathToCatalogFolder


	def parse(self, filename):
		"""
		This function parses a catalog descriptor file.
		It returns the address and port at which clients will be able to request the catalog.

		Sample catalog descriptor file :
			ServerAddress: 127.0.0.1
			ServerPort: 15000
			flux1.txt
			flux3.txt
			flux4.txt
			flux5.txt
			flux6.txt
			flux7.txt
		"""
		# TODO : gestion des erreurs d'ouverture (fichier introuvable)
		with open(filename, 'r') as startupFile:
			startupContent = startupFile.read()
			startupContent = startupContent.split(self.ENDL)

			# First two lines : server address and port
			catalogAddress = startupContent[0].split(': ')[1]
			catalogPort = startupContent[1].split(': ')[1]

			# All other lines : path to media descriptor files
			mediaDescriptors = startupContent[2:]
			for mediaDescriptor in mediaDescriptors:
				media = self.parseMediaDescriptor(mediaDescriptor)

				# Ask the ResourceManager to take this resource into account
				#ResourceManager.addResource(media.id, media.files)
				# Add this media to the catalog
				self._catalog.append(media)

			return (catalogAddress, catalogPort)

	def parseMediaDescriptor(self, filename):
		"""
		This function parses a media descriptor file and returns a dictionary containing all the relevant information.
		Sample media descriptor file :
			ID: 1
			Name: video1
			Type: BMP
			Address: 127.0.0.1
			Port: 8088
			Protocol: TCP_PUSH
			IPS: 1.5
			../resources/1/img1.bmp
			../resources/1/img2.bmp
			../resources/1/img3.bmp
			../resources/1/img4.bmp
			../resources/1/img5.bmp
		"""
		print('-- Opening media descriptor', filename)
		media = {}

		# TODO : gestion des erreurs d'ouverture (fichier introuvable)
		with open(self.PATH_TO_CATALOG_FOLDER + filename, 'r') as mediaDescriptorFile:
			mediaDescriptor = mediaDescriptorFile.read()
			mediaDescriptor = mediaDescriptor.split(self.ENDL)

			# The general properties for this media : id, name, type, address, port, protocol, ips
			for mediaProperty in mediaDescriptor[0:6]:
				mediaProperty = mediaProperty.split(': ')
				media[mediaProperty[0].lower()] = mediaProperty[1]

			# The files list
			media['files'] = []
			for path in mediaDescriptor[7:]:
				media['files'].append(path)

		return media
