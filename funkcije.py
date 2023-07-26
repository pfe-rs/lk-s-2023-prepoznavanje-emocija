# importi
from ipyfilechooser import FileChooser
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

import parselmouth
import seaborn as sns
import os

import librosa, librosa.display
import IPython.display as ipd


from statistics import * # videcemo

from os.path import exists
from pathlib import Path


# from shennong.audio import Audio
# from shennong.processor.plp import PlpProcessor

from hurst import compute_Hc, random_walk


## krece klasifikacija
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import mean_squared_error
from math import sqrt

from sklearn.metrics import accuracy_score

import sklearn.metrics as metrics
import sklearn

# from sklearn import svm
##

sns.set() ## fensi plotovi otprilike
#plt.xkcd() ## e ovo su real fancy plotovi vec

pd.set_option("display.max.columns", None)


def biraj_bazu() -> FileChooser:
    # biranje foldera
    fc = FileChooser()
    fc.show_only_dirs = True

    # brza pretraga da nadje default folder, sto da ne
    for dirname,_,_ in os.walk(fc.default_path):
        if Path(dirname).name == "wav":
            fc.default_path = dirname
            fc._select_default = True  ## da ne moramo da selektujemo svaki put, nadajmo se da je wav folder koji nadje zapravo od baze
            fc.reset()
            break
    # ovo valjda odradi posao

    display(fc)
    return fc


def biraj_fajl() -> FileChooser:
    # biranje fajla
    fc = FileChooser()

    display(fc)
    return fc


class primerak():
    def __init__(self, data: np.ndarray, emoci: str, file: str, path: str , sr: int, gr: str, recenica: str):
        self.data = data # niz u kojem je signal, raw
        self.emo = emoci # emocija, ili ce biti nemacko slovo po njihovim obelezjima, mozda napravimo i full translate
        self.filename = file # ajde i filename da znamo odma, i nek bude full path 
        self.path = path # citava putanja
        self.samplerate = sr # ovo je takav waste resursa al dobro, nek bude vise pre nego manje
        self.govornik = gr # kod govornika iz baze
        self.recenica = recenica # kod recenice iz baze
        # self.emocija # srpsko puno ime emocije
        # self.pol # pol govornika
        # self.godiste # godiste govornika


        # ovo je baza specificno na nemce

        # parsovanje emocije
        emo_niz = ['W', 'L', 'E', 'A', 'F', 'T', 'N']
        emo_srb = ["Bes", "Dosada", "Gadjenje", "Strah", "Sreća", "Tuga", "Neutralno"]
        indx = emo_niz.index(self.emo)
        
        self.emocija = emo_srb[indx]
        #

        # godiste i pol, da imamo sve u csv-u sto mozemo
        govornik_niz = ["03", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
        govornik_parse = [["M", "31"], ["F", "34"], ["F", "21"],  ["M", "32"],  ["M", "26"] ,["M", "30"],
                        ["F", "32"], ["F", "35"], ["M", "25"], ["F", "31"] ]
        gindx = govornik_niz.index(self.govornik)
        self.pol = govornik_parse[gindx][0]
        self.godiste = govornik_parse[gindx][1]
    



def ucitaj_bazu(fc): 
    selected = os.fsencode(fc.selected)
    # check if it's a directory or not
    # myb make it work on files too if it's not a dir, and make another function that is a filepicker

    if os.path.isdir(selected):
        # great, iterate over all the shit that looks like a wav file in it
        lista_fajlova = os.listdir(selected)
        lista_fajlova.sort()

        # primerci = np.empty(len(lista_fajlova), dtype = object)
        primerci = []

        # i = 0
        for file in lista_fajlova:
            filename = os.fsdecode(file)
            # full_name = fc.selected + filename
            # necemo nista da proveravamo, idemo try catch i naslepo sve
            try:
                data, samplerate = librosa.load(fc.selected + filename) 
            except:
                print("greska sa citanjem fajla:" + fc.selected + filename)
                continue

            emocija = filename[5]
            govornik = filename[:2]
            recenica = filename[2:5]
            # primerci[i] = primerak(data, emocija, filename, fc.selected + filename, samplerate)
            # i += 1
            primerci.append(primerak(data, emocija, filename, fc.selected + filename, samplerate, govornik, recenica))

        return primerci
    
    if os.path.isfile(filename):
        try:
            data, samplerate = librosa.load(fc.selected + filename) 
        except:
            print("greska sa citanjem fajla:" + fc.selected + filename)
        



# prilepiti 