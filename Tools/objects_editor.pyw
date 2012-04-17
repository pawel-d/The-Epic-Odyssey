#!/usr/bin/env python
# Copyright (c) 2012 8-Bit Corporation. All rights reserved

"""This program allows to create, edit and delete objects
in 'data1.epic' file.
"""

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


# Stores an unsaved object.
global tmp
tmp = None


class MainWindow(QMainWindow):
    """Program's main window."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.categories = []
        self.objects = []

        self.setupUi(self)

    def setupUi(self, MainWindow):
        """Sets up the program's user interface."""

        MainWindow.setFixedSize(QSize(480, 320))

        # Initial variables
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setGeometry(QRect(10, 31, 460, 279))

        # Loads game's files into a variable.
        self.game_files = game_utils.load_game_files()

        # Validates the value of 'self.game_files', raises an error if fails.
        if not type(self.game_files) is dict:
            self.raiseError("File Error", self.game_files, True)

        # Widgets - initialization
        self.treeWidget = QTreeWidget()
        self.treeWidget.setSortingEnabled(True)

        self.addButton = QPushButton("Add")
        self.deleteButton = QPushButton("Delete")
        self.editButton = QPushButton("Edit")

        self.addButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.editButton.setEnabled(False)

        # Widgets - listeners
        self.connect(self.treeWidget,
                     SIGNAL("itemClicked(QTreeWidgetItem *, int)"),
                     self.treeItemSelected)
        self.connect(self.addButton, SIGNAL("clicked()"),
                     self.buttonListener)
        self.connect(self.deleteButton, SIGNAL("clicked()"),
                     functools.partial(self.buttonListener, delete=True))
        self.connect(self.editButton, SIGNAL("clicked()"),
                     functools.partial(self.buttonListener, edit=True))

        # Menu Bar - Initial Settings
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QRect(0, 0, 480, 21))

        self.menuHelp = QMenu("Help", self.menuBar)

        # Help Menu - Actions
        self.actionAbout = QAction("About", MainWindow)
        self.actionAbout.setShortcut(QKeySequence.WhatsThis)

        # Help Menu - Additional Settings
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuHelp.menuAction())

        MainWindow.setMenuBar(self.menuBar)

        # Menu Items - Listeners
        self.connect(self.actionAbout, SIGNAL("triggered()"), self.about)

        # Widgets - layouts
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addStretch()

        mainLayout = QHBoxLayout(self.centralWidget)
        mainLayout.addWidget(self.treeWidget)
        mainLayout.addLayout(buttonLayout)

        # Window settings
        self.setWindowTitle("The Epic Odyssey - Objects Editor")

        # Initializes the tree.
        self.populateTree()

    def about(self):
        """Displays a message with the basic informations about the program."""

        QMessageBox.about(self, "About Objects Editor",
                          """<b>Objects Editor</b> v {}
                          <p>Copyright &copy; 2012 Pawel Deregowski.
                          All rights reserved.
                          <p>Python {} | Qt {} | PyQt {} on {}""".format(
                          __version__, platform.python_version(),
                          QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def buttonListener(self, delete=False, edit=False):
        """Button listener used to add, edit or delete an object."""

        # Deletes the object.
        if delete:
            item = self.treeWidget.currentItem()
            reply = QMessageBox.question(self, "Delete " + item.text(0) + "?",
                                         "Are you sure to delete " + \
                                         item.text(0) + "?",
                                         QMessageBox.Yes | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                for first in self.game_files:
                    for second in self.game_files[first]:
                        if second.get("name") == item.text(0):
                            self.game_files[first].remove(second)
                            break
                self.populateTree()
        else:
            # Edits the object.
            if edit:
                item = self.treeWidget.currentItem()

                for first in self.game_files:
                    for second in self.game_files[first]:
                        if second.get("name") == item.text(0):
                            object_ = second
                            type_ = first
                            break

                dlg = ObjectWindow(type_, object_=object_)
                if dlg.exec_():
                    global tmp
                    if not tmp is None:
                        self.game_files[type_].remove(object_)
                        self.game_files[type_].append(tmp)
                        tmp = None
                        self.populateTree()

            # Adds a new object.
            else:
                item = self.treeWidget.currentItem()

                dlg = ObjectWindow(str(item.text(0)))
                if dlg.exec_():
                    global tmp
                    if not tmp is None:
                        self.game_files[str(item.text(0))].append(tmp)
                        tmp = None
                        self.populateTree()

    def closeEvent(self, event):
        """Defines actions to be taken when the program is closed."""

        # Saves objects to file.
        game_utils.save_game_files(self.game_files)

        # Closes the program.
        event.accept()

    def populateTree(self):
        """Updates the tree widget with the current list of items."""

        # Sets the QTreeWidget().
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Type/Name"])
        self.treeWidget.setItemsExpandable(True)

        # Populates the widget with items.
        for first in self.game_files:
            item1 = QTreeWidgetItem(self.treeWidget, [first])
            item1.setTextAlignment(1, Qt.AlignLeft | Qt.AlignVCenter)
            self.treeWidget.collapseItem(item1)
            self.categories.append(item1.text(0))

            for second in self.game_files[first]:
                item2 = QTreeWidgetItem(item1, [second.get("name")])
                item2.setTextAlignment(1, Qt.AlignCenter | Qt.AlignVCenter)
                self.treeWidget.collapseItem(item2)
                self.objects.append(item2.text(0))

        # Sorts the widget alphabetically.
        self.treeWidget.sortItems(0, Qt.AscendingOrder)

    def raiseError(self, err_title, err_message, quit_=False):
        """Displays an error on the screen."""

        QMessageBox.warning(self, err_title, err_message)
        if quit_:
            sys.exit()

    def treeItemSelected(self, item):
        """Tree widget listener used to enable/disable certain buttons."""

        # Category selection
        if item.text(0) in self.categories:
            self.addButton.setEnabled(True)
            self.deleteButton.setEnabled(False)
            self.editButton.setEnabled(False)
        # Object selection
        elif item.text(0) in self.objects:
            self.addButton.setEnabled(False)
            self.deleteButton.setEnabled(True)
            self.editButton.setEnabled(True)


class ObjectWindow(QDialog):
    """A dialog used to add a new or edit an existing object."""

    def __init__(self, type_, object_=None, parent=None):
        super(ObjectWindow, self).__init__(parent)

        self.object = object_
        self.type = type_

        # Dialog's title
        if not self.object is None:
            self.setWindowTitle("Edit " + self.object.get("name"))
        else:
            self.setWindowTitle("Add New " + self.type)

        # Sets up the dialog's user interface.
        self.setupUi(self)

    def setupUi(self, Window):
        """Sets up the dialog's user interface."""

        self.spriteSheetPath = []

        if self.type in ("Human", "Olympian", "Titan"):

            # Widgets - initialization
            nameLabel = QLabel("Name:")
            self.nameEdit = QLineEdit()
            nameLabel.setBuddy(self.nameEdit)

            if not self.object is None:
                self.nameEdit.setText(self.object.get("name"))

            imageLabel = QLabel("Spritesheet:")
            self.imageButton = QPushButton("Browse")
            imageLabel.setBuddy(self.imageButton)

            if not self.object is None:
                self.spriteSheetPath.append(self.object.get("image"))

            defenseLabel = QLabel("Defense:")
            self.defenseSpinBox = QSpinBox()
            defenseLabel.setBuddy(self.defenseSpinBox)
            self.defenseSpinBox.setRange(1, 1000)

            if not self.object is None:
                self.defenseSpinBox.setValue(self.object.get("defense"))
            else:
                if self.type == "Olympian":
                    self.defenseSpinBox.setValue(300)
                elif self.type == "Titan":
                    self.defenseSpinBox.setValue(225)
                else:
                    self.defenseSpinBox.setValue(5)

            speedLabel = QLabel("Speed:")
            self.speedSpinBox = QSpinBox()
            speedLabel.setBuddy(self.speedSpinBox)
            self.speedSpinBox.setRange(2, 8)
            self.speedSpinBox.setSingleStep(2)

            if not self.object is None:
                self.speedSpinBox.setValue(self.object.get("speed"))

            agilityLabel = QLabel("Agility:")
            self.agilitySpinBox = QSpinBox()
            agilityLabel.setBuddy(self.agilitySpinBox)
            self.agilitySpinBox.setRange(1, 100)

            if not self.object is None:
                self.agilitySpinBox.setValue(self.object.get("agility"))

            meleeWeaponLabel = QLabel("Melee weapons skill:")
            self.meleeWeaponSpinBox = QSpinBox()
            meleeWeaponLabel.setBuddy(self.meleeWeaponSpinBox)
            self.meleeWeaponSpinBox.setRange(1, 100)

            if not self.object is None:
                self.meleeWeaponSpinBox.setValue(self.object.get("skills")[0])

            rangeWeaponLabel = QLabel("Range weapons skill:")
            self.rangeWeaponSpinBox = QSpinBox()
            rangeWeaponLabel.setBuddy(self.rangeWeaponSpinBox)
            self.rangeWeaponSpinBox.setRange(1, 100)

            if not self.object is None:
                self.rangeWeaponSpinBox.setValue(self.object.get("skills")[1])

            weaponLabel = QLabel("Weapon:")
            self.weaponComboBox = QComboBox()
            weaponLabel.setBuddy(self.weaponComboBox)

            if self.type == "Human":
                self.weaponComboBox.addItem("None")

            self.acceptButton = QPushButton()

            if not self.object is None:
                self.acceptButton.setText("Save")
            else:
                self.acceptButton.setText("Create")

            # Widgets - listeners
            self.connect(self.imageButton, SIGNAL("clicked()"),
                         self.buttonListener1)

            self.connect(self.acceptButton, SIGNAL("clicked()"),
                         functools.partial(self.buttonListener2, self.type))

            # Widgets - layouts
            gridLayout = QGridLayout()
            gridLayout.addWidget(nameLabel, 0, 0)
            gridLayout.addWidget(self.nameEdit, 0, 1)
            gridLayout.addWidget(imageLabel, 1, 0)
            gridLayout.addWidget(self.imageButton, 1, 1)
            gridLayout.addWidget(defenseLabel, 2, 0)
            gridLayout.addWidget(self.defenseSpinBox, 2, 1)
            gridLayout.addWidget(speedLabel, 3, 0)
            gridLayout.addWidget(self.speedSpinBox, 3, 1)
            gridLayout.addWidget(agilityLabel, 4, 0)
            gridLayout.addWidget(self.agilitySpinBox, 4, 1)
            gridLayout.addWidget(meleeWeaponLabel, 5, 0)
            gridLayout.addWidget(self.meleeWeaponSpinBox, 5, 1)
            gridLayout.addWidget(rangeWeaponLabel, 6, 0)
            gridLayout.addWidget(self.rangeWeaponSpinBox, 6, 1)
            gridLayout.addWidget(weaponLabel, 7, 0)
            gridLayout.addWidget(self.weaponComboBox, 7, 1)

            buttonLayout = QHBoxLayout()
            buttonLayout.addStretch()
            buttonLayout.addWidget(self.acceptButton)

            mainLayout = QVBoxLayout()
            mainLayout.addLayout(gridLayout)
            mainLayout.addLayout(buttonLayout)

            # Sets the dialog's layout.
            self.setLayout(mainLayout)

        elif self.type == "Map":

            # Widgets - initialization
            nameLabel = QLabel("Name:")
            self.nameEdit = QLineEdit()
            nameLabel.setBuddy(self.nameEdit)

            if not self.object is None:
                self.nameEdit.setText(self.object.get("name"))

            configLabel = QLabel("Config file:")
            self.configButton = QPushButton("Browse")
            configLabel.setBuddy(self.configButton)

            if not self.object is None:
                self.spriteSheetPath.append(self.object.get("config"))

            texturesLabel = QLabel("Textures:")
            self.texturesButton = QPushButton("Browse")
            texturesLabel.setBuddy(self.texturesButton)

            if not self.object is None:
                self.spriteSheetPath.append(self.object.get("textures"))

            zoneLabel = QLabel("Starting zone:")
            self.zoneSpinBox = QSpinBox()
            zoneLabel.setBuddy(self.zoneSpinBox)
            self.zoneSpinBox.setRange(1, 16)

            if not self.object is None:
                self.zoneSpinBox.setValue(self.object.get("zone"))

            self.acceptButton = QPushButton()

            if not self.object is None:
                self.acceptButton.setText("Save")
            else:
                self.acceptButton.setText("Create")

            # Widgets - listeners
            self.connect(self.configButton, SIGNAL("clicked()"),
                         self.buttonListener1)

            self.connect(self.texturesButton, SIGNAL("clicked()"),
                         self.buttonListener1)

            self.connect(self.acceptButton, SIGNAL("clicked()"),
                         functools.partial(self.buttonListener2, self.type))

            # Widgets - layouts
            gridLayout = QGridLayout()
            gridLayout.addWidget(nameLabel, 0, 0)
            gridLayout.addWidget(self.nameEdit, 0, 1)
            gridLayout.addWidget(configLabel, 1, 0)
            gridLayout.addWidget(self.configButton, 1, 1)
            gridLayout.addWidget(texturesLabel, 2, 0)
            gridLayout.addWidget(self.texturesButton, 2, 1)
            gridLayout.addWidget(zoneLabel, 3, 0)
            gridLayout.addWidget(self.zoneSpinBox, 3, 1)

            buttonLayout = QHBoxLayout()
            buttonLayout.addStretch()
            buttonLayout.addWidget(self.acceptButton)

            mainLayout = QVBoxLayout()
            mainLayout.addLayout(gridLayout)
            mainLayout.addLayout(buttonLayout)

            # Sets the dialog's layout.
            self.setLayout(mainLayout)

    def buttonListener1(self):
        """Button listener used to retrieve the name of an image."""

        # Path to the 'Graphics' folder
        path = sys.path[0] + "Data//Graphics//"

        # Opens a file dialog.
        tmp_path = (unicode(QFileDialog.getOpenFileName(self,
                            "Objects Editor - Load Image",
                            path, "BMP (*.bmp)")))

        # Appends image file to the list.
        self.spriteSheetPath.append(str(tmp_path)[str(tmp_path).rfind("/") + \
                                                  1:])

    def buttonListener2(self, type_):
        """Button listener used to add a new object."""

        # Displays an error if the object's images are missing.
        if type_ == "Map" and len(self.spriteSheetPath) < 2:
                QMessageBox.warning(self, "Missing Image",
                                    "Select both images before proceeding.")
        elif len(self.spriteSheetPath) == 0:
                QMessageBox.warning(self, "Missing Spritesheet",
                                    "Select a spritesheet before proceeding.")

        # Displays an error if the object's name is too short.
        elif len(self.nameEdit.text()) == 0:
            QMessageBox.warning(self, "Incorrect Name",
                                "Name of the object needs to be at least one \
                                character long.")
        else:
            # Adds a new object to the dictionary.
            if type_ in ("Human", "Olympian", "Titan"):
                global tmp
                tmp = {"name": str(self.nameEdit.text()),
                       "image": self.spriteSheetPath[-1],
                       "defense": self.defenseSpinBox.value(),
                       "speed": self.speedSpinBox.value(),
                       "agility": self.agilitySpinBox.value(),
                       "skills": [self.meleeWeaponSpinBox.value(),
                                  self.rangeWeaponSpinBox.value()],
                       "weapon": ""}
                QDialog.accept(self)
            elif type_ == "Map":
                global tmp
                tmp = {"name": str(self.nameEdit.text()),
                       "config": self.spriteSheetPath[-2],
                       "textures": self.spriteSheetPath[-1],
                       "zone": self.zoneSpinBox.value()}
                QDialog.accept(self)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Pawel Deregowski")
    app.setApplicationName("Object Editor")
    form = MainWindow()
    form.show()

    # Execute
    app.exec_()

if __name__ == "__main__":
    main()
