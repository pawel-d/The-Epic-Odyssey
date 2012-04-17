#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved

"""This program allows to script quests,
that are used within the game.
"""

from __future__ import with_statement

__version__ = "0.1"

import functools
import os
import platform
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Fixes the program's main directory to use in local packages and modules.
if __name__ == "__main__":
    sys.path[0] = os.getcwd()[:-len("Tools")]

import Routines.game_utils as game_utils
from Main.constants import *


GAME_KEYWORDS = ((r"\bcan_move\b", r"\bcreate_human\b", r"\bcreate_map\b",
                  r"\bcreate_olympian\b", r"\bcreate_titan\b", r"\bevent\b",
                  r"\bload_human\b", r"\bload_map\b", r"\bload_olympian\b",
                  r"\bload_titan\b", r"\bmove_unit\b", r"\bmove_unit_steps\b",
                  r"\bplace_unit\b", r"\bsay\b", r"\bset_background_sound\b",
                  r"\bset_map\b", r"\bset_music\b",
                  r"\bset_player_character\b", r"\bsee\b",
                  r"\bturn_unit\b", r"\bunits_in_range\b"))

PYTHON_KEYWORDS = ((r"\band\b", r"\bas\b", r"\bassert\b",
                    r"\bbreak\b", r"\bclass\b", r"\bcontinue\b",
                    r"\bdef\b", r"\bdel\b", r"\belif\b", r"\belse\b",
                    r"\bexcept\b", r"\bexec\b", r"\bfinally\b", r"\bfor\b",
                    r"\bfrom\b", r"\bglobal\b", r"\bif\b", r"\bimport\b",
                    r"\bin\b", r"\bis\b", r"\blambda\b", r"\bnot\b",
                    r"\bor\b", r"\bpass\b", r"\bprint\b", r"\braise\b",
                    r"\breturn\b", r"\btry\b", r"\bwhile\b", r"\bwith\b",
                    r"\byield\b"))


