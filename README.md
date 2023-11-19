# Emotion Alert - natHACKS

## Team 44

Welcome to the Emotion Alert project, developed during Nathacks, a hackathon where our team, Team 44, collaborated to create an application that helps users manage stress and anticipate panic attacks using advanced feature extraction algorithms.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [How We Built It](#how-we-built-it)
- [References](#references)
- [natHACKS](#nathacks)

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/emotion-alert.git
cd emotion-alert
```

## Features
- Real-time stress monitoring
- Panic attack anticipation
- Actionable insights and resources

## How We Built It

We started by designing a simple experiment to detect stress levels. Firstly, participants’ basal levels were recorded by exposing them to white noise to serve as a control to compare stress data. Afterwards, participants were introduced to a stress-inducing video, and their EEG data was recorded. The data collected was then put into a feature extraction algorithm, which filtered out background noise and irrelevant spikes in the data. To create a classification mdoel, we used the features to train an SVM model. The classification model is used to detect unusually high levels of stress. The live EEG feed is also displayed on our web app that we built, alongside resources for managing stress and general information on stress and panic attacks. To alert users when their stress levels are unusually high, we also built a wearable stress-induced buzzer (WSIB) using ESP32.

## References 
https://github.com/jordan-bird/eeg-feature-generation

## natHACKS

This project was developed as part of Nathacks, a hackathon where Team 44 collaborated to address the challenges in managing stress and anticipating panic attacks. Nathacks provided a platform for innovative solutions, and we are proud to present Emotion Alert as our contribution.

