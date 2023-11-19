import logging
import csv
import os
import time
import numpy as np
import pandas as pd
import pickle

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations

import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore
import sys

from HashItOut.classification_model.EEG_feature_extraction import generate_feature_vectors_from_samples

FEATURE_MATRIX = None


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self, board_shim, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)

        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_eeg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 25
        self.num_points = self.window_size * self.sampling_rate

        self.win = pg.GraphicsLayoutWidget(title='BrainFlow Plot', size=(800, 600))
        self.setCentralWidget(self.win)
        self.win.setBackground('w')

        self._init_timeseries()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.update_speed_ms)
        self.timer.timeout.connect(self.update)
        self.timer.start()

        self.data_file_path = "/Users/sumaiyasalsabil/Documents/natHACKS/HashItOut/eeg_data.csv"
        self.model_file_path = "/Users/sumaiyasalsabil/Documents/natHACKS/HashItOut/SampleModel.pkl"

        self.data_buffer = []

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i, col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            p.setTitle(f'Main Application Plot - Channel {self.exg_channels[i]}')
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        for count, channel in enumerate(self.exg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 3.0, 45.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 48.0, 52.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 58.0, 62.0, 2,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
            self.curves[count].setData(data[channel].tolist())

            formatted_data.append(str(data[channel][-1]))  # Append the latest data point for each channel

            # Add the formatted data to the buffer
            self.data_buffer.append(formatted_data)
        
        if len(self.data_buffer) >= 100:
            self.save_buffered_data()
            vectors, header = generate_feature_vectors_from_samples(self.data_file_path, 5, 1, 
										  state = None, 
										  remove_redundant = True,
										  cols_to_ignore = -1)
            FEATURE_MATRIX = np.vstack( [ FEATURE_MATRIX, vectors ] )
            print(FEATURE_MATRIX)
            with open(self.model_file_path , "rb") as file:
                classification_model = pickle.load(file)
            predictions = classification_model.predict(FEATURE_MATRIX)
            if 2 in predictions:
                print("STRESSED")
            self.clear_data_file()


    def save_buffered_data(self):
        """Saves the buffered data to a file."""
        with open(self.data_file_path, "a") as file:
            header = ["Timestamp"] + [f"Channel {ch}" for ch in self.exg_channels] + ["Right AUX"]
            file.write(','.join(header) + '\n')
            for data_row in self.data_buffer:
                if not data_row[-1] == '0':
                    data_row.append('0')

                file.write(','.join(data_row) + '\n')
        self.data_buffer = []  # Clear the buffer

    def clear_data_file(self):
        """Clears the content of the data file."""
        os.remove(self.data_file_path)



def main():
    params = BrainFlowInputParams()
    params.serial_port = "/dev/tty.usbmodem206F316C48471"

    # data_file_path = "/Users/sumaiyasalsabil/Documents/natHACKS/HashItOut/eeg_data.csv"  # Specify the desired file path
    # model_file_path = "/Users/sumaiyasalsabil/Documents/natHACKS/HashItOut/SampleModel.pkl"

    board_shim = BoardShim(BoardIds.MUSE_2_BOARD, params)
    try:
        board_shim.prepare_session()
        board_shim.start_stream(450000)
        app = QtWidgets.QApplication(sys.argv)
        w = MainApplication(board_shim)
        w.show()
        sys.exit(app.exec())
    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()

if __name__ == '__main__':
    main()