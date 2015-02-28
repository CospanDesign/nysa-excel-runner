#! /usr/bin/python

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

from nysa.common.status import Status
from nysa.host.platform_scanner import PlatformScanner

import xlwt

from nysa_selector import NysaSelector
from file_interface import FileInterface
from common.register_view import RegisterView
from excel.excel_engine import ExcelEngine
from excel.utils import create_excel_workbook

from driver.excel_driver import ExcelDriver


class Actions(QObject):
    scan_platforms = pyqtSignal(name = "platform_scan")
    platform_selection_changed = pyqtSignal(str, str, name = "platform_selection_changed")

    create_empty_excel = pyqtSignal(name = "create_empty_excel")
    create_example_excel = pyqtSignal(name = "create_example_excel")
    save_file = pyqtSignal(name = "save_file")
    load_file = pyqtSignal(name = "load_file")

    device_selected = pyqtSignal(str, name = "device_selected")


class MainView(QWidget):
    def __init__(self, actions, status):
        super(MainView, self).__init__()
        self.actions = actions
        self.status = status
        layout = QVBoxLayout()
        self.nysa_selector = NysaSelector(self.actions, self.status)
        self.file_interface = FileInterface(self.actions, self.status)
        self.register_viewer = RegisterView(self.actions, self.status)
        self.excel_engine = ExcelEngine(self.actions, self.status)
        layout.addWidget(self.nysa_selector)
        layout.addWidget(self.file_interface)

        playout = QHBoxLayout()
        playout.addWidget(self.excel_engine)
        playout.addWidget(self.register_viewer)

        layout.addLayout(playout)
        self.setLayout(layout)

    def get_nysa_selector(self):
        return self.nysa_selector

    def get_file_interface(self):
        return self.file_interface

    def get_register_view(self):
        return self.register_viewer

    def get_excel_engine(self):
        return self.excel_engine

class MainForm(QMainWindow):
    def __init__(self, actions, status):
        super (MainForm, self).__init__()
        self.status = status
        self.actions = actions
        self.mv = MainView(self.actions, self.status)
        self.setCentralWidget(self.mv)
        self.show()

    def get_nysa_selector(self):
        return self.mv.get_nysa_selector()

    def get_file_interface(self):
        return self.mv.get_file_interface()

    def get_register_view(self):
        return self.mv.get_register_view()

    def get_excel_engine(self):
        return self.exel_engine

class NysaExcelRunner(QObject):
    def __init__(self, debug):
        super (NysaExcelRunner, self).__init__()
        app = QApplication(sys.argv)
        self.actions = Actions()
        self.status = Status()
        self.actions.platform_selection_changed.connect(self.platform_selection_changed)
        self.mf = MainForm(self.actions, self.status)
        self.ns = self.mf.get_nysa_selector()
        self.fi = self.mf.get_file_interface()
        self.rw = self.mf.get_register_view()
        self.actions.scan_platforms.connect(self.scan_platforms)
        self.actions.create_empty_excel.connect(self.create_empty_excel)
        self.actions.create_example_excel.connect(self.create_example_excel)
        self.actions.save_file.connect(self.save_file)
        self.actions.load_file.connect(self.load_file)
        self.actions.device_selected.connect(self.device_selected)
        self.platform = None
        self.driver = None
        self.scan_platforms()

        if debug:
            self.status.set_level("verbose")

        app.exec_()

    def scan_platforms(self):
        ps = PlatformScanner()
        platforms_dict = ps.get_platforms()
        platform_names = platforms_dict.keys()

        if len(platform_names) > 0:
            #Always move the sim platform to the end
            if "sim" in platform_names:
                platform_names.remove("sim")
                platform_names.append("sim")

        platform_list = []
        for platform_name in platform_names:
            platform_instance = platforms_dict[platform_name](self.status)
            for platform_uid in platform_instance.scan():
                platform_list.append(QString("%s:%s" % (platform_name, platform_uid)))

        self.ns.update_platforms(platform_list)

    def platform_selection_changed(self, platform_name, board_id):
        platform_name = str(platform_name)
        board_id = str(board_id)
        self.status.Info("Platform Selection Changed to: %s:%s" % (platform_name, board_id))
        ps = PlatformScanner(self.status)
        platform_dict = ps.get_platforms()
        if platform_name not in platform_dict.keys():
            self.status.Error("Unknown Platform: %s")
            return
        platform_instances = platform_dict[platform_name](self.status)
        platforms = platform_instances.scan()
        if board_id not in platforms:
            self.status.Error("Unknown Board ID: %s in %s" % (board_id, platform_name))
            return
        platform = platforms[board_id]
        self.platform = platform
        self.driver = None
        self.device_selected("")
        self.scan_devices()

    def scan_devices(self):
        self.platform.read_sdb()
        som = self.platform.nsm.som
        self.ns.setup_sdb_tree(som)

    def create_empty_excel(self):
        self.status.Important("Create Empty Excel File")
        filepath = self.fi.get_save_filepath()
        #filepath = os.path.join(os.path.expanduser("~"), "sandbox", "file_test.xls")
        workbook = create_excel_workbook()
        workbook.save(filepath)


    def create_example_excel(self):
        self.status.Important("Create Example Excel File")
        #filepath = self.fi.get_save_filepath()
        filepath = os.path.join(os.path.expanduser("~"), "sandbox", "file_test.xls")
        setup_sheet = workbook.get_sheet(0)
        loop_sheet = workbook.get_sheet(1)
        result_sheet = workbook.get_sheet(2)

        #print "dir: Workbook: %s" % str(dir(workbook))
        #print "dir: Worksheet: %s" % str(sheet)


    def save_file(self):
        self.status.Important("Save File")

    def load_file(self):
        self.status.Important("Load File")
        filepath = self.fi.get_open_filepath()
        if len(filepath) == 0:
            return
        if not os.path.exists(filepath):
            self.status.Error("%s Doesn't exists!" % filepath)

    def device_selected(self, urn):
        self.rw.clear()
        self.rw.update()
        if urn is None:
            self.status.Verbose("Nothing selected")
        if len(urn) == 0:
            self.status.Verbose("Nothing selected")
            self.rw.clear()
            return
        self.status.Important("%s Selected" % urn)
        self.driver = ExcelDriver(self.platform, urn, self.status)
        size = self.driver.get_size()
        print "Size: %d" % size
        if size > 16:
            self.status.Warning("Size Truncated to 16")
            size = 16
        for r in range(size):
            self.rw.add_register(r, str(r), initial_value = self.driver.read_register(r))

if __name__ == "__main__":
    ner = NysaExcelRunner(True)

