# Client-side python app for groovevault app, which is calling
# a set of lambda functions in AWS through API Gateway.

# Authors: Gillian Gracey, Jenna Kopp, Annabel Edwards, Varoon Enjeti

#   Northwestern University
#   CS 310, Final Project
import requests
import jsons
import uuid
import pathlib
import logging
import sys
import os
from replit import audio
import base64
import io
from configparser import ConfigParser


class Playlist:

  def __init__(self, row):
    self.playlistid = row[0]
    self.playlistname = row[1]
    self.userid = row[2]


class User:

  def __init__(self, row):
    self.userid = row[0]
    self.username = row[1]


class Song:

  def __init__(self, row):
    self.songid = row[0]
    self.songname = row[1]
    self.artist = row[2]
    self.album = row[3]
    self.originalsongfile = row[4]
    self.songfilekey = row[5]


class Job:

  def __init__(self, row):
    self.jobid = row[0]
    self.userid = row[1]
    self.status = row[2]
    self.originaldatafile = row[3]
    self.datafilekey = row[4]
    self.resultsfilekey = row[5]


#PROMPT
def prompt():
  #my playlists (userid as input): DONE

  #songs by playlist (playlistid as input): DONE

  #songs by artist (artist name as input): DONE

  #albums by artist (artist name as input): DONE

  #songs by album (album name as input): DONE

  #song stats (song id as input): DONE

  #playliststats (get and list all playlists): DONE

  #search song (songid): Annabel TODO

  #download and play song (song id as input): DONE

  #download and play playlist: DONE

  #add song to playlist (song id and playlist id as inputs): DONE

  #add user (creates user): DONE

  #create playlist (playlist name and userid as inputs): DONE

  #upload song to library: DONE

  #get users to library: Annabel working

  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => get user's playlists")
  print("   2 => songs on playlist")
  print("   3 => songs by artist")
  print("   4 => albums by artist")
  print("   5 => songs in album")
  print("   6 => song stats in DB")
  print("   7 => playlist stats in DB")
  print("   8 => download and play playlist")
  print("   9 => download and play song")
  print("   10 => add song to playlist")
  print("   11 => create user")
  print("   12 => create playlist")
  print("   13 => upload song to library")
  print("   14 => get users")

  cmd = input()

  if cmd == "":
    cmd = -1
  elif not cmd.isnumeric():
    cmd = -1
  else:
    cmd = int(cmd)

  return cmd


#############################################################


#FUNCTION ONE
#for a given userid, prints out that user's playlists
def get_user_playlist(baseurl):
  try:
    url = baseurl + "/gv_getuserplists/"
    print("Enter userid>")
    userid = input()
    url = url + userid
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    playlists = []
    for row in body:
      plist = Playlist(row)
      playlists.append(plist)

    #if the user has no playlists
    if len(playlists) == 0:
      print("no playlists listed for that userid")
      return

    for index, p in enumerate(playlists, start=1):
      print(f"Playlist {index}: {p.playlistname}")
    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################
