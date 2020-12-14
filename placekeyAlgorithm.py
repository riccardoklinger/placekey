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

import traceback
import math
import time
from PyQt5.QtCore import (QCoreApplication, QUrl, QVariant)
from qgis.core import (Qgis,
                       QgsCoordinateTransform,
                       QgsFeature,
                       QgsFeatureSink,
                       QgsFields,
                       QgsField,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSink,
                       QgsProject,
                       QgsMapLayer,
                       QgsProcessingException,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterMapLayer,
                       QgsProcessingParameterField,
                       QgsCoordinateReferenceSystem,
                       QgsMessageLog,
                       QgsWkbTypes,
                       QgsSettings)
from qgis.utils import iface
import requests
import json


class placekeyAlgorithm(QgsProcessingAlgorithm):

    def __init__(self):
        super().__init__()

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    CityField = 'City Field'
    Mode = 'Mode'
    LocationField = 'Location Name Field'
    AddressField = 'Address Field'
    RegionField = 'Region Name Field'
    PostalField = 'Postal Code Field'
    CountryField = 'ISO Country Code Field'
    copyAttributes = 'Copy Attributes'
    DropGeo = 'Use Attributes only'

    def createInstance(self):
        return type(self)()

    def group(self):
        return "Add placekey"

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
        should provide a basic description about what the algorithm does and
        the parameters and outputs associated with it..
        """
        return self.tr(
            """This algorithm adds a placekey to your table. The placekey is
            defined either by a set of:
            - (lat, lon) taken from the geometry
            - (street_address, city, region, country) or
            - (street_address, region, postal_code, country)
            and a placename if needed.
            <a href="https://docs.placekey.io/">Placekey API Documentation</a>
            ______________
            Parameters:
            - Location Name Field: the name of the place / "Twin Peaks Petroleum"
            - City Name Field: The city where the place is located / "San Francisco"
            - Address Field: The street address of the place / "1543 Mission Street"
            - Region Name Field: The second-level administrative region below nation for the place. In the US, this is the state / "California" or "CA"
            - Postal Code: The postal code for the place / "94105"
            - Country Code: The ISO 2-letter Country Code for the place. Defaults to 'US' if none given.
            - Copy all Attributes: If checked we will copy all attributes from the input layer to the output. If false, we will only copy the feature id.
            - Use Attributes Only: If checked we will not use lat/lon as input atributes which then will 

            The output layer will be stored in EPSG 4326.
            Make sure to have your placekey API key added to the options using 'Manage placekey API keys"
            """)

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterMapLayer(
                self.INPUT,
                self.tr('Input table'),
                #[QgsProcessing.TypeFile,
                # QgsProcessing.TypeVector,
                # QgsProcessing.TypeVectorPoint,
                # QgsProcessing.TypeVectorAnyGeometry,
                # QgsProcessing.TypeMapLayer]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.LocationField,
                self.tr('Location Name Field'),
                parentLayerParameterName=self.INPUT,
                defaultValue="",
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CityField,
                self.tr('City Name Field'),
                parentLayerParameterName=self.INPUT,
                defaultValue="",
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.AddressField,
                self.tr('Address Field'),
                parentLayerParameterName=self.INPUT,
                defaultValue="",
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.RegionField,
                self.tr('Region Name Field'),
                parentLayerParameterName=self.INPUT,
                defaultValue="",
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.PostalField,
                self.tr('Postal Code Field'),
                parentLayerParameterName=self.INPUT,
                defaultValue="",
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CountryField,
                self.tr('ISO Country Code Field'),
                parentLayerParameterName=self.INPUT,
                defaultValue="",
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.copyAttributes,
                self.tr('Copy all Attributes')
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.DropGeo,
                self.tr('Use Attributes Only')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Layer with Placekeys')
            )
        )

    def loadCredFunctionAlg(self):
        creds = {}
        try:
            s = QgsSettings()
            creds["key"] = s.value("placekey/api_key", None)
        except BaseException:
            print("no API key found!")
        return creds

    def valueCheck(self, string):
        if string == "nan" or string == "NULL" or string == "0":
            return ""
        else:
            return string

    def addPayloadItem(self, parameters, source, context, feature, feedback):
        """getting field names"""
        locationName = self.parameterAsString(
            parameters,
            self.LocationField,
            context
        )
        cityName = self.parameterAsString(
            parameters,
            self.CityField,
            context
        )
        addressName = self.parameterAsString(
            parameters,
            self.AddressField,
            context
        )
        regionName = self.parameterAsString(
            parameters,
            self.RegionField,
            context
        )
        zipCode = self.parameterAsString(
            parameters,
            self.PostalField,
            context
        )
        country = self.parameterAsString(
            parameters,
            self.CountryField,
            context
        )
        geometry = self.parameterAsString(
            parameters,
            self.DropGeo,
            context
        )
        item = {
            "query_id": str(feature.id()),
        }
        if locationName != "":
            item["location_name"] = self.valueCheck(
                str(feature[locationName]))
        if addressName != "":
            item["street_address"] = self.valueCheck(str(feature[addressName]))
        if cityName != "":
            item["city"] = self.valueCheck(str(feature[cityName]))
        if zipCode != "":
            item["postal_code"] = self.valueCheck(str(feature[zipCode]))
        if regionName != "":
            item["region"] = self.valueCheck(str(feature[regionName]))
        if country != "":
            item["iso_country_code"] = self.valueCheck(str(feature[country]))
        if country == "":
            item["iso_country_code"] = "US"
        if geometry == "false":
            featGeometry = feature.geometry().centroid()
            sourceCrs = source.sourceCrs()
            if source.sourceCrs != QgsCoordinateReferenceSystem(4326):
                destCrs = QgsCoordinateReferenceSystem(4326)
                tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
                featGeometry.transform(tr)
            if math.isnan(featGeometry.asPoint().y()) is False:
                item["latitude"] = featGeometry.asPoint().y()
                item["longitude"] = featGeometry.asPoint().x()
            else:
                print("strange geometry found at feature with id " + str(feature.id()))
        return item

    def getKeys(self, payload, result, key, feedback):
        url = "https://api.placekey.io/v1/placekeys"
        headers = {
            'apikey': key,
            'Content-Type': 'application/json',
            'user-agent': 'placekey-qgis/1.0 batchMode'
        }
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=json.dumps(payload)
        )
        if response.status_code == 401:
            feedback.pushInfo(
                """check your API key. Seems like you're unauthorized!"""
            )
            raise QgsProcessingException(
                    "invalid API key")
        if response.status_code == 429:
            for retry in range(1, 11):
                feedback.pushInfo('waiting 10s, rate limit exceeded')
                feedback.pushInfo("trying again" + str(retry) + "/10 ")
                time.sleep(10)
                response = requests.request(
                    "POST",
                    url,
                    headers=headers,
                    data=json.dumps(payload)
                )
                if response.status_code == 200:
                    break
                if retry == 10:
                    raise QgsProcessingException(
                        "tried 10 times, cancelling processing"
                    )
        if response.status_code == 200:
            if "error" in response.json():
                for entry in payload["queries"]:
                    result.append(json.loads(
                        """{"query_id": """ +
                        str(entry["query_id"]) +
                        """, "placekey": "Invalid address"}"""))
            else:
                for item in response.json():
                    if "placekey" in item:
                        result.append(item)
                    if "error" in item:
                        result.append(json.loads(
                            """{"query_id": """ +
                            str(item["query_id"]) +
                            """, "placekey": "Invalid address"}"""))
        if response.status_code == 400:
            try:
                if response.json()["error"][0:2] == "All":
                    for entry in payload["queries"]:
                        result.append(json.loads(
                            """{"query_id": """ +
                            str(entry["query_id"]) +
                            """, "placekey": "Invalid address"}"""))
            except BaseException:
                raise QgsProcessingException(
                    """No proper request sent. Details in the python log,
                    make sure to have a proper set off attributes.
                    If you're using a point layer, make sure to have
                    valid geometries for all features! Response was: """ +
                    response.text)

        return result

    def inputCheck(self, source, parameters, context, feedback):
        locationName = self.parameterAsString(
            parameters,
            self.LocationField,
            context
        )
        cityName = self.parameterAsString(
            parameters,
            self.CityField,
            context
        )
        addressName = self.parameterAsString(
            parameters,
            self.AddressField,
            context
        )
        regionName = self.parameterAsString(
            parameters,
            self.RegionField,
            context
        )
        zipCode = self.parameterAsString(
            parameters,
            self.PostalField,
            context
        )
        country = self.parameterAsString(
            parameters,
            self.CountryField,
            context
        )
        geometry = self.parameterAsString(
            parameters,
            self.DropGeo,
            context
        )
        # no attributes given:
        if source.wkbType() in [0, 3, 4, 100]:
            feedback.pushInfo(
                "using a layer with no geometry. only attributes are used!"
            )
            if (locationName == "" and
                cityName == "" and
                addressName == "" and
                regionName == "" and
                zipCode == "" and
                country == "" and geometry == "true"):
                raise QgsProcessingException(
                    """You disabled geometry. Please provide additional
                    information like city name, zipcode and address /
                    housenumber to conszruct the WHERE part."""
                )
            if cityName == "" and zipCode == "" and geometry == "true":
                raise QgsProcessingException(
                    "please provide either city name or postal code"
                )

    def processAlgorithm(self, parameters, context, feedback):
        """checking for key"""
        key = self.loadCredFunctionAlg()["key"]
        if key == "" or key is None:
            feedback.reportError("no API key found!", True)
            raise QgsProcessingException(
                "no API key found! ")
        """getting the input table"""
        source = self.parameterAsSource(
            parameters,
            self.INPUT,
            context
        )
        if source.wkbType() in [1004, 2004, 3004]:
            raise QgsProcessingException(
                "MultiPoint layer are not supported!")
        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(
                    parameters, self.INPUT
                )
            )
        self.inputCheck(source, parameters, context, feedback)
        """predefining the output layer"""
        copy = self.parameterAsString(
            parameters,
            self.copyAttributes,
            context
        )
        geometry = self.parameterAsString(
            parameters,
            self.DropGeo,
            context
        )
        fields = source.fields()
        if copy == "false": 
            fields.clear()
            fields.append(QgsField("origin_id", QVariant.LongLong))

        fields.append(QgsField("placekey", QVariant.String))
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Point,
            source.sourceCrs()
        )
        if sink is None:
            raise QgsProcessingException(
                self.invalidSinkError(
                    parameters, self.OUTPUT))
        feedback.pushInfo(
            '{} points for placekey finding'.format(
                source.featureCount()))
        features = source.getFeatures()
        """lining up the entries"""
        payload = {"queries": []}
        batches = []
        result = []
        if source.featureCount() < 100:
            """small mode"""
            for current, feature in enumerate(features):
                if feedback.isCanceled():
                    break
                payload["queries"].append(self.addPayloadItem(parameters,
                                                              source,
                                                              context,
                                                              feature,
                                                              feedback))
            batches.append(payload)
            result = self.getKeys(batches[0], result, key, feedback)
        else:
            """batch mode"""
            index = 0
            for current, feature in enumerate(features):
                if feedback.isCanceled():
                    break
                index += 1
                if index % 100 != 0 and index != source.featureCount():
                    payloadItem = self.addPayloadItem(parameters,
                                                      source,
                                                      context,
                                                      feature,
                                                      feedback)
                    payload["queries"].append(payloadItem)
                if index % 100 == 0:
                    payloadItem = self.addPayloadItem(parameters,
                                                      source,
                                                      context,
                                                      feature,
                                                      feedback)
                    payload["queries"].append(payloadItem)
                    batches.append(payload)
                    payload = {"queries": []}
                if index == source.featureCount():
                    payloadItem = self.addPayloadItem(parameters,
                                                      source,
                                                      context,
                                                      feature,
                                                      feedback)
                    payload["queries"].append(payloadItem)
                    batches.append(payload)
                    payload = {"queries": []}
            currentBatch = 0
            for batch in batches:
                if feedback.isCanceled():
                    break
                currentBatch += 1
                result = self.getKeys(batch, result, key, feedback)
                feedback.setProgress(int(currentBatch / len(batches) * 100))
            feedback.pushInfo('gathering placekeys finished...')
        '''processing result'''
        features = source.getFeatures()
        feedback.pushInfo('merging source with placekeys...')
        if geometry == "true":
            feedback.pushInfo('attributes used for inputs, resulting geometry is the centroid of input geometries')
        if geometry == "false":
            feedback.pushInfo('centroids of geometries used for inputs and resulting geomtry of placekey layer')
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break
            #fet = QgsFeature()
            fet = QgsFeature(fields)
            if copy == "true":
                attributes = feature.attributes()
            try:
                fet.setGeometry(feature.geometry().centroid())
            except BaseException:
                feedback.pushInfo('no geometry available')
            for index in range(0, len(result)):
                if str(result[index]["query_id"]) == str(feature.id()):
                    placekey = result[index]["placekey"]
                    if copy == "true":
                        attributes.append(placekey)
                        fet.setAttributes(attributes)
                    else: 
                        fet.setAttribute(0, feature.id())
                        fet.setAttribute(1, placekey)
                    result.pop(index)
                    break
            sink.addFeature(fet, QgsFeatureSink.FastInsert)
            feedback.setProgress(int(current / source.featureCount()) * 100)
        return {self.OUTPUT: dest_id}
