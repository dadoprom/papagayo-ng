#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.3.5.1 on Thu Apr 21 12:10:56 2005

# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
from PySide2.QtGui import QDesktopServices
import PySide2.QtWidgets as QtWidgets

from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from PySide2.QtUiTools import QUiLoader as uic
from PySide2.QtCore import QFile

from utilities import *


class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            QDesktopServices.openUrl(url)
            return False
        return True


class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.setPage(WebEnginePage(self))


class AboutBox:
    def __init__(self):
        self.loader = None
        self.ui = None
        self.ui_file = None
        self.main_window = self.load_ui_widget(os.path.join(get_main_dir(), "./rsrc/about_box.ui"))
        self.main_window.about_window_group.html_view = HtmlView(self.main_window)
        self.main_window.about_window_group.html_view.setMinimumHeight(450)
        self.main_window.about_window_group.insertWidget(0, self.main_window.about_window_group.html_view)
        self.main_window.setWindowIcon(QtGui.QIcon(os.path.join(get_main_dir(), r"rsrc\window_icon.bmp")))
        self.main_window.about_ok_button.clicked.connect(self.close)

        with open(os.path.join(get_main_dir(), r"rsrc\about.html"), "r") as html_file:
            html_file_fixed_paths = html_file.read().replace("papagayo-ng.png", r"file:///{}".format(
                os.path.join(get_main_dir(), r"rsrc\papagayo-ng.png")))
            html_file_fixed_paths = html_file_fixed_paths.replace("gpl.html", r"file:///{}".format(
                os.path.join(get_main_dir(), r"rsrc\gpl.html")))
            self.main_window.about_window_group.html_view.setHtml(html_file_fixed_paths, baseUrl=QtCore.QUrl(
                r"file:///{}".format(os.path.join(get_main_dir(), r"rsrc\about.html"))))

    def load_ui_widget(self, ui_filename, parent=None):
        loader = uic()
        file = QFile(ui_filename)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parent)
        file.close()
        return self.ui

    def close(self):
        self.main_window.close()
# end of class AboutBox
