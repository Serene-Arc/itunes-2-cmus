#!/usr/bin/env python3
# coding=utf-8

import argparse
import csv
import logging
import os
import pathlib
import sys

parser = argparse.ArgumentParser(prog='itunes-2-cmus')
logger = logging.getLogger()


def _init_logging() -> None:
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    stream.setLevel(logging.INFO)


def _init_parser():
    parser.add_argument('playlist', metavar='P', help='playlist to convert')
    parser.add_argument(
        'mount',
        metavar='M',
        help='mount point of the windows drive')
    parser.add_argument(
        '--mountfolder',
        help='the mount point in the windows directory structure')


def read_from_itunes_playlist(
        playlist: pathlib.Path) -> list[pathlib.PurePath]:
    song_locations = []
    with open(playlist, 'r', newline='', encoding='utf-16') as csvfile:
        rd = csv.DictReader(csvfile, delimiter='\t')
        for song in rd:
            song_locations.append(pathlib.PureWindowsPath(song['Location']))
    return song_locations


if __name__ == '__main__':
    _init_logging()
    _init_parser()
    args = parser.parse_args()

    args.playlist = pathlib.Path(args.playlist)
    logger.info('Searching file...')
    songLocs = read_from_itunes_playlist(args.playlist)

    logger.info('{} songs found'.format(len(songLocs)))

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
