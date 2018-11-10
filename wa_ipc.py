# This is an incomplete set of constants derived from wa_ipc.h

WINAMP_OPTIONS_EQ = 40036  # toggles the EQ window
WINAMP_OPTIONS_PLEDIT = 40040  # toggles the playlist window
WINAMP_VOLUMEUP = 40058  # turns the volume up a little
WINAMP_VOLUMEDOWN = 40059  # turns the volume down a little
WINAMP_FFWD5S = 40060  # fast forwards 5 seconds
WINAMP_REW5S = 40061  # rewinds 5 seconds

# the following are the five main control buttons, with optionally shift
# or control pressed
# (for the exact functions of each, just try it out)
WINAMP_BUTTON1 = 40044
WINAMP_BUTTON2 = 40045
WINAMP_BUTTON3 = 40046
WINAMP_BUTTON4 = 40047
WINAMP_BUTTON5 = 40048
WINAMP_BUTTON1_SHIFT = 40144
WINAMP_BUTTON2_SHIFT = 40145
WINAMP_BUTTON3_SHIFT = 40146
WINAMP_BUTTON4_SHIFT = 40147
WINAMP_BUTTON5_SHIFT = 40148
WINAMP_BUTTON1_CTRL = 40154
WINAMP_BUTTON2_CTRL = 40155
WINAMP_BUTTON3_CTRL = 40156
WINAMP_BUTTON4_CTRL = 40157
WINAMP_BUTTON5_CTRL = 40158

IPC_ISPLAYING = 104
# int res = SendMessage(hwnd_winamp,WM_WA_IPC,0,IPC_ISPLAYING);
# This is sent to retrieve the current playback state of Winamp.
# If it returns 1, Winamp is playing.
# If it returns 3, Winamp is paused.
# If it returns 0, Winamp is not playing.

IPC_GETOUTPUTTIME = 105
# int res = SendMessage(hwnd_winamp,WM_WA_IPC,mode,IPC_GETOUTPUTTIME);
# This api can return two different sets of information about current playback status.
#
# If mode = 0 then it will return the position (in ms) of the currently playing track.
# Will return -1 if Winamp is not playing.
#
# If mode = 1 then it will return the current track length (in seconds).
# Will return -1 if there are no tracks (or possibly if Winamp cannot get the length).
#
# If mode = 2 then it will return the current track length (in milliseconds).
# Will return -1 if there are no tracks (or possibly if Winamp cannot get the length).

IPC_JUMPTOTIME = 106
# (requires Winamp 1.60+)
# SendMessage(hwnd_winamp,WM_WA_IPC,ms,IPC_JUMPTOTIME);
# This api sets the current position (in milliseconds) for the currently playing song.
# The resulting playback position may only be an approximate time since some playback
# formats do not provide exact seeking e.g. mp3
# This returns -1 if Winamp is not playing, 1 on end of file, or 0 if it was successful.

IPC_GETMODULENAME = 109
IPC_EX_ISRIGHTEXE = 666
# usually shouldnt bother using these, but here goes:
# send a WM_COPYDATA with IPC_GETMODULENAME, and an internal
# flag gets set, which if you send a normal WM_WA_IPC message with
# IPC_EX_ISRIGHTEXE, it returns whether or not that filename
# matches. lame, I know.

IPC_WRITEPLAYLIST = 120
# (requires Winamp 1.666+)
# int cur = SendMessage(hwnd_winamp,WM_WA_IPC,0,IPC_WRITEPLAYLIST);
#
# IPC_WRITEPLAYLIST will write the current playlist to winamp.m3u and on unicode clients
# it will also write the current playlist to winamp.m3u8. This will also return the
# current playlist position (see IPC_GETLISTPOS).
#
# Where the playlist(s) are saved to depends on the Winamp client version used though it
# is simple to find the path using the correct location (when working in-process):
#
# Pre 2.90 -> '<winampdir>\\Winamp.m3u'
# From 2.90 to 5.1 -> Use IPC_GETINIDIRECTORY
# From 5.11 -> Use IPC_GETM3UDIRECTORY
#
# If working from an external program then it is possible to work out the location of the
# playlist by reading relevant values out of paths.ini (if found) otherwise the pre 2.90
# behaviour is what will be attempted to be used (as Winamp does if there is any failure).
#
# This is kinda obsoleted by some of the newer 2.x api items but it still is good for
# use with a front-end program (instead of a plug-in) and you want to see what is in the
# current playlist.
#
# This api will only save out extended file information in the #EXTINF entry if Winamp
# has already read the data such as if the file was played of scrolled into view. If
# Winamp has not read the data then you will only find the file with its filepath entry
# (as is the base requirements for a m3u playlist).

