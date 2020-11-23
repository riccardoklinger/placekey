# -*- coding: utf-8 -*-
"""
/***************************************************************************
 placekey
                                 A QGIS plugin
 adds placekeys to your data
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Riccardo Klinger
        email                : riccardo.klinger@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .placekey_dockwidget import placekeyDockWidget
from .GetMapCoordinates import GetMapCoordinates
# Import for Processing
from qgis.core import QgsApplication
from placekey.placekeyProvider import placekeyProvider

import os.path


class placekey:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.provider = placekeyProvider()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'placekey_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Placekey Connector')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'placekey')
        self.toolbar.setObjectName(u'placekey')

        #print "** INITIALIZING placekey"

        self.pluginIsActive = False
        self.dockwidget = None

        self.getMapCoordinates = GetMapCoordinates(self.iface)
        self.getMapCoordTool = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('placekey', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/placekey/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Placekey'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # init the processing
        QgsApplication.processingRegistry().addProvider(self.provider)

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING placekey"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD placekey"

        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&Placekey Connector'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        # remove the processing
        QgsApplication.processingRegistry().removeProvider(self.provider)

    #--------------------------------------------------------------------------
    def setGetMapToolCoordFrom(self):
        """ Method that is connected to the target button. Activates and deactivates map tool """
        if self.dockwidget.toolButton.isChecked():
            print("true FROM")
            self.iface.mapCanvas().unsetMapTool(self.getMapCoordTool)
            self.dockwidget.toolButton.setChecked(True)
            return
        if self.dockwidget.toolButton.isChecked() is False:
            self.iface.mapCanvas().setCursor(Qt.CrossCursor)
            self.iface.mapCanvas().setMapTool(self.getMapCoordTool)
            self.dockwidget.toolButton.setChecked(False)
            return

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True
            #print "** STARTING placekey"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = placekeyDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            #self.dockwidget.toolButton.clicked.connect(self.setGetMapToolCoordFrom)  
            self.dockwidget.toolButton.setIcon(
                QIcon(
                    os.path.join(
                        os.path.dirname(__file__),
                        "target.png")))
            self.getMapCoordTool = self.getMapCoordinates
            self.getMapCoordTool.setButton(self.dockwidget.toolButton)
            self.getMapCoordTool.setWidget(self.dockwidget)
            self.iface.mapCanvas().setMapTool(self.getMapCoordTool)
            self.dockwidget.toolButton.pressed.connect(self.setGetMapToolCoordFrom)
            self.dockwidget.show()
