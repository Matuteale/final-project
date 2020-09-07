# Blink Detection Prototype
A python implementation to interpret neural activity asociated to blinks using Neurosky Mobile headset device. 
After setup, the implementation will analyse and and classify brain activity live as winks or not.

## Introduction
This implementation uses a Neurosky Mobile v2 headset to read brain activity on the wearer and forward the signal through a bluetooth serial connection.
Such signals are then parsed and used by python scripts for the different steps required. Such steps will create a mathematical model that will lastly be used for the live classification of winks.

### Neurosky Mobile v2
A [Neurosky headset](http://download.neurosky.com/support_page_files/MindWaveMobile/docs/mindwave_mobile_user_guide.pdf) was used for the implementation. This headset runs o a simple double A battery to power a [dry electrode](https://en.wikipedia.org/wiki/Electroencephalography#Dry_EEG_electrodes) that must be in contact with the wearers forehead and a clip that goes to the ear lobe. Both points of contact on the user allow for a reading on brain activity based on [EEG](https://en.wikipedia.org/wiki/Electroencephalography) analysis. 

### CLI requirements
*TODO list cli requirements*

## Steps to create model
In order to be able to classify blinks based on brain activity, a classification model must be generated based on previous blink data analysis.
### Sampling 
The first step for creating the model is by running the [phase_1_raw_data_collector.py](https://github.com/Matuteale/final-project/blob/master/phase_1_raw_data_collector.py "phase_1_raw_data_collector.py") script to generate a video of the user using the default camera and log file with the raw data collected by the Neurosky headset. 
This script will start recording and collecting data only after headset auto calibration is successful. Afterwards it will close the files. 
(Read file for required parameters)
### Ground Truth Generation
In this second step, the script [phase_2_training_data_creation.py]([https://github.com/Matuteale/final-project/blob/master/phase_2_training_data_creation.py](https://meet.google.com/linkredirect?authuser=1&dest=https%3A%2F%2Fgithub.com%2FMatuteale%2Ffinal-project%2Fblob%2Fmaster%2Fphase_2_training_data_creation.py) "phase_2_training_data_creation.py") must be executed. The video will start playing and keyboard key 'B' should be pressed on each blink encounter. The previous input will save a "mark" on the final training file indicating that a group of processed brain activity activity readings correspond to a real blink.
### Model Generation
The [phase_3_training.py](https://github.com/Matuteale/final-project/blob/master/phase_3_training.py "phase_3_training.py") script will generate a mathematical model that should be able to classify brain activity.
The script receives as input the `Ground Truth` file generated on the previous section. 
The model is saved to disk so that regeneration is not required.
## Realtime Prediction
Using a previously generated logistic regression model as input,  its possible to parse realtime brain activity read by the Neurosky headset and classify it as wink or not wink. 
Classification is done with [phase_4_blink_detection.py](https://github.com/Matuteale/final-project/blob/master/phase_4_blink_detection.py "phase_4_blink_detection.py") by having a moving window of data that gets classified based on the model.
## Quick Start

*TODO step by step guide*

### Model Usage
Previously generated models are available on the repository for a quick start.
*TODO model usage*