class MainWindow(QMainWindow):
    """Program's main window."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.path = ""
        self.unsaved = False

        self.setupUi(self)

    def setupUi(self, MainWindow):
        """Sets up the program's user interface."""

        MainWindow.setFixedSize(QSize(800, 600))

        # Initial variables
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setGeometry(QRect(10, 31, 780, 559))

        # Widgets
        self.textArea = QPlainTextEdit(self.centralWidget)
        self.textArea.setGeometry(QRect(0, 0, 780, 559))
        self.textArea.setFont(QFont("Monospace", 10))
        self.textArea.setUndoRedoEnabled(True)

        palette = self.textArea.palette()
        palette.setColor(QPalette.Active, QPalette.Text, Qt.white)
        palette.setColor(QPalette.Active, QPalette.Base, QColor(0, 30, 65))
        self.textArea.setPalette(palette)

        self.highlighter = KeywordsHighlighter(self.textArea.document())

        # Widgets - listeners
        self.connect(self.textArea, SIGNAL("modificationChanged(bool)"),
                     self.textChanged)

        # Menu Bar - Initial Settings
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QRect(0, 0, 800, 21))

        self.menuFile = QMenu("File", self.menuBar)

        # File Menu - Actions
        self.actionClose = QAction("Close", MainWindow)
        self.actionNew = QAction("New", MainWindow)
        self.actionOpen = QAction("Open", MainWindow)
        self.actionSave = QAction("Save", MainWindow)
        self.actionSaveAs = QAction("Save As", MainWindow)

        self.actionClose.setShortcut(QKeySequence.Quit)
        self.actionNew.setShortcut(QKeySequence.New)
        self.actionOpen.setShortcut(QKeySequence.Open)
        self.actionSave.setEnabled(False)
        self.actionSave.setShortcut(QKeySequence.Save)
        self.actionSaveAs.setEnabled(False)
        self.actionSaveAs.setShortcut(QKeySequence.SaveAs)

        # File Menu - Additional Settings
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.menuHelp = QMenu("Help", self.menuBar)

        # Help Menu - Actions
        self.actionAbout = QAction("About", MainWindow)
        self.actionManual = QAction("Manual", MainWindow)

        self.actionAbout.setShortcut(QKeySequence.WhatsThis)
        self.actionManual.setShortcut(QKeySequence.HelpContents)

        # Help Menu - Additional Settings
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionManual)
        self.menuBar.addAction(self.menuHelp.menuAction())

        MainWindow.setMenuBar(self.menuBar)

        # Menu Items - Listeners
        self.connect(self.actionAbout, SIGNAL("triggered()"), self.about)
        self.connect(self.actionClose, SIGNAL("triggered()"), self.close)
        self.connect(self.actionManual, SIGNAL("triggered()"), self.manual)
        self.connect(self.actionNew, SIGNAL("triggered()"), self.new)
        self.connect(self.actionOpen, SIGNAL("triggered()"), self.open_)
        self.connect(self.actionSave, SIGNAL("triggered()"), self.save)
        self.connect(self.actionSaveAs, SIGNAL("triggered()"),
                     functools.partial(self.save, True))

        # Window settings
        self.setWindowTitle("The Epic Odyssey - Quests Editor")

    def about(self):
        QMessageBox.about(self, "About Quest Editor",
                          """<b>Quests Editor</b> v {}
                          <p>Copyright &copy; 2012 Pawel Deregowski.
                          All rights reserved.
                          <p>Python {} | Qt {} | PyQt {} on {}""".format(
                          __version__, platform.python_version(),
                          QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def closeEvent(self, event):
        if not self.unsaved:
            event.accept()
        elif len(str(self.textArea.toPlainText())) > 0:
            reply = QMessageBox.question(self,
                    "Quests Editor - Unsaved Changes",
                    "Save unsaved changes?",
                    QMessageBox.Yes | QMessageBox.No |
                    QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                if len(self.path) > 0:
                    self.save(self.path)
                else:
                    self.save()
                if not self.unsaved:
                    event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()

    def manual(self):
        dialog = ManualDialog(self)
        if dialog.exec_():
            self.hide()

    def new(self):
        if self.unsaved:
            reply = QMessageBox.question(self,
                    "Quests Editor - Unsaved Changes",
                    "Save unsaved changes?",
                    QMessageBox.Yes | QMessageBox.No |
                    QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                if len(self.path) > 0:
                    self.save(self.path)
                else:
                    self.save()
                if not self.unsaved:
                    self.textArea.clear()
            elif reply == QMessageBox.No:
                self.textArea.clear()
                self.unsaved = False
                self.setWindowTitle("The Epic Odyssey - Quests Editor")
        else:
            self.textArea.clear()
            self.unsaved = False
            self.setWindowTitle("The Epic Odyssey - Quests Editor")

    def open_(self):
        self.path = unicode(QFileDialog.getOpenFileName(self,
                            "Quests Editor - Load File",
                            PATH_QUESTS,
                            "SRC (*.src)"))
        if len(self.path) > 0:
            try:
                with open(self.path, "r") as fh:
                    self.textArea.setPlainText(fh.read())
            except IOError:
                QMessageBox.warning(self, "IO Error",
                                    "Error! Cannot load the file.")
            else:
                self.setWindowTitle("The Epic Odyssey - Quests Editor : " \
                                    + self.path)

    def save(self, save_as=False):
        if save_as or len(self.path) == 0:
            fname = unicode(QFileDialog.getSaveFileName(self,
                            "Object Editor - Save File",
                            PATH_QUESTS + "untitled.src",
                            "SRC (*.src)"))
            if len(fname) > 0:
                try:
                    if fname[-4:] != ".src":
                        fname += ".src"
                    with open(fname, "w") as fh:
                        fh.write(str(self.textArea.toPlainText()))
                except IOError:
                    QMessageBox.warning(self, "IO Error",
                                        "Error! Cannot save the file.")
                else:
                    self.path = fname
                    self.unsaved = False
        else:
            try:
                with open(self.path, "w") as fh:
                    fh.write(str(self.textArea.toPlainText()))
            except IOError:
                QMessageBox.warning(self, "IO Error",
                                    "Error! Cannot save the file.")
            else:
                self.unsaved = False

    def textChanged(self, changed):
        if changed:
            if not self.unsaved:
                self.unsaved = True
                for i in [self.actionSave, self.actionSaveAs]:
                    if not i.isEnabled():
                        i.setEnabled(True)
        else:
            if self.unsaved:
                self.unsaved = False
                for i in [self.actionSave, self.actionSaveAs]:
                    if i.isEnabled():
                        i.setEnabled(False)


class KeywordsHighlighter(QSyntaxHighlighter):

    Rules = []

    def __init__(self, parent=None):
        super(KeywordsHighlighter, self).__init__(parent)

        gameKeywordFormat = QTextCharFormat()
        gameKeywordFormat.setForeground(QColor(255, 165, 0))
        for pattern in GAME_KEYWORDS:
            KeywordsHighlighter.Rules.append((QRegExp(pattern),
                                              gameKeywordFormat))

        pythonKeywordFormat = QTextCharFormat()
        pythonKeywordFormat.setForeground(Qt.yellow)
        for pattern in PYTHON_KEYWORDS:
            KeywordsHighlighter.Rules.append((QRegExp(pattern),
                                              pythonKeywordFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(160, 82, 45))
        commentFormat.setFontItalic(True)
        KeywordsHighlighter.Rules.append((QRegExp(r"#.*"),
                                        commentFormat))
        self.stringFormat = QTextCharFormat()
        self.stringFormat.setForeground(QColor(218, 165, 32))
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        KeywordsHighlighter.Rules.append((stringRe, self.stringFormat))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        KeywordsHighlighter.Rules.append((self.stringRe,
                                        self.stringFormat))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')

    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE = range(3)

        for regex, format_ in KeywordsHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, format_)
                i = regex.indexIn(text, i + length)

        self.setCurrentBlockState(NORMAL)
        if self.stringRe.indexIn(text) != -1:
            return
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = text.length()
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3, self.stringFormat)
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, text.length(), self.stringFormat)


class ManualDialog(QDialog):

    def __init__(self, parent=None):
        super(ManualDialog, self).__init__(parent)

        self.resize(QSize(640, 480))

        self.browser = QTextBrowser()
        try:
            with open(PATH_MISC + "manual.html", "r") as fh:
                self.browser.setHtml(fh.read())
        except IOError:
            QMessageBox.warning(self, "IO Error",
                                "Error! Cannot load the manual file.")
            sys.exit()
        else:
            self.browser.setReadOnly(True)
            layout = QVBoxLayout()
            layout.addWidget(self.browser)
            self.setLayout(layout)
            self.setWindowTitle("Quests Editor - Manual")


# Overrides the built-in 'TextEdit' class.
class TextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)

    def event(self, event):
        if (event.type() == QEvent.KeyPress and
            event.key() == Qt.Key_Tab):
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
        return QTextEdit.event(self, event)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Pawel Deregowski")
    app.setApplicationName("Quests Editor")
    form = MainWindow()
    form.show()

    # Executes the program.
    app.exec_()

if __name__ == "__main__":
    main()
