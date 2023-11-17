import matplotlib.pyplot as plt
import mne
import numpy as np
from scipy.io import wavfile
from scipy import signal

def plotBands(bands):
    binNames = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    plt.ylabel("Amplitude")
    plt.bar(binNames, bands, color="#7967e1")
    plt.show()
    plt.clf()

def main():

    # channels = [[] for _ in range(4)]  # Create a list for each channel

    # with open("data/EEG_Umama_Light_Stroop_120s.csv", "r") as data:
    #     next(data)  # Skip the first line
    #     for line in data:
    #         # Format the line
    #         line = line.split(",")         # Convert to a list
    #         for num in range(4):
    #             channels[num].append(float(line[num + 1]))  # Record each channel

    # # Plot the data
    # time = np.arange(0, len(channels[0]), 1)

    # plt.stackplot(time, channels, labels=['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'])

    # plt.xlabel("Sample")
    # plt.ylabel("μV")
    # plt.legend()
    # plt.show()

    channel = []
    with open("data/EEG_Umama_Light_Stroop_120s.csv", "r") as data:
        next(data) 
        for line in data:
            # Format the line
            line = line.split(",")         # Convert to a list
            channel.append(float(line[4])) # Just record the 1st channel

    # Plot the data
    # time = np.arange(0, len(channel), 1)
    time = np.arange(0, 50, 1)

    plt.plot(time, channel[0:50])
    plt.xlabel("Sample")
    plt.ylabel("μV")
    plt.show()
    plt.clf()

    # Make each point repeat twice (effectively ignoring every second point)
    for point in range(len(channel)):
        if(point%2 != 0):
            channel[point] = channel[point-1]

    # Plot the data again
    time = np.arange(0, len(channel), 1)
    # Fourier transform
    fftData = np.fft.fft(channel)
    freq = np.fft.fftfreq(len(channel))*250

    # Remove unnecessary negative reflection
    fftData = fftData[1:int(len(fftData)/2)]
    freq = freq[1:int(len(freq)/2)]

    # Recall FFT is a complex function
    fftData = np.sqrt(fftData.real**2 + fftData.imag**2)

    # Plot for sanity check
    plt.plot(freq, fftData)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()
    plt.clf()

    bandTotals = [0,0,0,0,0]
    bandCounts = [0,0,0,0,0]

    for point in range(len(freq)):
        if(freq[point] < 4):
            bandTotals[0] += fftData[point]
            bandCounts[0] += 1
        elif(freq[point] < 8):
            bandTotals[1] += fftData[point]
            bandCounts[1] += 1
        elif(freq[point] < 12):
            bandTotals[2] += fftData[point]
            bandCounts[2] += 1
        elif(freq[point] < 30):
            bandTotals[3] += fftData[point]
            bandCounts[3] += 1
        elif(freq[point] < 100):
            bandTotals[4] += fftData[point]
            bandCounts[4] += 1

    # Save the average of all points
    bands = list(np.array(bandTotals)/np.array(bandCounts))
    plotBands(bands)

main()