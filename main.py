#!/bin/python3

import os

import music_tag
import wget
from pydub import AudioSegment
from pytube import Playlist, YouTube
from ytmusicapi import YTMusic

yt_music = YTMusic()


def mdown(id, url):
    if id is None:
        link = url
    else:
        for i in id:
            link = "https://music.youtube.com/" + i
            try:
                # download song in webm
                yt = YouTube(link)
                print(f"\nDownloading {yt.title}")
                file_name = f"{yt.title}"
                file_name = file_name.replace("/", "-")
                file_name = file_name.replace("(", "\(")
                file_name = file_name.replace(")", "\)")
                file_name = file_name.replace(" ", "\ ")
                file_name = file_name.replace("'", "'")

                yt.streams.filter(only_audio=True, abr="160kbps").first().download(
                    output_path="/home/aile_/Music/",
                    filename=f"{yt.title.replace('/','-')}.webm",
                )
                # convert song in mp3 and remove webm file
                webm_audio = AudioSegment.from_file(
                    f"/home/aile_/Music/{yt.title.replace('/','-')}.webm", format="webm"
                )
                webm_audio.export(
                    f"/home/aile_/Music/{yt.title.replace('/','-')}.mp3", format="mp3"
                )
                os.system(f"rm /home/aile_/Music/{file_name}.webm")
                # adding metadata
                try:
                    f = music_tag.load_file(
                        f"/home/aile_/Music/{yt.title.replace('/','-')}.mp3"
                    )
                    f["title"] = f"{yt.title}"
                    f["artist"] = f"{yt.author}"

                except Exception as e:
                    print("\nfailed to add metadata, error: ", e)

                try:
                    # adding thumbnail
                    img_url = f"{yt.thumbnail_url}"
                    file_name = wget.download(img_url)

                    with open(f"{file_name}", "rb") as img_in:
                        f["artwork"] = img_in.read()

                    f.save()

                    file_name = file_name.replace("/", "\/")
                    file_name = file_name.replace("(", "\(")
                    file_name = file_name.replace(")", "\)")
                    file_name = file_name.replace(" ", "\ ")
                    file_name = file_name.replace("'", "'")

                    os.system(f"rm {file_name}")
                except Exception as e:
                    print("\nfailed to add artwork, error: ", e)

                print("\nDONE\n")

            except Exception as e:
                try:
                    p = Playlist(link)
                    numb = 1
                    album_name = f"{p.title}"
                    album_name = album_name.replace(" ", "\ ")
                    album_name = album_name.replace("(", "\(")
                    album_name = album_name.replace(")", "\)")
                    album_name = album_name.replace("/", "\/")
                    album_name = album_name.replace("'", "'")

                    print(f"Downloading {p.title}\n")

                    for song in p.videos:
                        print(f"\nDownloading {song.title}")
                        file_name = f"{song.title}"
                        file_name = file_name.replace("/", "\/")
                        file_name = file_name.replace("(", "\(")
                        file_name = file_name.replace(")", "\)")
                        file_name = file_name.replace(" ", "\ ")
                        file_name = file_name.replace("'", "'")

                        song.streams.filter(
                            only_audio=True, abr="160kbps"
                        ).first().download(
                            output_path=f"/home/aile_/Music/{p.title}/webm/",
                            filename=f"{str(numb)} - {song.title.replace('/','-')}.webm",
                        )

                        webm_audio = AudioSegment.from_file(
                            f"/home/aile_/Music/{p.title}/webm/{str(numb)} - {song.title.replace('/','-')}.webm",
                            format="webm",
                        )
                        webm_audio.export(
                            f"/home/aile_/Music/{p.title}/{str(numb)} - {song.title.replace('/','-')}.mp3",
                            format="mp3",
                        )

                        try:
                            f = music_tag.load_file(
                                f"/home/aile_/Music/{p.title}/{str(numb)} - {song.title.replace('/','-')}.mp3"
                            )
                            f["title"] = f"{song.title}"
                            f["artist"] = f"{song.author}"
                            f["album"] = f"{p.title}"
                            f["tracknumber"] = f"{numb}"
                        except Exception as e:
                            print("\nfailed to add metadata, error: ", e)

                        try:
                            # adding thumbnail
                            img_url = f"{song.thumbnail_url}"
                            file_name = wget.download(img_url)

                            with open(f"{file_name}", "rb") as img_in:
                                f["artwork"] = img_in.read()

                            with open(f"{file_name}", "rb") as img_in:
                                f["artwork"] = img_in.read()

                            f.save()

                            file_name = file_name.replace("/", "\/")
                            file_name = file_name.replace("(", "\(")
                            file_name = file_name.replace(")", "\)")
                            file_name = file_name.replace(" ", "\ ")
                            file_name = file_name.replace("'", "'")

                            os.system(f"rm {file_name}")
                        except Exception as e:
                            print("\nfailed to add artwork, error: ", e)
                        numb += 1

                    os.system(f"rm -r /home/aile_/Music/{album_name}/webm")
                    print("\nDONE\n")
                except Exception as e:
                    print(f"\nSomething went wrong: {e}\n")


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

    results = yt_music.search(
        input("\nType the song/album name here: "), filter=f"{mode}"
    )
    print("\nHere's what we found: \n")
    n = 0
    for song in results:
        title = song["title"]
        art = song["artists"]
        artist = (art[0])["name"]
        print(f" {n}: {title} by {artist}")
        n += 1
    sns = input(
        f"\nType in the song/album numbers (0 to {n-1}) separated by a space or search again (enter): "
    )
    if sns == "":
        continue
    sns = sns.split(" ")
    if mode == "albums":
        id = []
        for s in sns:
            alb_dt = yt_music.get_album(browseId=f"{(results[int(s)])[key]}")
            id.append("playlist?list=" + alb_dt["audioPlaylistId"])
        url = None
        mdown(id, url)
    else:
        id = []
        for s in sns:
            id.append("watch?v=" + (results[int(s)])[key])
        url = None
        mdown(id, url)