IPC_SETPLAYLISTPOS = 121
# (requires Winamp 2.0+)
# SendMessage(hwnd_winamp,WM_WA_IPC,position,IPC_SETPLAYLISTPOS)
# IPC_SETPLAYLISTPOS sets the playlist position to the specified 'position'.
# It will not change playback status or anything else. It will just set the current
# position in the playlist and will update the playlist view if necessary.
#
# If you use SendMessage(hwnd_winamp,WM_COMMAND,MAKEWPARAM(WINAMP_BUTTON2,0),0);
# after using IPC_SETPLAYLISTPOS then Winamp will start playing the file at 'position'.

IPC_SETVOLUME = 122
# (requires Winamp 2.0+)
# SendMessage(hwnd_winamp,WM_WA_IPC,volume,IPC_SETVOLUME);
# IPC_SETVOLUME sets the volume of Winamp (between the range of 0 to 255).
#
# If you pass 'volume' as -666 then the message will return the current volume.
# int curvol = SendMessage(hwnd_winamp,WM_WA_IPC,-666,IPC_SETVOLUME);

# IPC_GETVOLUME(hwnd_winamp) SendMessage(hwnd_winamp,WM_WA_IPC,(WPARAM)-666,IPC_SETVOLUME)
# (requires Winamp 2.0+)
# int curvol = IPC_GETVOLUME(hwnd_winamp);
# This will return the current volume of Winamp (between the range of 0 to 255).

IPC_SETPANNING = 123
IPC_SETBALANCE = 123
# (requires Winamp 2.0+)
# SendMessage(hwnd_winamp,WM_WA_IPC,panning,IPC_SETPANNING);
# IPC_SETPANNING sets the panning of Winamp from 0 (left) to 255 (right).
#
# At least in 5.x+ this works from -127 (left) to 127 (right).
#
# If you pass 'panning' as -666 to this api then it will return the current panning.
# int curpan = SendMessage(hwnd_winamp,WM_WA_IPC,-666,IPC_SETPANNING);
#
# IPC_GETPANNING(hwnd_winamp) SendMessage(hwnd_winamp,WM_WA_IPC,-666,IPC_SETPANNING)
# IPC_GETBALANCE(hwnd_winamp) SendMessage(hwnd_winamp,WM_WA_IPC,-666,IPC_SETBALANCE)
# (requires Winamp 2.0+)
# int curpan = IPC_GETPANNING(hwnd_winamp);
# This will return the current panning level of Winamp (5.x) from -127 (left) to 127 (right)
# or from 0 (left) to 255 (right) on older client versions.

IPC_GETLISTLENGTH = 124
# (requires Winamp 2.0+)
# int length = SendMessage(hwnd_winamp,WM_WA_IPC,0,IPC_GETLISTLENGTH);
# IPC_GETLISTLENGTH returns the length of the current playlist as the number of tracks.


IPC_GETLISTPOS = 125
# (requires Winamp 2.05+)
# int pos=SendMessage(hwnd_winamp,WM_WA_IPC,0,IPC_GETLISTPOS);
# IPC_GETLISTPOS returns the current playlist position (which is shown in the playlist
# editor as a differently coloured text entry e.g is yellow for the classic skin).
#
# This api is a lot like IPC_WRITEPLAYLIST but a lot faster since it does not have to
# write out the whole of the current playlist first.

IPC_GETNEXTLISTPOS = 136
# (requires Winamp 5.61+)
# int pos=SendMessage(hwnd_winamp,WM_WA_IPC,0,IPC_GETNEXTLISTPOS);
# IPC_GETNEXTLISTPOS returns the next playlist position expected to be played from the
# current playlist and allows for determining the next playlist item to be played even
# if shuffle mode (see IPC_GET_SHUFFLE) is enabled at the time of using this api.
#
# If there is no known next playlist item then this will return -1 i.e. if there's only
# one playlist item or at the end of the current playlist and repeat is disabled.
#
# Notes: If a plug-in (like the JTFE plug-in) uses IPC_GET_NEXT_PLITEM to override the
#        playlist order then you will need to query the plug-in directly (via api_queue
#        for the JTFE plug-in) to get the correct next playlist item to be played.
#
#        If a change is made to the internal shuffle table, the value returned by prior
#        use of this api is likely to be different and so will need to be re-queried.
#
#        The returned playlist item position is zero-based.

IPC_GETINFO = 126
# (requires Winamp 2.05+)
# int inf=SendMessage(hwnd_winamp,WM_WA_IPC,mode,IPC_GETINFO);
# IPC_GETINFO returns info about the current playing song. The value
# it returns depends on the value of 'mode'.
# Mode      Meaning
# ------------------
# 0         Samplerate, in kilohertz (i.e. 44)
# 1         Bitrate  (i.e. 128)
# 2         Channels (i.e. 2)
# 3 (5+)    Video LOWORD=w HIWORD=h
# 4 (5+)    > 65536, string (video description)
# 5 (5.25+) Samplerate, in hertz (i.e. 44100)