#FUNCTION TWO
#for a given plylistid, prints out that playlist's songs
def get_playlist_songs(baseurl):
  try:
    url = baseurl + "/gv_songsbyplaylist/"
    print("Enter playlistid>")
    playlistid = input()
    url = url + playlistid
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    songs = []
    for row in body:
      song = Song(row)
      songs.append(song)

    #if the playlist has no songs
    if len(songs) == 0:
      print("no songs in this playlist")
      return

    print("Playlist", playlistid, "has the following songs:")
    for index, s in enumerate(songs, start=1):
      print(f"  Song {index}: {s.songname}")
    return

  except Exception as e:
    logging.error("songs() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################


#FUNCTION THREE
#for a given userid, prints out that user's playlists
def get_songs_by_artist(baseurl):
  try:
    url = baseurl + "/gv_songsbyartist/"
    print("Enter artist>")
    userid = input()
    url = url + userid
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    songs = []
    for row in body:
      songs.append(row)

    #if the user has no playlists
    if not songs:
      print("no songs listed for that artist")
      return

    print(userid, "has the following songs:")
    for index, s in enumerate(songs, start=1):
      print(f"  Song {index}: {s[0]}")
    return

    # for s in songs:
    #   print(s[0])
    # return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################

#FUNCTION Four
#for a given artist name --> show albums


def get_album_by_artist(baseurl):
  try:
    url = baseurl + "/gv_albumsbyartist/"
    print("Enter artist>")
    userid = input()
    url = url + userid
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return

    body = res.json()
    albums = []
    for row in body:
      albums.append(row)

    #if the user has no playlists
    if not albums:
      print("no albums listed for that artist")
      return

    print("Artist", userid,
          "has the following albums (# of times it appear in the Database):")
    for index, a in enumerate(albums, start=1):
      print(f"  Album {index}: {a[0]}")

    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################

#FUNCTION FIVE
#for a given album name --> show songs


def songs_by_album(baseurl):
  try:
    url = baseurl + "/gv_songsbyalbum/"
    print("Enter album name>")
    userid = input()
    url = url + userid
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return

    body = res.json()
    songs = []
    for row in body:
      songs.append(row)

    #if the user has no playlists
    if not songs:
      print("no albums listed for that artist")
      return

    print(userid, "has the following songs in the DB:")
    for index, s in enumerate(songs, start=1):
      print(f"  Song {index}: {s[0]}")
    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################


#FUNCTION SIX
#get all songstats
def get_songstats(baseurl):
  try:
    url = baseurl + "/gv_songstats/"
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    songs = []
    for row in body:
      song = Song(row)
      songs.append(song)

    #if the user has no playlists
    if not songs:
      print("no songs in DB yet")
      return

    for s in songs:
      print("Song ID:", s.songid)
      print("  Song Name:", s.songname)
      print("  Artist Name:", s.artist)
      print("  Album Name:", s.album)
      print("  Song File Name:", s.originalsongfile, "\n")
    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################


#FUNCTION SEVEN
#get all playliststt
def get_playliststats(baseurl):
  try:
    url = baseurl + "/gv_playliststats/"
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    playlists = []
    for row in body:
      plist = Playlist(row)
      playlists.append(plist)

    #if the user has no playlists
    if not playlists:
      print("no playlists created yet")
      return

    for p in playlists:
      print("Playlist ID:", p.playlistid)
      print("  Playlist Name:", p.playlistname)
      print("  User ID:", p.userid, "\n")
    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################


#FUNCTION TEN
#for a given playlist id and songid, adds that song to that playlist
def add_song_to_playlist(baseurl):
  try:
    url = baseurl + "/gv_addsongtoplaylist/"
    print("Enter songid of song you want to add>")
    songid = input()
    url = url + songid + "/"
    print("Enter playlistid>")
    playlistid = input()
    url = url + playlistid
    res = requests.post(url)
    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    else:
      body = res.json()
      # print(body)
      print("Song titled: '" + body[0] + "' added to playlist: '" + body[1] +
            "'")
      return
  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################


#FUNCTION ELEVEN
#Create User
def create_user(baseurl):
  try:
    url = baseurl + "/gv_createuser/"
    print("Enter username>")
    username = input()
    url = url + username
    res = requests.post(url)
    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    else:
      print("New user '" + username + "' created")
      return
  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################


#FUNCTION TWELVE
#Create Playlist
def create_playlist(baseurl):
  try:
    url = baseurl + "/gv_createplaylist/"
    print("Enter userid of user creating this playlist>")
    userid = input()
    url = url + userid + "/"
    print("Enter playlist name>")
    playlistname = input()
    url = url + playlistname
    res = requests.post(url)
    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    else:
      print("New playlist called '" + playlistname + "' created for user " +
            str(userid))
      return
  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################


#FUNCTION THIRTEEN
#Upload Song to Library
def upload_song(baseurl):
  """
  Prompts the user for a local filename, song name, album, and artist.
  Then uploads that asset (MP3) to S3 for processing. 

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  print("Enter MP3 filename>")
  local_filename = input()

  if not pathlib.Path(local_filename).is_file():
    print("MP3 file '", local_filename, "' does not exist...")
    return

  print("Enter song's name>")
  songname = input()
  print("Enter the song's artist>")
  artist = input()
  print("Enter song's album>")
  album = input()

  try:
    #
    # build the data packet:
    #
    infile = open(local_filename, "rb")
    bytes = infile.read()
    infile.close()

    #
    # now encode the pdf as base64. Note b64encode returns
    # a bytes object, not a string. So then we have to convert
    # (decode) the bytes -> string, and then we can serialize
    # the string as JSON for upload to server:
    #
    data = base64.b64encode(bytes)
    datastr = data.decode()

    data = {
        "songname": songname,
        "artist": artist,
        "album": album,
        "og_filename": local_filename,
        "data": datastr
    }

    #
    # call the web service:
    #
    api = '/gv_uploadsong'
    url = baseurl + api

    res = requests.post(url, json=data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # success, extract songid:
    #
    body = res.json()

    songid = body

    print("MP3 uploaded, song id =", songid)
    return

  except Exception as e:
    logging.error("upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################


#FUNCTION FOURTEEN
#get all USERS
def get_users(baseurl):
  try:
    url = baseurl + "/get_users/"
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    users = []
    for row in body:
      user = User(row)
      users.append(user)

    #if the user has no playlists
    if not users:
      print("no songs in DB yet")
      return

    for u in users:
      print("User ID:", u.userid)
      print("  Username:", u.username, "\n")
    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#############################################################


def jobs(baseurl):
  """
  Prints out all the jobs in the database

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/jobs'
    url = baseurl + api

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # deserialize and extract jobs:
    #
    body = res.json()
    #
    # let's map each row into an Job object:
    #
    jobs = []
    for row in body:
      job = Job(row)
      jobs.append(job)
    #
    # Now we can think OOP:
    #
    if len(jobs) == 0:
      print("no jobs...")
      return

    for job in jobs:
      print(job.jobid)
      print(" ", job.userid)
      print(" ", job.status)
      print(" ", job.originaldatafile)
      print(" ", job.datafilekey)
      print(" ", job.resultsfilekey)
    #
    return

  except Exception as e:
    logging.error("jobs() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
#
# upload
#
def upload(baseurl):
  """
  Prompts the user for a local filename and user id, 
  and uploads that asset (PDF) to S3 for processing. 

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  print("Enter PDF filename>")
  local_filename = input()

  if not pathlib.Path(local_filename).is_file():
    print("PDF file '", local_filename, "' does not exist...")
    return

  print("Enter user id>")
  userid = input()

  try:
    #
    # build the data packet:
    #
    infile = open(local_filename, "rb")
    bytes = infile.read()
    infile.close()

    #
    # now encode the pdf as base64. Note b64encode returns
    # a bytes object, not a string. So then we have to convert
    # (decode) the bytes -> string, and then we can serialize
    # the string as JSON for upload to server:
    #
    data = base64.b64encode(bytes)
    datastr = data.decode()

    data = {"filename": local_filename, "data": datastr}

    #
    # call the web service:
    #
    api = '/upload'
    url = baseurl + api + "/" + userid

    res = requests.post(url, json=data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # success, extract jobid:
    #
    body = res.json()

    jobid = body

    print("PDF uploaded, job id =", jobid)
    return

  except Exception as e:
    logging.error("upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################


#FUNCTION NINE
#download and play song
def play_song(baseurl, opt_songid):
  """
  Prompts the user for the song id, and downloads
  that song (.mp3).

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """
  if opt_songid is None:
    print("Enter songid>")
    songid = input()
  else:
    songid = str(opt_songid)
  api = '/gv_playsong'
  url = baseurl + api + '/' + songid
  try:

    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    datastr = body[0]
    song = body[1]
    artist = body[2]
    base64_bytes = datastr.encode()
    bytes = base64.b64decode(base64_bytes)
    with open("song_file.mp3", "wb") as binary_file:
      binary_file.write(bytes)
    src = audio.play_file("song_file.mp3")
    print("Playing " + song + " by " + artist)
    if opt_songid is None:
      print("Enter p to pause song. Enter q to return to main menu>")
      inp = input()
      while inp != "q":
        if inp == "p":
          src.set_paused(True)
          print("Enter r to resume song. Enter q to return to main menu>")
          inp = input()
        elif inp == "r":
          src.set_paused(False)
          print("Enter p to pause song. Enter q to return to main menu>")
          inp = input()
      src.set_paused(True)
      return
    else:
      print("Enter p to pause. Enter s to skip song>")
      inp = input()
      while inp != "s":
        if inp == "p":
          src.set_paused(True)
          print("Enter r to resume song. Enter s to skip song>")
          inp = input()
        elif inp == "r":
          src.set_paused(False)
          print("Enter p to pause song. Enter s to skip song>")
          inp = input()
      src.set_paused(True)
      return
    #if we are playing playlist, offer option to skip to next song in playlist

  except Exception as e:
    logging.error("download() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
#FUNCTION EIGHT
#for a given playlistid, prints out that playlist's songs
def get_playlist_ids(baseurl):
  try:
    url = baseurl + "/gv_songsbyplaylist/"
    print("Enter playlistid>")
    playlistid = input()
    url = url + playlistid
    res = requests.get(url)

    if res.status_code != 200:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        body = res.json()
        print("Error message:", body)
      return
    body = res.json()
    songs = []
    for row in body:
      song = Song(row)
      songs.append(song)

    #if the playlist has no songs
    if len(songs) == 0:
      print("no songs in this playlist")
      return []
    ids = []
    for s in songs:
      ids.append([s.songid, s.songname])
    return ids

  except Exception as e:
    logging.error("songs() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return []


#############################################################
############################################################
# main
#
try:
  print('** Welcome to GrooveVault **')
  print()

  # eliminate traceback so we just get error message:
  sys.tracebacklimit = 0

  config_file = 'groovevault-client-config.ini'

  # does config file exist?
  if not pathlib.Path(config_file).is_file():
    print("**ERROR: config file '", config_file, "' does not exist, exiting")
    sys.exit(0)

  # setup base URL to web service:
  configur = ConfigParser()
  configur.read(config_file)
  baseurl = configur.get('client', 'webservice')

  # make sure baseurl does not end with /, if so remove:
  if len(baseurl) < 16:
    print("**ERROR: baseurl '", baseurl, "' is not nearly long enough...")
    sys.exit(0)

  if baseurl == "https://YOUR_GATEWAY_API.amazonaws.com":
    print("**ERROR: update config.ini file with your gateway endpoint")
    sys.exit(0)

  lastchar = baseurl[len(baseurl) - 1]
  if lastchar == "/":
    baseurl = baseurl[:-1]

  cmd = prompt()

  while cmd != 0:
    if cmd == 1:
      get_user_playlist(baseurl)
    elif cmd == 2:
      get_playlist_songs(baseurl)
    elif cmd == 3:
      get_songs_by_artist(baseurl)
    elif cmd == 4:
      get_album_by_artist(baseurl)
    elif cmd == 5:
      songs_by_album(baseurl)
    elif cmd == 6:
      get_songstats(baseurl)
    elif cmd == 7:
      get_playliststats(baseurl)
    elif cmd == 8:
      #call function that returns list of song ids in playlist
      ids = get_playlist_ids(baseurl)
      for song in ids:
        id = song[0]
        name = song[1]
        play_song(baseurl, id)
      print("Playlist finished")
    elif cmd == 9:
      play_song(baseurl, None)
    elif cmd == 10:
      add_song_to_playlist(baseurl)
    elif cmd == 11:
      create_user(baseurl)
    elif cmd == 12:
      create_playlist(baseurl)
    elif cmd == 13:
      upload_song(baseurl)
    elif cmd == 14:
      get_users(baseurl)
    else:
      print("** Unknown command, try again...")

    cmd = prompt()

  # done
  print()
  print('** done **')
  sys.exit(0)

except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)
