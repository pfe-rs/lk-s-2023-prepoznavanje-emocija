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


#from shennong.audio import Audio
#from shennong.processor.plp import PlpProcessor

from hurst import compute_Hc, random_walk

def biraj_bazu() -> FileChooser:
    # biranje foldera
    fc = FileChooser()
    fc.show_only_dirs = True

    # brza pretraga da nadje default folder, sto da ne
    for dirname,_,_ in os.walk(fc.default_path):
        if Path(dirname).name == "wav":
            fc.default_path = dirname
            break
    # ovo valjda odradi posao

    display(fc)
    return fc


class primerak():
    def __init__(self, data: np.ndarray, emocija: str, file: str, path: str , sr: int):
        self.data = data # niz u kojem je signal, raw
        self.emo = emocija # emocija, ili ce biti nemacko slovo po njihovim obelezjima, mozda napravimo i full translate
        self.filename = file # ajde i filename da znamo odma, i nek bude full path 
        self.path = path # citava putanja
        self.samplerate = sr # ovo je takav waste resursa al dobro, nek bude vise pre nego manje

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
            # primerci[i] = primerak(data, emocija, filename, fc.selected + filename, samplerate)
            # i += 1
            primerci.append(primerak(data, emocija, filename, fc.selected + filename, samplerate))

        return primerci
    
    if os.path.isfile(filename):
        try:
            data, samplerate = librosa.load(fc.selected + filename) 
        except:
            print("greska sa citanjem fajla:" + fc.selected + filename)
        
