import yt_dlp
import os
import subprocess
import csv 
import time




#-------- recuperer Link --
def recup_link(file_links , id ) :
    try:
        with open(file_links, 'r', encoding='utf-8') as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number == id:
                    return line.strip()  # Supprime les espaces ou retours à la ligne
            
        return f"La ligne {id} n'existe pas dans le fichier."
    except FileNotFoundError:
        return f"Le fichier '{file_links}' est introuvable."
    except Exception as e:
        return f"Une erreur s'est produite : {e}"
    
#---------------Download ----------------------
def download_v(link, folder, id, resol ):

    output_folder = folder
    format = "bestvideo[height<="+resol+"][ext=mp4]+bestaudio[ext=m4a]/best[height<="+resol+"][ext=mp4]"

    try:
        ydl_opts = {
            'format': format ,  # télécharger la meilleure qualité
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(output_folder, f'{id}_{resol}.%(ext)s')  # nom du fichier de sortie
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(link)
        print(f"Download completed! file saved in {output_folder}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try another URL.")
#----------------Id ---------------
def last_id_v(folder):

    files = os.listdir(folder)

    ids = []
    video_files = [f for f in files if f.endswith('.mp4')]
    for file in video_files : 
        try :
       
            id_part = file.split('_')[0]
            ids.append(int(id_part))
        except ValueError:
            pass
    return max(ids, default=0)

#-----------------Get Data -----------------
def get_video_metadata(link):


    ydl_opts = {
        'quiet': True,  # Empêche l'affichage de logs inutiles

        'extract_flat': False,  # Assurez-vous que la vidéo est extraite correctement
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extraire les informations de la vidéo
        info_dict = ydl.extract_info(link, download=False)

    return info_dict 

def all_para(info_dic):

    for key,value in info_dic.items():
        print (value)

def pertinent_para(info_dic):
    list =["id", "title","description", "duration" ,"view_count","categories","subtitles","comment_count", "uploader" , "upload_date", "format" , "height", "resolution" , "creator" , "quality"]
    list_para =[]
    for key,value in info_dic.items():
        for i in list :
            if key == i : 
                list_para.append([key,value])
    return list_para


#-----------------Compresse --------------------------

def compresse_v(input_f,output_f):
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

"""
def size_v(orig_v,compressed_v):
        # Vérifie si les fichiers existent
    if not os.path.exists(orig_v):
        print(f"Le dossier original {orig_v} n'existe pas.")
        return
    if not os.path.exists(compressed_v):
        print(f"Le dossier compressé {compressed_v} n'existe pas.")
        return

    original_size = os.path.getsize(orig_v)
    compressed_size = os.path.getsize(compressed_v)
    print("size ori :",original_size , "size compressed : ", compressed_size )
    return original_size , compressed_size
"""
#---------recuperer la taille d'un video ----
def recup_size(folder , nom_v):
    if not os.path.exists(folder):
        print(f"Le dossier {folder} n'existe pas.")
        return 
    if os.path.getsize(folder+"/"+nom_v) :
        return os.path.getsize(folder+"/"+nom_v)
    return "NB"
    
#----------------- csv file ------------------

def create_csv_file(csv_file , field):
    with open(csv_file, 'w', newline='') as file :
        writer = csv.writer(file)
        writer.writerow(field)
        
def write_on_csv_file(csv_file , field):
    with open(csv_file, 'a', newline='') as file :
        writer = csv.writer(file)
        writer.writerow(field)

def collector(link, field ,id , orig_v_folder , c_v_folder ):
    info_dic = get_video_metadata(link)
    l_para = pertinent_para(info_dic)
    l_output= []
    # init list output 
    j = 0
    for i in range(len(field)):
        l_output.append("NB")
        if field[i] == "144":
            j = i

    l_output[0] = str(id)
    for i in range(len(field)) :
        for key , value in l_para :
            if field[i] == key :
                l_output[i] = str(value) 
    

    for i in range(j,len(field),3) :
        if i + 2 >= len(field):  # Vérification pour éviter un dépassement d'index
            break
        nom_video_ori = str(id)+'_'+field[i]+".mp4" 
        nom_video_c = "C_"+str(id)+"_"+field[i]+".mp4"

        size_ori = recup_size(orig_v_folder, nom_video_ori)
        size_c = recup_size(c_v_folder, nom_video_c)

        l_output[i] = str(size_ori) if size_ori is not None else "NB"
        l_output[i + 1] = str(size_c) if size_c is not None else "NB"

        # Calculer le ratio si possible
        if size_ori is not None and size_c is not None and size_ori > 0:
            l_output[i + 2] = str((size_ori - size_c) / size_ori)
        else:
            l_output[i + 2] = "NB"
    
 
    return l_output
    





if __name__ == '__main__':
    #netoyage 
    #Discription 
    #ajouter url dans data.csv 

    """
 # --------------Définition des formats
    format_144 = 'bestvideo[height<=144][ext=mp4]+bestaudio[ext=m4a]/best[height<=144][ext=mp4]'
    format_240 = 'bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[height<=240][ext=mp4]'
    format_360 = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]'
    format_480 = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]'
    format_720 = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]'
    format_1080 = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]'

    """    

# ------------------Dossier pour télécharger les videos  
    orig_v_folder = "Orig_videos"
    C_v_folder = "C_videos"
    csv_file  = "data.csv" 
    file_links = "Youtube_Links.txt"

    if not os.path.exists(orig_v_folder):
        os.makefile(orig_v_folder)

    # modififeir la fonction lastid (61081_360.mp4 au lieu de 7_360.mp4)
    id = last_id_v(orig_v_folder) + 1
    #print (id)



    # importer les links depuis la list !!!!!!!!!!!!!!!!!!!!!
    link = recup_link(file_links , id)

    list_resolu = ["144","240","360","480","720","1080"]
    for reso  in list_resolu : 
        download_v(link, orig_v_folder , id , reso)
        input_f = orig_v_folder+"/"+str(id)+"_"+reso+".mp4"
        output_f = C_v_folder+"/"+"C_"+str(id)+"_"+reso+".mp4"
        compresse_v(input_f,output_f)

    """
    download_v(link, orig_v_folder , id , format_240,"240")
    input_f = orig_v_folder+"/"+str(id)+"_"+"240"+".mp4"
    output_f = C_v_folder+"/"+"C_"+str(id)+"_"+"240"+".mp4"
    compresse_v(input_f,output_f)

    download_v(link, orig_v_folder , id , format_360,"360")
    input_f = orig_v_folder+"/"+str(id)+"_"+"360"+".mp4"
    output_f = C_v_folder+"/"+"C_"+str(id)+"_"+"360"+".mp4"
    compresse_v(input_f,output_f)

    download_v(link, orig_v_folder , id , format_480,"480")
    input_f = orig_v_folder+"/"+str(id)+"_"+"480"+".mp4"
    output_f = C_v_folder+"/"+"C_"+str(id)+"_"+"480"+".mp4"
    compresse_v(input_f,output_f)
    download_v(link, orig_v_folder , id , format_720,"720")
    input_f = orig_v_folder+"/"+str(id)+"_"+"720"+".mp4"
    output_f = C_v_folder+"/"+"C_"+str(id)+"_"+"720"+".mp4"
    compresse_v(input_f,output_f)

    download_v(link, orig_v_folder , id , format_1080,"1080")
    input_f = orig_v_folder+"/"+str(id)+"_"+"1080"+".mp4"
    output_f = C_v_folder+"/"+"C_"+str(id)+"_"+"1080"+".mp4"
    compresse_v(input_f,output_f)
    """
    
    field = ["id_v", "id" ,"title", "duration" ,"view_count","categories","subtitles","comment_count", "uploader" , "upload_date", "format" , "height", "resolution" , "creator" , "quality","144","C_144","R_144","240","C_240","R_240","360","C_360","R_360","480","C_480","R_480","720","C_720","R_729","1080","C_1080","R_1080","description"]
    
    #if os.path.isfile(csv_file): 
        #create_csv_file(csv_file , field)


    list_input = collector(link, field, id  , orig_v_folder , C_v_folder)
    time.sleep(1)  

    write_on_csv_file(csv_file, list_input)
    print ("termineeeeeeeeee")
    #for i in range(len(list_input) )  :
    #    print ("key : " , field[i] ,"   value : ", list_input[i])









#----------------les parametres 

    #info_dic = get_video_metadata(link)
    #print ("les para dispo : -------------- ")
    #all_para(info_dic)

    #enregistrer dans une liste !!!!!!!!!!!!
    #print ("video database : --------------")
    #pertinent_para(info_dic)

    """
#------------ compresser video

    # il faut compersser pour tt les resolutions !!!!!!!!!!!
    video = ""
    resol ="360"
    video = str(id)+"_"+resol+".mp4"
    folder_c = "test_2"
    input_f = folder+"/"+video
    output_f = C_v_folder+"/"+"C_"+video
    print ("-----compresser-----" )
    compresse_v(input_f,output_f)
    print ("--------size------")

    # la moyenne des rations de tous les resolutions possible (moyen ration d'un m video avec tt les reso)
    x,y = size_v(input_f,output_f)
    print ("------ration : ------")
    print ((x-y)/x)

   
    

#----------------- csv file ------------------
    field = ["id_v", "id" ,"title","description", "duration" ,"view_count","categories","subtitles","comment_count", "uploader" , "upload_date", "format" , "height", "resolution" , "creator" , "quality","144","C_144","240","C_240","360","C_360","480","C_480","720","C_720","1080","C_1080"]
    
    
    #create_csv_file(csv_file , field)


    list_input = collector(link, field, id  , orig_v_folder , C_v_folder)
    write_on_csv_file(csv_file, list_input)
    for i in range(len(list_input) )  :
        print ("key : " , field[i] ,"   value : ", list_input[i])


    """

    