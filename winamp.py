###########################################################
# winamp.py
# Python Winamp Controller
#
# Version 1.1 21-Oct-2006  minor bugfix
# Version 1.0, 1-Feb-2001
#
# About:
#  Class to control running instance
#  or Winamp mp3 player on current
#  machine.
#
# Requirements:
#  Winamp and Win32 (of course).
#  ActivePython or Win32 Python extensions.
#  Tested with Winamp 2.71 and ActivePython 2.0
#  on WinNT4.
#
# Usage:
#  Copy this file anywhere in your
#  pythonpath.
#  Create an instance of winamp class
#  and call methods on it to control
#  a running winamp program on current
#  machine.
#
#  Example:
#    >>> import winamp
#    >>> w = winamp.Winamp()
#    >>> w.getPlayingStatus()
#    'stopped'
#    >>> w.play()
#    >>> w.getPlayingStatus()
#    'playing'
#    >>>
#
# Uses the winamp api http://www.winamp.com
# /nsdn/winamp2x/dev/sdk/api.jhtml
# and windows messaging to control winamp.
#
#
# Copyright (c) 2001-2006, Shalabh Chaturvedi
#
# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without
# limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
###########################################################

import wa_ipc as ipc

import argparse
import sys
import win32api
import win32gui

# wonder why win32 imports dont define these
WM_COMMAND = 0x0111
WM_USER = 0x400


class NoWinampOpened(Exception):
    pass


class Winamp:

    COMMANDS = {
        "prev": ipc.WINAMP_BUTTON1,
        "next": ipc.WINAMP_BUTTON5,
        "play": ipc.WINAMP_BUTTON2,
        "pause": ipc.WINAMP_BUTTON3,
        "stop": ipc.WINAMP_BUTTON4,
        "fadeout": ipc.WINAMP_BUTTON4_CTRL,
        "forward": ipc.WINAMP_BUTTON5_SHIFT,
        "rewind": ipc.WINAMP_BUTTON1_SHIFT,
        "raisevol": ipc.WINAMP_VOLUMEUP,
        "lowervol": ipc.WINAMP_VOLUMEDOWN,
    }

    def __init__(self):
        self.hWinamp = win32gui.FindWindow("Winamp v1.x", None)
        if self.hWinamp is 0:
            raise NoWinampOpened()

        iVersionNumber = self.usercommand(0)
        sVersionString = hex(iVersionNumber)
        sVersionString = sVersionString[2:3] + "." + sVersionString[3:]
        self.sVersion = sVersionString

    def command(self, sCommand):
        if sCommand in Winamp.COMMANDS:
            return win32api.SendMessage(
                self.hWinamp, WM_COMMAND, Winamp.COMMANDS[sCommand], 0
            )
        else:
            raise Exception("NoSuchWinampCommand")

    def __getattr__(self, attr):
        self.command(attr)
        return lambda: None

    def usercommand(self, id, data=0):
        return win32api.SendMessage(self.hWinamp, WM_USER, data, id)

    def getVersion(self):
        """Returns the version number of Winamp"""
        return self.sVersion

    def getPlayingStatus(self):
        """Returns the current status string which is one of
        'playing', 'paused' or 'stopped'"""
        iStatus = self.usercommand(ipc.IPC_ISPLAYING)
        if iStatus == 1:
            return "playing"
        elif iStatus == 3:
            return "paused"
        else:
            return "stopped"

    def getTrackStatus(self):
        """Returns a tuple (total_length, current_position) where both are in msecs"""
        # the usercommand returns the number in seconds:
        iTotalLength = self.usercommand(ipc.IPC_GETOUTPUTTIME, 1) * 1000
        iCurrentPos = self.usercommand(ipc.IPC_GETOUTPUTTIME, 0)
        return iTotalLength, iCurrentPos

    def setCurrentTrack(self, iTrackNumber):
        """Changes the track selection to the number specified"""
        return self.usercommand(ipc.IPC_SETPLAYLISTPOS, iTrackNumber)

    def getCurrentTrack(self):
        return self.usercommand(ipc.IPC_GETLISTPOS)

    def getCurrentTrackName(self):
        return win32gui.GetWindowText(self.hWinamp)

    def seekWithinTrack(self, iPositionMsecs):
        """Seeks within currently playing track to specified milliseconds since start"""
        return self.usercommand(ipc.IPC_JUMPTOTIME, iPositionMsecs)

    def setVolume(self, iVolumeLevel):
        """Sets the volume to number specified (range is 0 to 255)"""
        return self.usercommand(ipc.IPC_SETVOLUME, iVolumeLevel)

    def getNumTracks(self):
        """Returns number of tracks in current playlist"""
        return self.usercommand(ipc.IPC_GETLISTLENGTH)

    def getTrackInfo(self):
        """Returns a tuple (samplerate, bitrate, number of channels)"""
        iSampleRate = self.usercommand(ipc.IPC_GETINFO, 0)
        iBitRate = self.usercommand(ipc.IPC_GETINFO, 1)
        iNumChannels = self.usercommand(ipc.IPC_GETINFO, 2)
        return iSampleRate, iBitRate, iNumChannels

    def dumpList(self):
        """Dumps the current playlist into WINAMPDIR/winamp.m3u"""
        return self.usercommand(ipc.IPC_WRITEPLAYLIST)


def getTrackList(sPlaylistFilepath):
    playlist = []
    with open(sPlaylistFilepath, "r") as playlistfile:
        for line in playlistfile.readlines():
            if line.startswith("#"):
                continue
            playlist.append(line.strip())
    return playlist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Winamp control",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("command", nargs="?", default="status", help="Command")
    parser.add_argument("subcommand", nargs="?", help="Sub-command")
    args = parser.parse_args()

    try:
        w = Winamp()
    except NoWinampOpened:
        sys.stderr.write("Winamp not open.\n")
        sys.exit(1)

    if args.command == "status":
        # state = w.getPlayingStatus()
        # print(state)
        print(w.getCurrentTrackName())
        # if state == "playing":

    elif args.command == "vol":
        if args.subcommand == "up":
            # TODO: increase volume by 10%
            w.command("raisevol")
        elif args.subcommand == "down":
            # TODO: decrease volume by 10%
            w.command("lowervol")
        elif args.subcommand:
            print(args.subcommand)
            # scale volume 0-100 to 0-255
            newvol = float(args.subcommand) * 255 / 100
            print(newvol)
            w.setVolume(newvol)

    elif args.command:
        w.command(args.command)

# End of file
