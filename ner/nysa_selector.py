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

from common.sdb_table import SDBTree

class NysaSelector(QWidget):

    def __init__(self, actions, status):
        super (NysaSelector, self).__init__()
        self.actions = actions
        self.status = status

        platform_scan_button = QPushButton("Scan")
        platform_scan_button.clicked.connect(self.actions.scan_platforms)

        self.platform_list = QListWidget()
        self.platform_list.itemSelectionChanged.connect(self.platform_selection_changed)
        self.platform_list.setSelectionMode(QAbstractItemView.SingleSelection)

        self.sdb_tree = SDBTree(self)

        expand_all_button = QPushButton("Expand All")
        expand_all_button.clicked.connect(self.sdb_tree.expandAll)
        collapse_all_button = QPushButton("Collapse All")
        collapse_all_button.clicked.connect(self.sdb_tree.collapseAll)

        #Main Layout
        layout = QHBoxLayout()

        #Platform Box
        playout = QVBoxLayout()
        playout.addWidget(platform_scan_button)
        playout.addWidget(self.platform_list)

        sdblayout = QVBoxLayout()
        sdb_button_layout = QHBoxLayout()

        sdb_button_layout.addWidget(expand_all_button)
        sdb_button_layout.addWidget(collapse_all_button)

        sdblayout.addLayout(sdb_button_layout)
        sdblayout.addWidget(self.sdb_tree)

        layout.addLayout(playout)
        #layout.addLayout(dlayout)
        layout.addLayout(sdblayout)

        self.setLayout(layout)

    def update_platforms(self, platform_list):
        position = None
        if len(self.platform_list.selectedItems()) > 0:
            position = self.platform_list.selectedIndexes()[0]
            
        self.platform_list.clear() 

        for p in platform_list:
            i = platform_list.index(p)
            self.platform_list.insertItem(i, p)

        item = None
        if position is not None:
            item = self.platform_list.itemFromIndex(position)
            self.platform_list.setItemSelected(item, True)
        else:
            if len(self.platform_list) > 0:
                self.platform_list.setSelection(QRect(0, 0, 1, 1), QItemSelectionModel.Select) 

    def platform_selection_changed(self):
        if len(self.platform_list.selectedItems()) == 0:
            return
        value = str(self.platform_list.selectedItems()[0].text())
        platform_name = value.partition(":")[0]
        board_name = value.partition(":")[2]
        self.actions.platform_selection_changed.emit(platform_name, board_name)

    def setup_sdb_tree(self, som):
        self.sdb_tree.clear()
        self.sdb_tree.set_som(som)
        self.sdb_tree.expandAll()

    def device_selection_changed(self):
        pass

