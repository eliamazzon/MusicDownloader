#!/bin/python3

from pytube import YouTube
from pytube import Playlist
from ytmusicapi import YTMusic
from pydub import AudioSegment
import os
import music_tag
import wget

ytmusic = YTMusic()
path = "/home/aile_/Music/"


def term_text(txt):  # formatting text to be terminal friendly
    txt = txt.replace(" ", "\ ")
    txt = txt.replace("(", "\(")
    txt = txt.replace(")", "\)")
    txt = txt.replace("'", "\'")
    return txt


def down_song(link):
    yt = YouTube(link)
    print(f"\nDonwloading {yt.title}")
    file_path = f"{path}{yt.title.replace('/','-')}.webm"
    yt.streams.filter(only_audio=True, abr="160kbps").first().download(
        output_path=f"{path}", filename=f"{yt.title.replace('/','-')}.webm")

    mp3_conv(file_path, file_path.replace("webm", "mp3"))
    tags_and_art(file_path.replace("webm", "mp3"),
                 yt.title, None, yt.author, None, yt.thumbnail_url)

    os.system(f"rm -r {term_text(file_path)}")
    print("\nDONE\n")


def down_plist(link):
    p = Playlist(link)
    title = p.title.replace("Album - ", "")
    numb = 1
    print(f"Downloading {title}\n")
    file_path = f"{path}{title}/webm/"

    for song in p.videos:
        print(f"\nDownloading {song.title}")
        song.streams.filter(only_audio=True, abr="160kbps").first().download(
            output_path=f"{path}{title}/webm/", filename=f"{str(numb)} - {song.title.replace('/','-')}.webm")
        mp3_conv(f"{file_path}{str(numb)} - {song.title.replace('/','-')}.webm",
                 f"{path}{title}/{song.title.replace('/','-')}.mp3")
        tags_and_art(f"{path}{title}/{song.title.replace('/','-')}.mp3",
                     song.title, title, song.author, str(numb), song.thumbnail_url)
        numb += 1

    os.system(f"rm -r {term_text(file_path[:-1])}")
    print("\nDONE\n")


def tags_and_art(file_path, song_name, album, author, trk_nmbr, art_link):
    f = music_tag.load_file(file_path)
    f['title'] = song_name
    f['artist'] = author
    if album != None:
        f['album'] = album
    if trk_nmbr != None:
        f['tracknumber'] = trk_nmbr
    file_name = wget.download(art_link)
    with open(f'{file_name}', 'rb') as img_in:
        f['artwork'] = img_in.read()
    f.save()
    os.system(f'rm {term_text(file_name)}')


def mp3_conv(file_path, out_path):
    webm_audio = AudioSegment.from_file(
        f"{file_path}", format="webm")
    webm_audio.export(
        f"{out_path}", format="mp3")


def mdown(id, url):
    if id == None:
        link = url
        try:
            down_song(link)

        except Exception as e:
            try:
                down_plist(link)
            except Exception as err:
                print("down_plist error: ", err)
    else:
        for i in id:
            link = "https://music.youtube.com/"+i
            try:
                down_song(link)

            except Exception as er:
                try:
                    down_plist(link)
                except Exception as e:
                    print("down_plist error: ", e)


while True:
    mode = input("Chose MODE album(a) song(s) url(u) quit(q): ")
    if mode.lower().strip() == "a":
        mode = "albums"
        key = "browseId"
    elif mode.lower().strip() == "s":
        mode = "songs"
        key = "videoId"

    elif mode.lower().strip() == "q":
        break

    elif mode.lower().strip() == "u":
        url = input("\npaste URL here: ")
        id = None
        mdown(id, url)
        continue
    else:
        print("sorry try again")
        continue

    results = ytmusic.search(
        input("\nType the song/album name here: "), filter=f"{mode}")
    print("\nHere's what we found: \n")
    n = 0
    for song in results:
        title = song['title']
        art = song['artists']
        artist = (art[0])['name']
        print(f" {n}: {title} by {artist}")
        n += 1
    sns = input(
        f"\nType in the song/album numbers (0 to {n-1}) separated by a space or search again (enter): ")
    if sns == "":
        continue
    sns = sns.split(" ")
    if mode == "albums":
        id = []
        for s in sns:
            alb_dt = ytmusic.get_album(browseId=f"{(results[int(s)])[key]}")
            id.append("playlist?list=" + alb_dt['audioPlaylistId'])
        url = None
        mdown(id, url)
    else:
        id = []
        for s in sns:
            id.append("watch?v=" + (results[int(s)])[key])
        url = None
        mdown(id, url)
