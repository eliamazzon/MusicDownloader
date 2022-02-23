from pytube import YouTube
from pytube import Playlist

while(True):
    link = input("\nPaste ur link here (or 'q' to exit): ")
    if link.lower().strip() == "q":
        break;
    else:
        pass;
    try:
        yt = YouTube(link);
    except:
        if input("\n is it an album or a playlist? (y/n)") == "y":
            p= Playlist(link)
            chuck = input(f"\n Is this the album/playlist u want to download (y/n): \n {p.title}")
            if chuck.lower().strip()=="y":
                pass;
            else:
                print("ups!")
                continue;
            for song in p.videos:
                print(f"Downloading {song.title}")
                song.streams.filter(only_audio=True,abr="160kbps").first().download(output_path=f"/home/aile_/Documents/CODING/python/mdwn/music/{p.title}",filename=f"{song.title}")
            print("\nDONE\n")

        continue;
    print(f"Donwloading {yt.title}")
    yt.streams.filter(only_audio=True,abr="160kbps").first().download(output_path="/home/aile_/Documents/CODING/python/mdwn/music/",filename=f"{yt.title}")
    print("\nDONE\n")
