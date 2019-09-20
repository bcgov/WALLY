# Wally PDF Generator App

## Introduction
This app provides an express.js API that uses the npm package [React-PDF](https://react-pdf.org/) to render 
PDF's based pre-built react templates.
The API allows named parameters to be passed in a request that will auto-populate key fields in a pdf template. 

The template API endpoint looks like:
``
http://localhost:3000/reports/featureReport
``

The templates are created using a limited set of react components:

``
Document, Page, View, Image, Text, Canvas, Link, Note, Font, StyleSheet
``

Example Template:
```
export default () => (
    <Document>
        <Page size="A4" style={styles.page}>
            <View style={styles.section}>
                <Text>Section #1</Text>
            </View>
            <View style={styles.section}>
                <Text>Section #2</Text>
            </View>
        </Page>
    </Document>
);
```
## Setup
``
npm install
``
: Install dependancies

``
npm run start
``
: This will build the app with babel and run it with node.

## Layers

Layers and API data can be added to the report by adding `&layers=LAYER_ID` to the url query params, where `LAYER_ID` is an ID that the Wally API recognizes (e.g. HYDAT). Each layer should have its own `&layers=` param, e.g. `&layers=hydrometric_stream_flow&layers=aquifers` (in other words, comma separated lists are not supported). The frameworks that Wally uses accept this format out of the box.

Some layers are required for the standard report and are always fetched, even if not included in the url params: Hydrometric data, Aquifers, Watersheds and Water Rights Licences.

## bbox (bounding box)

The `bbox` param is mandatory.  There should be 4 `bbox=...` params that together define the opposite corners of a rectangular area of interest (see example below).

## Generating a sample report

http://localhost:3000/reports/featureReport?bbox=-122.93512344360353&bbox=49.294008682393994&bbox=-122.88173675537111&bbox=49.3310514349268&layers=aquifers&layers=hydrometric_stream_flow&layers=water_rights_licences

http://localhost:8000/api/v1/aggregate?bbox=-122.93512344360353&bbox=49.294008682393994&bbox=-122.88173675537111&bbox=49.3310514349268&layers=aquifers&layers=hydrometric_stream_flow&layers=water_rights_licences
