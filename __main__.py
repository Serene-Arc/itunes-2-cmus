import csv
import argparse
import os

parser = argparse.ArgumentParser(prog='itunes-2-cmus')

def initParser():
	parser.add_argument('playlist', metavar='P', help='playlist to convert')
	parser.add_argument('mount', metavar='M', help='mount point of the windows drive')

if __name__ == '__main__':
	initParser()
	args = parser.parse_args()
	print('Searching file...')
	songLocs = []
	with open(args.playlist, 'r', newline='', encoding='utf-16') as csvfile:
		rd = csv.DictReader(csvfile, delimiter='\t')
		for song in rd:
			songLocs.append(song['Location'])
	print('{} songs found'.format(len(songLocs)))
	songLocs = [os.path.splitdrive(path)[-1] for path in songLocs]
	songLocs = [path.replace('\\', '/') for path in songLocs]
	songLocs = [args.mount.rstrip('/') + path + '\n' for path in songLocs]
	print('writing...')
	with open(os.path.basename(args.playlist).split('.')[0] + '.pl', 'w', encoding='utf-8') as file:
		for song in songLocs:
			file.write(song)

	print('Conversion ')