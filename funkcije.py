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


def biraj_bazu() -> FileChooser:
    # biranje foldera
    fc = FileChooser()
    fc.show_only_dirs = True
    display(fc)
    return fc