# Copyright (c) 2014 Dave McCoy (dave.mccoy@cospandesign.com)

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


""" nysa interface
"""

__author__ = 'dave.mccoy@cospandesign.com (Dave McCoy)'

import sys
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class FileInterface(QWidget):

    def __init__(self, actions, status):
        super (FileInterface, self).__init__()
        self.actions = actions
        self.status = status

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.actions.save_file)
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.actions.load_file)
        create_empty_button = QPushButton("Create Empty Excel Project")
        create_empty_button.clicked.connect(self.actions.create_empty_excel)
        create_example_button = QPushButton ("Create Example Excel Project")
        create_example_button.clicked.connect(self.actions.create_example_excel)

        path = os.path.join(os.path.expanduser("~"), "sandbox", "file_test.xls")
        self.filepath = QLineEdit(path)

        layout = QVBoxLayout()
        clayout = QHBoxLayout()
        clayout.addWidget(create_empty_button)
        clayout.addWidget(create_example_button)
        flayout = QHBoxLayout()
        #flayout.addWidget(save_button)
        flayout.addWidget(self.filepath)
        flayout.addWidget(load_button)

        layout.addLayout(clayout)
        layout.addLayout(flayout)

        self.setLayout(layout)


    def get_save_filepath(self):
        if not os.path.exists(self.filepath.text()):
            path = QFileDialog.getSaveFileName( parent = None,
                                                caption = "Select a location for an excel file")
            if path is not None:
                self.filepath.setText(path)

        return self.filepath.text()
             

    def get_open_filepath(self):
        if not os.path.exists(self.filepath.text()):
            path = QFileDialog.getOpenFileName( parent = None,
                                                caption = "Open an Excel File")
            if path is not None:
                self.filepath.setText(path)
        return self.filepath.text()

