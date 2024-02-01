from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.getenv("BASE_DIR")

print(BASE_DIR)
def getInformasiDataset():
    tFile = {
        'betawi' : 0,
        'geblekrenteng' : 0,
        'kawung' : 0,
        'lasem' : 0,
        'megamendung' : 0,
        'pala' : 0,
        'parang' : 0,
        'sekarjagad' : 0,
        'tambal' : 0
    }
    path_betawi = str(BASE_DIR)+'/static/dataset/Batik_Betawi'
    path_geblekrenteng = str(BASE_DIR)+'/static/dataset/Batik_Geblekrenteng'
    path_kawung = str(BASE_DIR)+'/static/dataset/Batik_Kawung'
    path_lasem = str(BASE_DIR)+'/static/dataset/Batik_Lasem'
    path_megamendung = str(BASE_DIR)+'/static/dataset/Batik_Megamendung'
    path_pala = str(BASE_DIR)+'/static/dataset/Batik_Pala'
    path_parang = str(BASE_DIR)+'/static/dataset/Batik_Parang'
    path_sekarjagad = str(BASE_DIR)+'/static/dataset/Batik_Sekarjagad'
    path_tambal = str(BASE_DIR)+'/static/dataset/Batik_Tambal'

    all_file_betawi = os.listdir(path_betawi)
    all_file_geblekrenteng = os.listdir(path_geblekrenteng)
    all_file_kawung = os.listdir(path_kawung)
    all_file_lasem = os.listdir(path_lasem)
    all_file_megamendung = os.listdir(path_megamendung)
    all_file_pala = os.listdir(path_pala)
    all_file_parang = os.listdir(path_parang)
    all_file_sekarjagad = os.listdir(path_sekarjagad)
    all_file_tambal = os.listdir(path_tambal)
    
    fData = []
    ord = 1
     # mapping final data betawi
    for x in all_file_betawi:
        tempData = {
            'filename' : x,
            'class' : 'Batik_Betawi',
            'ord' : ord,
            'filename' : 'dataset/Batik_Betawi/'+x
        }
        fData.append(tempData)
        ord += 1
    # mapping final data geblekrenteng
    for j in all_file_geblekrenteng:
        tempData = {
            'filename' : j,
            'class' : 'Batik_Geblekrenteng',
            'ord' : ord,
            'filename' : 'dataset/Batik_Geblekrenteng/'+j
        }
        fData.append(tempData)
        ord += 1
        # mapping final data kawung
    for k in all_file_kawung:
        tempData = {
            'filename' : k,
            'class' : 'Batik_Kawung',
            'ord' : ord,
            'filename' : 'dataset/Batik_Kawung/'+k
        }
        fData.append(tempData)
        ord += 1
        # mapping final data lasem
    for l in all_file_lasem:
        tempData = {
            'filename' : l,
            'class' : 'Batik_Lasem',
            'ord' : ord,
            'filename' : 'dataset/Batik_Lasem/'+l
        }
        fData.append(tempData)
        ord += 1
        # mapping final data megamendung
    for m in all_file_megamendung:
        tempData = {
            'filename' : m,
            'class' : 'Batik_Megamendung',
            'ord' : ord,
            'filename' : 'dataset/Batik_Megamendung/'+m
        }
        fData.append(tempData)
        ord += 1
        # mapping final data pala
    for n in all_file_pala:
        tempData = {
            'filename' : n,
            'class' : 'Batik_Pala',
            'ord' : ord,
            'filename' : 'dataset/Batik_Pala/'+n
        }
        fData.append(tempData)
        ord += 1
        # mapping final data parang
    for o in all_file_parang:
        tempData = {
            'filename' : o,
            'class' : 'Batik_Parang',
            'ord' : ord,
            'filename' : 'dataset/Batik_Parang/'+o
        }
        fData.append(tempData)
        ord += 1
        # mapping final data sekarjagad
    for p in all_file_sekarjagad:
        tempData = {
            'filename' : p,
            'class' : 'Batik_Sekarjagad',
            'ord' : ord,
            'filename' : 'dataset/Batik_Sekarjagad/'+p
        }
        fData.append(tempData)
        ord += 1
        # mapping final data tambal
    for q in all_file_tambal:
        tempData = {
            'filename' : q,
            'class' : 'Batik_Tambal',
            'ord' : ord,
            'filename' : 'dataset/Batik_Tambal/'+q
        }
        fData.append(tempData)
        ord += 1
    

    tFile['betawi'] = len(all_file_betawi)
    tFile['geblekrenteng'] = len(all_file_geblekrenteng)
    tFile['kawung'] = len(all_file_kawung)
    tFile['lasem'] = len(all_file_lasem)
    tFile['megamendung'] = len(all_file_megamendung)
    tFile['pala'] = len(all_file_pala)
    tFile['parang'] = len(all_file_parang)
    tFile['sekarjagad'] = len(all_file_sekarjagad)
    tFile['tambal'] = len(all_file_tambal)

    dr = {
        'dataKuantitas' : tFile,
        'dataBatik' : fData
    }

    return dr