from qgis.PyQt.QtCore import Qt, QUrl
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsProcessingException
from qgis.gui import QgsMapToolEmitPoint, QgsMapToolPan
import requests
from .placekeyAlgorithm import addPlacekey
import json


class GetMapCoordinates(QgsMapToolEmitPoint):
    '''Class to interact with the map canvas to capture the coordinate
    when the mouse button is pressed.'''

    def __init__(self, iface):
        QgsMapToolEmitPoint.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.canvasClicked.connect(self.clicked)
        # self.pt4326=None

    def activate(self):
        '''When activated set the cursor to a crosshair.'''

    def clicked(self, pt, b):
        # if self.dlg.captureButton.isChecked():
        '''Capture the coordinate when the mouse button has been released,
        format it, and copy it to dashboard'''
        # transform the coordinate to 4326 but display it in the original crs
        canvasCRS = self.canvas.mapSettings().destinationCrs()
        epsg4326 = QgsCoordinateReferenceSystem('EPSG:4326')
        transform = QgsCoordinateTransform(
            canvasCRS, epsg4326, QgsProject.instance())
        pt4326 = transform.transform(pt.x(), pt.y())
        lat = pt4326.y()
        lon = pt4326.x()
        # change dockwidget corrdinate with the original crs
        self.dockwidget.lineEdit_2.setText("no address found")
        try:
            key = addPlacekey.loadCredFunctionAlg(self)["key"]
            if key == "" or key is None:
                raise QgsProcessingException(
                    "no API key found! add one using 'Manage placekey API keys'")
                self.dockwidget.lineEdit_2.setText("no API key found! add one using 'Manage placekey API keys'")
                return
        except BaseException:
            print("no API key found! add one using 'Manage placekey API keys'")
            self.dockwidget.lineEdit_2.setText("no API key found! add one using 'Manage placekey API keys'")
            return
        ### getting Placekey from Input ###
        placeText = self.dockwidget.lineEdit.text()
        country = self.dockwidget.comboBox.currentText()
        url = "https://api.placekey.io/v1/placekey"
        headers = {
            'apikey': key,
            'Content-Type': 'application/json'
        }
        payload = {
            "query": {
                "location_name": placeText,
                "iso_country_code": country,
                "latitude": lat,
                "longitude": lon
            }
        }
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(payload)
        )
        self.dockwidget.lineEdit_2.setText(str(response.json()["placekey"]))
        self.dockwidget.toolButton.setChecked(False)
        self.iface.mapCanvas().setCursor(Qt.ArrowCursor)
        #if self.dockwidget.toolButton.isChecked():
        #    print("something went wrong")
        #    try:
        #        self.dockwidget.label.setText("test")
        #            #json.loads(
         #           #    r.text)["items"][0]["title"])
         #   except BaseException:
         #       self.dockwidget.label.setText("no address found")
         #       
         ##   self.dockwidget.label.setText(
           #     str("tests"))
           # self.dockwidget.toolButton.setChecked(False)

    def setWidget(self, dockwidget):
        self.dockwidget = dockwidget
