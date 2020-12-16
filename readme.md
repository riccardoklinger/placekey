# Placekey API Plugin
With the Placekey plugin for QGIS 3.x, you can query the map and get a Placekey for the place of your choice. Additionally, you can process different layers/files and get the Placekey for each feature using the Placekey API.

## Prerequesities
Please get yourself a Placekey API key at <a href="https://www.placekey.io/">placekey.io</a>. Then use the processing step <i>processing -> placekey -> manage placekey API key</i> to save your API key in the QGIS settings.

## Usage

Currently, vector layers and delimited data files (.csv) are supported. PostgreSQL data layers should work as well. If no latitude and longitude is available in your layer, make sure to fill the attributes:
- `location_name`
- `street_address` (which is street name + house number)
- `postal_code`
- `city`
- `region` (which is state in the US)
- `iso_country_code` (only `US` and `NL` are supported right now). If no country is provided, the plugin defaults it to `US`.

The API supports various sub-combinations of the above attributes, such as (`location_name`, `latitude`, and `longitude`), (`street_address`, `city`, and `region`), (`street_address`, `region`, and `postal_code`). For full API specifications, please see the <a href="https://docs.placekey.io/">API docs</a>.

If you would like to drop the geomery information, check "use Attributes Only" in the dialog. Otherwise we will use point-geometries. If your layer is of type polygon/polyline, we will calculate centroids and use them as inputs for `latitude` and `longitude`. This will be treated as prime information on the API side, so will outrule the attribute information (like `street_address`, `postal_code` and so on). 

If you want to have all source attributes of the input dataset copied to the output, make sure to enable "Copy All Atributes".

Resulting Layer will use EPSG 4326 and the centroids of input data if available.

## Support
If you find issues or have enhancement requests, make sure to create an issue on this repo and we will get back to you as soon as possible. If it's an option on your side, please make sure to add some minimal data example for your issue / user story
