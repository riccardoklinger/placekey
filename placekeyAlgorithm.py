# -*- coding: utf-8 -*-

"""
/***************************************************************************
 placekey
                                 A QGIS plugin
 Processing plugin for placekey
                              -------------------
        begin                : 2020-11-12
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

from collections import OrderedDict
import traceback
from PyQt5.QtCore import (QCoreApplication, QUrl, QVariant)
from qgis.core import (Qgis,
                       QgsProcessing,
                       QgsProject,
                       QgsMapLayer,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingParameterBoolean,
                       QgsMessageLog,
                       QgsWkbTypes,
                       QgsSettings)
from qgis.utils import iface

from qgis.core import QgsProcessingAlgorithm

class placekeyAlgorithm(QgsProcessingAlgorithm):

    def __init__(self):
        super().__init__()

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    CityField = 'City Field'
    LocationName = 'Location Name Field'
    StreetName = 'Street Name Field'
    HouseNumber = 'Housenumber Field'
    RegionField = 'Region Name Field'
    PostalField = 'Postal Code Field'

    def createInstance(self):
        return type(self)()

    def group(self):
        return "add placekey"

    def groupId(self):
        return "addplacekey"


class addPlacekey(placekeyAlgorithm):
    """This is an example algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the GeoAlgorithm class.
    """

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def name(self):
        """This is the provired full name.
        """
        return 'addPlacekey'

    def displayName(self):
        """This is the provired full name.
        """
        return 'Add placekey'
    
    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr(
            """HERE comes the Help""")

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input table'),
                [QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.LocationName,
                self.tr('Location Name Field'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CityField,
                self.tr('City Name Field'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.StreetName,
                self.tr('Street Name Field'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.HouseNumber,
                self.tr('House Number Field'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ReegionField,
                self.tr('Region Name Field'),
                parentLayerParameterName=self.INPUT,    
                type=QgsProcessingParameterField.String
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.PostalField,
                self.tr('Postal Code Field'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String
            )
        )
    def loadCredFunctionAlg(self):
        scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        # self.dlg.credentialInteraction.setText("")
        creds = {}
        try:
            s = QgsSettings()
            creds["key"] = s.value("placekey/api_key", None)
        except BaseException:
            print("api code load failed, check QGIS global settings")
        return creds

    def processAlgorithm(self, parameters, context, progress):
        """Here is where the processing itself takes place."""
        print("test")
        return {}