from django.shortcuts import render
import random
import numpy as np
from . import models
from . import forms
import time

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def feed(request):
    initialize()
    button = models.StartButton.objects.first()
    feed_active = False
    loading = False

    if request.method == 'POST':
        # Process the button click
        clicked = request.POST.get('clicked')
        print(request.POST)
        if clicked:
            loading = True
            time.sleep(5)
            get_window()
            button.clicked = True
            feed_active = True
            loading = False  # Reset loading to false once the feed is ready

    # Render the template with the object and form
    return render(request, 'feed.html', {
        'form': forms.StartButtonForm(), 
        "feed_active" : feed_active, 
        "loading" : loading
    })

def initialize():
    
    if models.StartButton.objects.exists():
        models.StartButton.objects.all().delete()

    models.StartButton.objects.create()

import logging

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations

import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore
import sys

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self, board_shim, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)

        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_eeg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 50
        self.num_points = self.window_size * self.sampling_rate

        self.win = pg.GraphicsLayoutWidget(title='BrainFlow Plot', size=(800, 600))
        self.setCentralWidget(self.win)
        self.win.setBackground('w')

        self._init_timeseries()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.update_speed_ms)
        self.timer.timeout.connect(self.update)
        self.timer.start()

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


def get_window():
    params = BrainFlowInputParams()
    params.serial_port = "/dev/ttyACMO"

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