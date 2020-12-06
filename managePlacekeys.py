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


class managePlacekey(QgsProcessingAlgorithm):

    def __init__(self):
        super().__init__()

    INPUT = 'API Key'
    OUTPUT = 'Result'

    def createInstance(self):
        return type(self)()

    def group(self):
        return "Manage placekey API key"

    def groupId(self):
        return "managePlacekeyAPI"


class manageKeys(managePlacekey):
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
        return 'managePlacekey'

    def displayName(self):
        """This is the provired full name.
        """
        return 'Manage placekey API keys'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr(
            """Saves your Placekey API key for the use of the placekey processing. To get a free API Key, register at <a href='https://dev.placekey.io/default/register'>placekey.io</a>""")

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT,
                self.tr('API Key')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """getting the api key"""
        s = QgsSettings()
        key = self.parameterAsString(
            parameters,
            self.INPUT,
            context
        )
        s.setValue("placekey/api_key", key)
        feedback.pushInfo(
            """Success! Your API key was updated/saved and will be used for future placekey requests."""
        )
        return {}

