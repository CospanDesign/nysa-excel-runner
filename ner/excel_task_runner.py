# Copyright (c) 2015 Dave McCoy (dave.mccoy@cospandesign.com)

# This file is part of Nysa (wiki.cospandesign.com/index.php?title=Nysa).
#
# Nysa is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Nysa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nysa; If not, see <http://www.gnu.org/licenses/>.


"""
Excel Task Runner
"""

__author__ = 'dave.mccoy@cospandesign.com (Dave McCoy)'

import os
import sys
import time

from array import array as Array

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *



class ExcelTaskRunnerError(Exception):
    pass

class ExcelTaskRunnerWorker(QObject):
    def __init__(self):
        super (ExcelTaskRunnerWorker, self).__init__()
    
    @pyqtSlot(object, object, object, object, float, object)
    def thread_init(self, engine, driver, mutex, status, delay, actions):
        self.driver = driver
        self.status = status
        self.engine = engine
        self.mutex = mutex
        self.delay = int(delay * 1000)
        self.actions = actions
        self.term_flag = False
        self.init_pos = 0
        self.loop_pos = 0
        self.pause = False
        self.step = False
        self.step_loop = False

        self.status.Verbose("Initializing worker")

class ExcelTaskRunner(QWidget):
    def __init__(self, driver, status, actions):
        super (ExcelTaskRunner, self).__init__()
        self.actions = actions
        self.status = status
        self.driver = driver
        self.delay = 0.010
        self.thread = QThread()
        self.thread.start()
        self.mutex = QMutex()
        self.worker = ExcelTaskRunnerWorker()
        self.worker.moveToThread(self.thread)
        QMetaObject.invokeMethod(self.worker,
                                    "thread_init",
                                    Qt.QueuedConnection,
                                    Q_ARG(object, self),
                                    Q_ARG(object, self.driver),
                                    Q_ARG(object, self.mutex),
                                    Q_ARG(object, self.status),
                                    Q_ARG(float, self.delay),
                                    Q_ARG(object, self.actions))

        run_button = QPushButton("Run")
        reload_button = QPushButton("Reload")
        pause_button = QPushButton("Pause")
        stop_button = QPushButton("Stop")
        reset_button = QPushButton("Reset")
        step_button = QPushButton("Step")
        loop_step_button = QPushButton("Loop Step")
        update_delay_button = QPushButton("Update Dealy (ms)")
        
        self.delay_le = QLineEdit("100")
        self.delay_le.setAlignment(Qt.AlignRight)
        v = QIntValidator()
        v.setBottom(1)

        self.execute_status = QLabel("Idle")

        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Excel Task Runner"))
        layout.addWidget(run_button)
        layout.addWidget(reload_button)
        layout.addWidget(pause_button)
        layout.addWidget(stop_button)
        layout.addWidget(reset_button)
        layout.addWidget(step_button)
        layout.addWidget(loop_step_button)
        layout.addWidget(update_delay_button)
        layout.addWidget(self.delay_le)
        layout.addWidget(self.execute_status)
        self.setLayout(layout)
