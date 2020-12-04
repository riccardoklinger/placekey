# Placekey API Plugin
With the placekey plugin for QGIS 3.x you can query the map and get a placekey for the place of your choice. Additionally you can process different layers/files and get the placekey for each feature using the placekey API.

## Prerequesities
Please get yourself a placekey API key at <a href="https://www.placekey.io/">placekey.io</a>. Then use the processing step <i>processing -> placekey -> manage placekey API key</i> to save your API key in the qgis settings.

## Usage

Currently point layers and delimited data files (example a csv) are supported. PostgreSQL data layers should work as well. If no Latitude and Longitude is available in your layer, make sure to fill the attributes:
- placename
- street name + house number
- postcode
- city
- region
- country (only US and NL are supported right now). If no country is provided, the plugin defaults it to "US".

## Support
If you find issues, have enhancement wishes, make sure to create an issue on this repo and we will get back to you as soon as possible. If it's an option on your side, please make sure to add some minimal data example for your issue / user story
