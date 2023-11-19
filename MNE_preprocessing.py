import numpy as np
import pandas as pd 
import mne
import matplotlib.pyplot as plt

path = "data/EEG_Umama_Light_Stroop_120s.csv"
data = pd.read_csv(path, 
                   skiprows=0, usecols=[*range(1, 5)]) 
ch_names = ['TP9', 'AF7', 'AF8', 'TP10']

sfreq = 256 
info = mne.create_info(ch_names = ch_names, sfreq = sfreq)
raw = mne.io.RawArray(data.T, info)

print(raw.info)
picks = mne.pick_channels(raw.ch_names, include=ch_names)
raw.filter(0.1, 40, picks=picks)

raw.plot()
plt.show()

