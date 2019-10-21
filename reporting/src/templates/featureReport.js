import React from 'react'
import axios from 'axios'
import {Page, Text, View, Image, Document, Font, StyleSheet} from '../app'
import Header from './common/Header'
import Footer from './common/Footer'
import List, { Item } from './common/List';
import { renderReact } from "../app";
import createChart, {exampleData, exampleData2, exampleDataLabels} from "../charts";
import MapboxAPI from "./components/mapboxService";
import {fullMonthNames, shortMonthNames} from "../styles/labels";
import { sampleData } from './sampleData'
import querystring from 'querystring'

import Aquifer from './components/Aquifer'
import EcoCat from './components/EcoCat'
import ReportSummary from './components/Summary'
import GenericDatasheet from './components/GenericDatasheet'
import Hydat from './components/Hydat'
import font from '../assets/MyriadWebPro.ttf'
import strings from './mapData'

Font.register({
    family: 'MyriadWebPro',
    src: font,
    fontStyle: 'normal',
    fontWeight: 'bold'
});

const log = (level, message) => {
    console.log(JSON.stringify({ level, message, datetime: (new Date()).toISOString() }));
};

const featureReport = async (data) => {
    let props = {}

    // bbox is used to display the search area with a Mapbox map image.
    // the actual search area is defined by the polygon attribute
    const bbox = data.bbox
    const searchPolygon = data.polygon
    let layers = []

    // get request with only one layer comes in as string, not array, so we check here
    if(typeof(data.layers) === 'string') {
        layers.push(data.layers)
    } else {
        layers = data.layers
    }

    if (!bbox || !bbox.length || bbox.length !== 4) {
        throw "bbox must be a list of 4 numbers representing corners of a bounding box, e.g. x1,y1,x2,y2"
    }

    // default layers that should always be included.
    const defaultLayers = [
        strings.aquifers,
        strings.water_rights_licences
    ]

    // add in default layers before making request
    for (let i = 0; i < defaultLayers.length; i++) {
        if (!layers.includes(defaultLayers[i])) {
            layers.push(defaultLayers[i])
        }
    }

    // Fetch aggregated map data.
    // The API's service name needs to be known.
    // For an OpenShift deployment, this should be the OpenShift service name.
    // For local development, this should correspond to the API's docker-compose
    // service name.  See env-backend.env in Wally's root folder to fill in
    // this value for docker-compose.
    const host = process.env.API_SERVICE
    if (!host) {
        throw "the API hostname must be provided in environment variable API_SERVICE"
    }
    log('info', `retrieving data from ${host}...`)    
    const params = querystring.stringify({
        bbox: bbox,
        polygon: searchPolygon,
        layers: layers
    })
    const layerData = await axios.get(
        `http://${host}/api/v1/aggregate?${params}`
    )
    log('info', 'data retrieved, generating map image...')
    props['bbox'] = bbox
    props['data'] = layerData.data

    // Transformers
    const mb = new MapboxAPI()

    // create a viewport for accessing the Mapbox static images API.
    // the viewport consists of a center coordinate pair and a zoom level.
    const summaryViewport = mb.bboxToViewport(bbox.map(x => Number(x)), [1100, 600])

    // generate overview image, returning a png file buffer that we can use in the ReactPDF components.
    const mapImage = await mb.staticPNG(summaryViewport.center,summaryViewport.zoom, 1100, 600)

    // "sample" images for aquifers and stream stations.
    // we may not need to generate separate images for every object.
    // const aqImg = await mb.staticPNG([-122.9101,49.3165],12, 300, 300)
    // const streamImg = await mb.staticPNG([-122.8737,49.3035],14, 300, 300)
    // props['aqImg'] = aqImg
    // props['streamImg'] = streamImg
    
    props['map'] =  mapImage



    // dynamic charts are not yet implemented.
    // these charts render sample data.
    // props['chart1'] = await createChart('bar', exampleData, {
    //     xLabels: exampleDataLabels,
    //     ylabel: 'Licensed volume by licence (m3/year)',
    //     title: 'Annual licensed volume (m3/year)',
    //     suffix: 'm3'
    // }, 400, 300)
    // props['chart2'] = await createChart('line', exampleData2, {
    //     xLabels: shortMonthNames,
    //     ylabel: 'Stream Level (m)',
    //     title: 'Stream Levels 1997-2018 (Average) (m)',
    //     suffix: 'm'
    // })
    log('info', 'map generated, retrieving layer catalogue info...')
    const catalogue = await axios.get(
        `http://${host}/api/v1/catalogue`
    )
    props['catalogue'] = catalogue.data.layers

    return await renderReact(FeatureReport, props)
}

const styles = StyleSheet.create({
    page: {
        flexDirection: 'column',
        justifyContent: 'flex-start',
        paddingBottom: 20
    },
    section: {
        margin: 25
    },
    date: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        marginTop: 10,
        marginHorizontal: 25
    }
})

class FeatureReport extends React.Component {
    constructor(props) {
        super(props)
        // console.log(props)
    }

    render() {
        const sections = this.props.data.display_data
        const createDate = Date()

        // as we develop custom feature components, break the feature data out to process separately.
        let featureData = {}
        featureData[strings.aquifers] = sections.find(s => s.layer === strings.aquifers)
        featureData[strings.HYDAT] = sections.find(s => s.layer === strings.HYDAT)
        featureData[strings.ECOCAT] = sections.find(s => s.layer === strings.ECOCAT)

        // make a list of any additional layers that we haven't pulled out.
        const extraSections = sections.filter(s => {
            return !featureData[s.layer]
        })

        return (
            <Document title="Water Allocation Report">
                {/* Header and report summary */}
                <Page size="LETTER" style={styles.page}>
                    <Header/>
                    <Text style={styles.date}>
                        Report Created: {createDate}
                    </Text>
                    <View style={styles.section}>
                        <ReportSummary 
                            map={this.props.map}
                        ></ReportSummary>
                    </View>
                </Page>

                {/* Aquifer section */}
                {featureData[strings.aquifers] && featureData[strings.aquifers].geojson &&
                    !!featureData[strings.aquifers].geojson.features &&
                    <Page size="LETTER" wrap style={styles.page}>
                        <Aquifer
                            aquifers={featureData[strings.aquifers]}
                        ></Aquifer>
                    </Page>
                }

                {/* Hydrometric data section */}
                {featureData[strings.HYDAT] &&
                    featureData[strings.HYDAT].geojson &&
                    !!featureData[strings.HYDAT].geojson.features &&
                    <Page size="LETTER" wrap style={styles.container}>
                        <Hydat
                            data={featureData[strings.HYDAT]}
                        ></Hydat>
                    </Page>
                }

                {/* Hydrometric data section */}
                {featureData[strings.ECOCAT] &&
                    featureData[strings.ECOCAT].geojson &&
                    !!featureData[strings.ECOCAT].geojson.features &&
                    <Page size="LETTER" wrap style={styles.page}>
                        <EcoCat
                            data={featureData[strings.ECOCAT]}
                        ></EcoCat>
                    </Page>
                }

                {/* All other data that doesn't have custom components will be displayed in list format. */}
                {extraSections.map((s, i) => (
                <Page size="LETTER" wrap style={styles.page} key={i}>
                    <GenericDatasheet
                        wrap
                        data={s}
                        highlightFields={this.props.catalogue.find(l => l.display_data_name === s.layer)
                            .highlight_columns}
                    ></GenericDatasheet>
                </Page>
                ))}


            </Document>
        );
    }
}

export default featureReport;
