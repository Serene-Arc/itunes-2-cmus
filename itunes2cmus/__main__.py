#!/usr/bin/env python3
# coding=utf-8

import argparse
import csv
import os
import logging
import pathlib

parser = argparse.ArgumentParser(prog='itunes-2-cmus')
logger = logging.getLogger()


def initParser():
    parser.add_argument('playlist', metavar='P', help='playlist to convert')
    parser.add_argument(
        'mount',
        metavar='M',
        help='mount point of the windows drive')
    parser.add_argument(
        '--mountfolder',
        help='the mount point in the windows directory structure')


if __name__ == '__main__':
    initParser()
    args = parser.parse_args()
    logger.info('Searching file...')
    songLocs = []
    with open(args.playlist, 'r', newline='', encoding='utf-16') as csvfile:
        rd = csv.DictReader(csvfile, delimiter='\t')
        for song in rd:
            songLocs.append(pathlib.PureWindowsPath(song['Location']))

    logger.info('{} songs found'.format(len(songLocs)))
    songLocs = [str(path).strip(path.anchor) for path in songLocs]

    if args.mountfolder:
        songLocs = [
            pathlib.PureWindowsPath(''.join(path.split(args.mountfolder)[1:]))
            for path in songLocs]

    songLocs = [
        pathlib.PurePosixPath(
            pathlib.PurePosixPath(args.mount) / path.relative_to('\\'))
        for path in songLocs]

    logger.info('writing...')
    with open(os.path.basename(args.playlist).split('.')[0] + '.pl', 'w', encoding='utf-8') as file:
        for song in songLocs:
            file.write(song.as_posix() + '\n')

    logger.info('Conversion Complete')
