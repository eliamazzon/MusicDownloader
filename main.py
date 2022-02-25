from pytube import YouTube
from pytube import Playlist
from ytmusicapi import YTMusic
from pydub import AudioSegment
import os
import music_tag
import wget
import re

ytmusic = YTMusic()


def mdown(id, url):
    if id == None:
        link = url
    else:
        for i in id:
            link = "https://music.youtube.com/"+i
            try:
                #donwload song in webm
                yt = YouTube(link)
                print(f"\nDonwloading {yt.title}")
                fname = f"{yt.title}"
                fname = fname.replace("/", "\/")
                fname = fname.replace("(", "\(")
                fname = fname.replace(")", "\)")
                fname = fname.replace(" ", "\ ")

                yt.streams.filter(only_audio=True, abr="160kbps").first().download(
                    output_path="/home/aile_/Music/", filename=f"{yt.title}.webm")
                #print("donwloaded")
                #convert song in mp3 and remove webm file
                webm_audio = AudioSegment.from_file(
                    f"/home/aile_/Music/{yt.title}.webm", format="webm")
                webm_audio.export(
                    f"/home/aile_/Music/{yt.title}.mp3", format="mp3")
                os.system(f"rm /home/aile_/Music/{fname}.webm")
                #adding metadata
                try:
                    f = music_tag.load_file(
                        f"/home/aile_/Music/{yt.title}.mp3")
                    f['title'] = f"{yt.title}"
                    f['artist'] = f"{yt.author}"
                    #print("\nadded\n")
                except Exception as e:
                    print("\nfailed to add metadata, error: ", e)

                try:
                    #adding thumbnail
                    img_url = f"{yt.thumbnail_url}"
                    file_name = wget.download(img_url)

                    with open(f'{file_name}', 'rb') as img_in:
                        f['artwork'] = img_in.read()

                    f.save()
                except Exception as e:
                    print("\nfailed to add artwork, error: ", e)

                print("\nDONE\n")
            except Exception as e:
                #print("Error: ", e, "\n")
                try:
                    p = Playlist(link)
                    numb = 1
                    aname = f"{p.title}"
                    aname = aname.replace(" ", "\ ")
                    aname = aname.replace("(", "\(")
                    aname = aname.replace(")", "\)")
                    aname = aname.replace("/", "\/")
                    print(f"Downloading {p.title}\n")

                    for song in p.videos:
                        print(f"Downloading {song.title}")
                        fname = f"{song.title}"
                        fname = fname.replace("/", "\/")
                        fname = fname.replace("(", "\(")
                        fname = fname.replace(")", "\)")
                        fname = fname.replace(" ", "\ ")
                        song.streams.filter(only_audio=True, abr="160kbps").first().download(
                            output_path=f"/home/aile_/Music/{p.title}/webm/", filename=f"{str(numb)} - {song.title}.webm")

                        webm_audio = AudioSegment.from_file(
                            f"/home/aile_/Music/{p.title}/webm/{str(numb)} - {song.title}.webm", format="webm")
                        webm_audio.export(
                            f"/home/aile_/Music/{p.title}/{str(numb)} - {song.title}.mp3", format="mp3")

                        try:
                            print("meta")
                            f = music_tag.load_file(
                                f"/home/aile_/Music/{p.title}/{str(numb)} - {song.title}.mp3")
                            f['title'] = f"{song.title}"
                            f['artist'] = f"{song.author}"
                            f['album'] = f"{p.title}"
                            f['tracknumber'] = f"{numb}"
                            print("\nadded\n")
                        except Exception as e:
                            print("\nfailed to add metadata, error: ", e)

                        try:
                            #adding thumbnail
                            img_url = f"{song.thumbnail_url}"
                            print(img_url)
                            file_name = f"{song.title}_art.jpg"
                            res = requests.get(img_url, stream=True)
                            if res.status_code == 200:
                                with open(file_name, 'wb') as fl:
                                    shutil.copyfileobj(res.raw, fl)
                                print('artwork sucessfully Downloaded: ', file_name)
                            else:
                                print('artwork Couldn\'t be retrieved')

                            with open(f'{file_name}', 'rb') as img_in:
                                f['artwork'] = img_in.read()

                            f.save()
                        except Exception as e:
                            print("\nfailed to add artwork, error: ", e)
                        numb += 1

                    os.system(
                        f"rm -r /home/aile_/Music/{aname}/webm")
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
        f"\nType in the song/album numbers (0 to {n-1}) separated by a space or search again (enter): \n")
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
