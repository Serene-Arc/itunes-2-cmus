# itunes-2-cmus

This is a tool for converting iTunes playlists into a format that can be used by cmus. Cmus playlists are simply the file locations of each of the songs so it's a fairly simple script to extract these from the iTunes playlist file.

## Arguments

There are three different arguments to the script:

- `playlist`
- `mount`
- `--mountfolder`

The `playlist` argument is the file location of the playlist that was exported from iTunes. 

The `mount` argument is the path to the mount point of the drive with the music on it. For me, this was the windows drive that had my old OS.

The `--mountfolder` argument is optional and is for if the drive is not mounted to the root directory. For example, I made a symbolic link between my music folder on Linux and the music drive on the Windows partition. In this case, this argument would be the Windows path up to the symlinked directory.

## Example Command

`python3 itunes-2-cmus ~/example_playlist.xml /media/windows --mountfolder 'Users/Example_User/Music/iTunes'`
