#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

#import ResourceManager

"""
This module is in charge of parsing a catalog file. 
It first loads a file which contains the server address, the server port (on which it should serve the catalog) and a list of media descriptor files.
It then goes through the list of descriptor files and parses each file.
"""

ENDL = "\n" # "\r\n"
PATH_TO_CATALOG_FOLDER = "catalog/"

_catalog = []
_catalogAddress = '127.0.0.1'
_catalogPort = 9999

def parse(filename):
	"""
	This function parses a catalog descriptor file.
	It returns the address and port at which clients will be able to request the 

	Sample catalog descriptor file:
		ServerAddress: 127.0.0.1
		ServerPort: 15000
		stream1.txt
		stream3.txt
		stream4.txt
		stream5.txt
		stream6.txt
		stream7.txt
	"""
	global _catalogAddress, _catalogPort

	# TODO : file io errors handling
	with open(filename, 'r') as startupFile:
		startupContent = startupFile.read()
		startupContent = startupContent.split(ENDL)

		# First two lines : server address and port
		_catalogAddress = startupContent[0].split(': ')[1]
		_catalogPort = int(startupContent[1].split(': ')[1])

		# All other lines : path to media descriptor files
		mediaDescriptors = startupContent[2:]
		for mediaDescriptor in mediaDescriptors:
			media = _parseMediaDescriptor(mediaDescriptor)

			# Ask the ResourceManager to take this resource into account
			#ResourceManager.addResource(media.id, media.files)
			# Add this media to the catalog
			_catalog.append(media)

		return (_catalogAddress, _catalogPort)

def _parseMediaDescriptor(filename):
	"""
	This function parses a media descriptor file and returns a dictionary containing all the relevant information.
	Sample media descriptor file:
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
	media = {}

	with open(PATH_TO_CATALOG_FOLDER + filename, 'r') as mediaDescriptorFile:
		mediaDescriptor = mediaDescriptorFile.read()
		mediaDescriptor = mediaDescriptor.split(ENDL)

		# The general properties for this media : id, name, type, address, port, protocol, ips
		for mediaProperty in mediaDescriptor[0:7]:
			mediaProperty = mediaProperty.split(': ')
			media[mediaProperty[0].lower()] = mediaProperty[1]

		# The files list
		media['files'] = []
		for path in mediaDescriptor[7:]:
			media['files'].append(path)

	return media

def getConnectionTypes():
	"""
	Returns a dictionary associating each port to its connection type (written as string), taken directly from the media descriptor.
	Example : 
	{
		'8088': 'TCP_PUSH',
		'12234': 'MCAST_PUSH',
		'11114': 'UDP_PULL',
		'11111': 'MCAST_PUSH',
		'11113': 'TCP_PULL',
		'11112': 'UDP_PUSH'
	}
	"""
	connectionTypes = {}
	# Add one connection type for catalog serving
	connectionTypes[_catalogPort] = 'CATALOG'

	for media in _catalog:
		connectionTypes[int(media['port'])] = media['protocol']
	return connectionTypes

def asHttp():
	"""
	Returns the catalog as an HTTP response.

	Sample HTTP response for the catalog:
	HTTP/1.1 200 OK\r\n
	Server: TP_3IF_DPyStream\r\n
	Connection: Keep-Alive\r\n
	Content-Type: text/txt\r\n
	Content-Length: 100\r\n
	\r\n
	Object ID=1 name=video1 type=BMP address=127.0.0.1 port=8088 protocol=TCP_PUSH ips=1.50\r\n
	Object ID=3 name=video3 type=BMP address=225.100.110.12 port=11111 protocol=MCAST_PUSH ips=0.50\r\n
	\r\n
	"""
	body = bytes(asText(), 'Utf-8')

	html = b'HTTP/1.1 200 OK\r\n'
	html += b'Server: TP_3IF_DPyStream\r\n'
	html += b'Connection: Keep-Alive\r\n'
	html += b'Content-Type: text/txt\r\n'
	html += b'Content-Length: '+ bytes(str(len(body)), 'Utf-8') + b'\r\n'
	html += b'\r\n'
	html += body
	html += b'\r\n'

	return html

def asText():
	"""
	Returns the catalog as plain text, formatted as specified by the client applications.

	Sample plain text catalog:
	ServerAddress: 127.0.0.1\r\n
	ServerPort: 15000\r\n
	Object ID=1 name=video1 type=BMP address=127.0.0.1 port=8088 protocol=TCP_PUSH ips=1.50\r\n
	Object ID=3 name=video3 type=BMP address=225.100.110.12 port=11111 protocol=MCAST_PUSH ips=0.50\r\n
	"""

	text = 'ServerAddress: {0}\r\nServerPort: {1}\r\n'.format(_catalogAddress, _catalogPort)

	for media in _catalog:
		text += 'Object ID={id} name={name} type={type} address={address} port={port} protocol={protocol} ips={ips}\r\n'.format(**media)

	return text