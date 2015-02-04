#Will exit if from directory does not exist but will create the to directory
import os
import sys
import errno
import eyed3
import shutil
import mutagen


UNKOWN_CONST = "unknown"

def createCountLogger(total):
	#returns log function printing upto total
	data = [total]
	count = [0]
	def counter():
		d = data[0]
		count[0] += 1
		if count[0] % 20 == 0:
			print "{} of {} complete".format(count[0],d)
	return counter

def valOrUnknown(s):
	if not s:
		return UNKOWN_CONST
	else:
		return s

def make_sure_path_exists(path):
	#from: http://goo.gl/4cjaLB
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

def m4a_info(song,key):
	if key in song.tags:
		return song.tags[key][0]
	else:
		return UNKOWN_CONST

def moveM4A(songPath,endDirector):
	song = mutagen.File(songPath)
	album = m4a_info(song,'\xa9alb').replace("/","")
	title = m4a_info(song,'\xa9nam').replace("/","")
	artist = m4a_info(song,'\xa9ART').replace("/","")
	albumDir = os.path.join(endDirector, artist,album)
	make_sure_path_exists(albumDir)
	newSongPath = os.path.join(albumDir,title) + ".m4a"
	shutil.copy(songPath,newSongPath)


def moveMP3(songPath,endDirector):
	audiofile = eyed3.load(songPath)
	if audiofile.tag:
		album = valOrUnknown(audiofile.tag.album).replace("/","")
		title = valOrUnknown(audiofile.tag.title).replace("/","")
		artist = valOrUnknown(audiofile.tag.artist).replace("/","")
	else:
		album = title = artist = UNKOWN_CONST
	albumDir = os.path.join(endDirector, artist,album)
	make_sure_path_exists(albumDir)
	newSongPath = os.path.join(albumDir,title) + ".mp3"
	shutil.copy(songPath,newSongPath)

def main():
	fromDir = "/Volumes/USER'S IPOD/iPod_Control/Music"
	toDir = '/Users/daniel/Documents/music'

	if len(sys.argv) > 3 or len(sys.argv) == 2:
		sys.exit("Usage: python transfer.py [origin directory] [destination directory]")

	if len(sys.argv) == 3:
		fromDir = sys.argv[1]
		toDir = sys.argv[2]

	if not os.path.isdir(fromDir):
		sys.exit("Must be valid origin directory")

	#TO DIRECTORY IS GUARANTEED TO BE CREATED
	make_sure_path_exists(toDir)


	all_files = {}
	for (dirpath, dirnames, filenames) in os.walk(fromDir):
		for fName in filenames:
			if fName[0] == "/":
					fName = fName[1:]
			file_path = os.path.join(dirpath,fName)
			all_files[file_path] = True

	files = all_files.keys()
	mp3Files = filter(lambda x:x.lower()[-3:] == "mp3",files)
	m4aFiles = filter(lambda x:x.lower()[-3:] == "m4a",files)
	total = len(mp3Files) + len(m4aFiles)
	countLogger = createCountLogger(total )
	count = 0
	for m4a in m4aFiles:
		moveM4A(m4a,toDir)
		countLogger()
	for mp3 in mp3Files:
		moveMP3(mp3,toDir)
		countLogger()

if __name__ == "__main__":
	main()

