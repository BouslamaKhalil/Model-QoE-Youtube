from pytube import YouTube 
from pytube.exceptions import RegexMatchError
import yt_dlp
import os
import subprocess
import csv 
#YouTube("https://www.youtube.com/watch?v=wfcPR4qCc34").streams

# 'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height>=480]',

#ffmpeg -ss 00:00:30 -t 00:00:30 -i orig_videos/1.mp4 -vf scale=256:144 -c:v libx264 -crf 35 -preset veryslow -b:v 300k -c:a aac -b:a 64k test17.mp4

"""
id
title
formats
thumbnails
thumbnail
description
channel_id
channel_url
duration
view_count
average_rating
age_limit
webpage_url
categories
tags
playable_in_embed
live_status
release_timestamp
_format_sort_fields
automatic_captions
subtitles
comment_count
chapters
heatmap
like_count
channel
channel_follower_count
channel_is_verified
uploader
uploader_id
uploader_url
upload_date
timestamp
availability
original_url
webpage_url_basename
webpage_url_domain
extractor
extractor_key
playlist
playlist_index
display_id
fulltitle
duration_string
release_year
is_live
was_live
requested_subtitles
_has_drm
epoch
requested_formats
format
format_id
ext
protocol
language
format_note
filesize_approx
tbr
width
height
resolution
fps
dynamic_range
vcodec
vbr
stretched_ratio
aspect_ratio
acodec
abr
asr
audio_channels

"""
def download_v(link, file):

    output_folder = file

    try:
        ydl_opts = {
            'format': 'best' ,  # télécharger la meilleure qualité
            # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height>=480]',
            'outtmpl': os.path.join(output_folder, '%(id)s.%(ext)s')  # nom du fichier de sortie
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try another URL.")


def last_id_v(folder):
    # Vérifie si le dossier existe
    if not os.path.exists(folder):
        print(f"Le dossier {folder} n'existe pas.")
        return 0
    
    # Liste tous les fichiers dans le dossier
    files = os.listdir(folder)
    
    # Filtre uniquement les fichiers qui se terminent par .mp4
    video_files = [f for f in files if f.endswith('.mp4')]
    
    if not video_files:
        return 0  # Si aucun fichier vidéo n'est trouvé, retourne 0
    
    # Extrait les IDs des noms de fichiers
    ids = []
    for file in video_files:
        try:
            id_part = file.split('.')[0]  # Supposons que le format est "id.ext"
            ids.append(int(id_part))     # Convertit en entier
        except ValueError:
            pass  # Ignore les fichiers avec des noms inattendus
    
    # Retourne l'ID maximum ou 0 si aucun ID n'est valide
    return max(ids, default=0)


def last_id_v2(folder):

    files = os.listdir(folder)

    ids = []
    video_files = [f for f in files if f.endswith('.mp4')]
    for file in video_files : 
        try :
       
            id_part = file.split('.')[0]
            ids.append(int(id_part))
        except ValueError:
            pass
    return max(ids, default=0)


def compresse_v(input_f,output_f,video):
    # Commande FFmpeg
    ffmpeg_command = [
        "ffmpeg", "-ss", "00:00:00", "-t", "00:00:30", "-i",
        input_f,
        "-vf", "scale=256:144", "-c:v", "libx264", "-crf", "35", "-preset", "veryslow",
        "-b:v", "300k", "-c:a", "aac", "-b:a", "64k",
        output_f
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Compression terminée. Fichier sauvegardé dans : {output_f}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la compression : {e}")

def size_v(orig_v,compressed_v):
        # Vérifie si les fichiers existent
    if not os.path.exists(orig_v):
        print(f"Le fichier original {orig_v} n'existe pas.")
        return
    if not os.path.exists(compressed_v):
        print(f"Le fichier compressé {compressed_v} n'existe pas.")
        return

    original_size = os.path.getsize(orig_v)
    compressed_size = os.path.getsize(compressed_v)
    print("size ori :",original_size , "size compressed : ", compressed_size )

def create_csv_file(csv_file , field):
    with open(csv_file, 'w', newline='') as file :
        writer = csv.writer(file)
        writer.writerow(field)
def write_on_csv_file(csv_file , field):
    with open(csv_file, 'a', newline='') as file :
        writer = csv.writer(file)
        writer.writerow(field)


if __name__ == '__main__' :
     
    print ("test :) ")


    #folder= "test_2"
    #last_id = last_id_v2(folder)
    #print(f"Le dernier ID trouvé est : {last_id}")
   # download_v("https://www.youtube.com/watch?v=_Td7JjCTfyc",file)
    #print ("-----compresser-----" )
    #compresse_v("orig_videos/1.mp4","test_2/com_1.mp4","1.mp4")
    #size_v("orig_videos/1.mp4","test_2/com_1.mp4")
    field = ["id", "title","categories","view_count", "duration" , "uploader" , "upload_date", "creator" , "format", "resolution" , "height" , "quality","description","comment_count","144","C_144","240","C240","360","C_360","480","C_480","720","C_720","1080","C_1080","subtitles"]
    csv_file = "data_test.csv"
    #if : 
    #   create_csv_file(csv_file , field)
    create_csv_file(csv_file , field)
    #write_on_csv_file(csv_file,["1","tt","animal","rff"] )

    