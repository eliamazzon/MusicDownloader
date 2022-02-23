from pytube import YouTube
from pytube import Playlist
from ytmusicapi import YTMusic

ytmusic = YTMusic()

def mdown(id,url):
    if id == None:
        link = url
    else:
        link = "https://music.youtube.com/"+id
    print(link)
    try:
        yt = YouTube(link);
        print(f"Donwloading {yt.title}")
        yt.streams.filter(only_audio=True,abr="160kbps").first().download(output_path="/home/aile_/Documents/CODING/python/mdwn/music/",filename=f"{yt.title}")
        print("\nDONE\n")
    except:
        try:
            p= Playlist(link)
            for song in p.videos:
                print(f"Downloading {song.title}")
                song.streams.filter(only_audio=True,abr="160kbps").first().download(output_path=f"/home/aile_/Music/{p.title}",filename=f"{song.title}")
            print("\nDONE\n")
        except:
            print("\nAn error occurred, try again...\n")




while True:
    mode = input("Chose MODE album(a) song(s) url(u): ")
    if mode.lower().strip() == "a":
        mode = "albums"
        key = "browseId"
    elif mode.lower().strip() == "s":
        mode = "songs"
        key = "videoId"

    elif mode.lower().strip() == "u":
        url = input("\npaste URL here: ")
        id = None
        mdown(id,url)
        continue
    else:
        print("sorry try again")
        continue

    results = ytmusic.search(input("\nType the song/album name here: "),filter=f"{mode}")
    print("\nHere's what we found: \n")
    n=0
    for song in results:
        title = song['title']
        art = song['artists']
        artist = (art[0])['name']
        print(f" {n}: {title} by {artist}")
        n+=1
    sn=input(f"\nType in the song/album number (0 to {n-1}): \n")
    if mode == "albums":
        alb_dt = ytmusic.get_album(browseId=f"{(results[int(sn)])[key]}")
        id = "playlist?list=" + alb_dt['audioPlaylistId']
    else:
        id = "watch?v=" + (results[int(sn)])[key]
    mdown(id)
