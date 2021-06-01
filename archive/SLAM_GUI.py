# SLAM_GUI.py
# Last Modified: 27 February 2021
# Description: This file is the SLAM user interface file, defining all windows, etc.
import sys, io
import slam_variables
import folium
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QAction, QHBoxLayout, QTreeView, QToolBar
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, *args, **kwargs):
        """Initializes SLAM"""
        super(Window, self).__init__(*args, **kwargs)
        self.setWindowTitle(slam_variables.app_name + ": Version " + slam_variables.app_version)
        self.resize(slam_variables.app_width, slam_variables.app_height)
        layout = QHBoxLayout()
        
        # Creates the menu bar and its items
        self._createActions()
        self._createMenuBar()
        
        # Create widgets using self-defined functions
        mapView = self._createMap() # Create the main map
        treeView = self._createItemViewer() # Create the item tree viewer

        # Create the main widget and add sub-widgets to it
        mainWidget = QWidget()
        layout.addWidget(treeView, 1)
        layout.addWidget(mapView, 3)
        # Set the layout of the main widget to layout, a QHBoxLayout
        mainWidget.setLayout(layout)
        # Add the main widget to the GUI
        self.setCentralWidget(mainWidget)

    def getValue(self, val):
        print(val.data())
        print(val.row())
        print(val.column())

### HELPER FUNCTIONS TO CREATE GUI ###
    def _createMenuBar(self):
        """Creates Menu Bars"""
        
        # Define menu bars
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")
        viewMenu = menuBar.addMenu("&View")
        gisMenu = menuBar.addMenu("&GIS")
        satelliteMenu = menuBar.addMenu("&Satellite")
        groundMenu = menuBar.addMenu("&Ground")

        # Populate File menu
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exportAction)

        # Populate Edit menu
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)

        # Populate View menu


        # Populate GIS menu
        gisMenu.addAction(self.mercatorAction)
        gisMenu.addAction(self.globeAction)
        gisMenu.addAction(self.exportShapefileAction)

        # Populate Satellite menu
        satelliteMenu.addAction(self.newSatellite)

        # Populate Ground menu
        groundMenu.addAction(self.newGroundStation)

    def _createActions(self):
        """Creates Actions for Menu Bar"""
        # File
        self.newAction = QAction("&New Analysis", self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.saveAsAction = QAction("&Save As", self)
        self.exportAction = QAction("&Export", self)

        # Edit
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)

        # View
        

        # GIS
        self.mercatorAction = QAction("&Mercator", self)
        self.globeAction = QAction("&Globe", self)
        self.exportShapefileAction = QAction("&Export Shapefile")

        # Satellite
        self.newSatellite = QAction("&New", self)

        # Ground
        self.newGroundStation = QAction("&New", self)

    def _createItemViewer(self):
        # Creates the object viewer
        treeView = QTreeView()
        treeView.setHeaderHidden(True)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        # TODO: this needs to be dynamic, of course
        exampleLink = Item('Link', 12, set_bold=True)
        

        return treeView

    def _createMap(self):
        m = folium.Map(
            location=[37.210537, -80.39623], zoom_start=5
        )

        data = io.BytesIO()
        m.save(data, close_file=False)
        

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())

        return webView

class Item(QStandardItem):

    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

