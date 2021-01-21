# Placekey API Plugin

IMPORTANT NOTE: Currently only fully supported for US and Canada based Addresses and POIs.

Placekey is designed to be a free, universal identifier for physical places. The Placekey API does the work of POI resolution, address normalization, validation, and geocoding to ensure that unique places receive unique Placekeys. Learn more at <a href="https://www.placekey.io/">placekey.io</a>.

With the Placekey plugin for QGIS 3.x, you can query the map and get a Placekey for the place of your choice. Additionally, you can process different layers/files and get the Placekey for each feature using the Placekey API.

Use this Plugin to perform the following:

### Address and POI Matching

If you are drawing address and/or POI-oriented data from multiple different places, Placekey allows you to match them together easily. Placekey can act as an alternative to a spatial join, letting you join on the Placekey attribute. This significantly reduces the downsides of spatial joins - these include geocodes on top of each other in apartment buildings or offices, densely-placed geocodes in urban areas, and street-level versus rooftop-level geocodings.

### Address Normalization

By resolving messy input address formats, Placekey removes the need to first normalize your addresses and POIs when joining them with other data. The Placekey API ensures that the same place will receive the same Placekey, even if it is referenced using multiple names and/or address conventions.

### Address and POI Deduplication

Placekey can help you remove duplicate rows in your dataset, even if their address and POI formats differ. Just Placekey all of your rows and drop duplicates of the Placekey attribute.

### Evaluate Address Data Quality

The Placekey API compares your address and POI data against multiple authoritative sources of truth in order to generate a unique Placekey for each place in your dataset. Overall data quality can be ascertained by appending Placekeys and looking at the match rate.


## Prerequesities
Please get yourself a Placekey API key at <a href="https://dev.placekey.io/default/register">placekey.io</a>. Then use the processing step <i>processing -> placekey -> manage placekey API key</i> to save your API key in the QGIS settings.

## Usage

Currently, vector layers and delimited data files (.csv) are supported. PostgreSQL data layers should work as well. If no latitude and longitude is available in your layer, make sure to fill the attributes:
- `location_name`
- `street_address` (which is street name + house number)
- `postal_code`
- `city`
- `region` (which is state in the US)
- `iso_country_code` (only `US`, `CA` are supported right now). If no country is provided, the plugin defaults it to `US`.

The API supports various sub-combinations of the above attributes, such as (`location_name`, `latitude`, and `longitude`), (`street_address`, `city`, and `region`), (`street_address`, `region`, and `postal_code`). For full API specifications, please see the <a href="https://docs.placekey.io/">API docs</a>.

If you would like to drop the geomery information, check "use Attributes Only" in the dialog. Otherwise we will use point-geometries. If your layer is of type polygon/polyline, we will calculate centroids and use them as inputs for `latitude` and `longitude`. This will be treated as prime information on the API side, so will outrule the attribute information (like `street_address`, `postal_code` and so on). 

If you want to have all source attributes of the input dataset copied to the output, make sure to enable "Copy All Atributes".

Resulting Layer will use EPSG 4326 and the centroids of input data if available.

## Support
If you find issues or have enhancement requests, make sure to create an issue on this repo and we will get back to you as soon as possible. If it's an option on your side, please make sure to add some minimal data example for your issue / user story

## Additional Resources
- <a href="https://docs.placekey.io/">Placekey API Documentation</a>
- <a href="https://digital-geography.com/joining-data-with-the-placekey-qgis-plugin/">Digital Geography Blog</a>
- <a href="https://www.youtube.com/watch?v=MD0khQxYaZE&feature=emb_title">Plugin Demo Video</a>

## Tags

address matching, poi matching, address normalization, address standardization, address verification, address validation, address parsing, address correction, company name matching, business name matching, company name normalization, company name standardization, data conflation, deduplication
