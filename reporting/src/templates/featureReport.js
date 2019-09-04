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
import ReportSummary from './components/Summary'
import Hydat from './components/Hydat'
import font from '../assets/MyriadWebPro.ttf'
import mapData from './mapData'

Font.register({
    family: 'MyriadWebPro',
    src: font,
    fontStyle: 'normal',
    fontWeight: 'bold'
});

const generateFeatureReport = async (data) => {
    let props = {}

    const bbox = data.bbox
    const layers = data.layers || []



    if (!bbox || !bbox.length || bbox.length !== 4) {
        throw "bbox must be a list of 4 numbers representing corners of a bounding box, e.g. x1,y1,x2,y2"
    }

    // default layers that should always be included.
    const defaultLayers = [
        mapData.WMS_WATERSHEDS,
        mapData.WMS_AQUIFERS,
        mapData.WMS_WATER_RIGHTS_LICENCES,
        mapData.WMS_GROUNDWATER_LICENCES
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
    
    const params = querystring.stringify({
        bbox: bbox,
        layers: layers
    })
    const layerData = await axios.get(
        `http://${host}/api/v1/aggregate?${params}`
    )

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
    const aqImg = await mb.staticPNG([-122.9101,49.3165],12, 300, 300)
    const streamImg = await mb.staticPNG([-122.8737,49.3035],14, 300, 300)

    props['map'] =  mapImage
    props['aqImg'] = aqImg
    props['streamImg'] = streamImg


    // dynamic charts are not yet implemented.
    // these charts render sample data.
    props['chart1'] = await createChart('bar', exampleData, {
        xLabels: exampleDataLabels,
        ylabel: 'Licensed volume by licence (m3/year)',
        title: 'Annual licensed volume (m3/year)',
        suffix: 'm3'
    }, 400, 300)
    props['chart2'] = await createChart('line', exampleData2, {
        xLabels: shortMonthNames,
        ylabel: 'Stream Level (m)',
        title: 'Stream Levels 1997-2018 (Average) (m)',
        suffix: 'm'
    })
    return await renderReact(FeatureReport, props)
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        justifyContent: 'flex-start',
    },
    Title: {
        fontFamily: 'MyriadWebPro',
        fontSize: 22,
        marginTop: 10,
        marginLeft: 10
    },
    section: {
        margin: 25
    },
    header: {
        fontFamily: 'MyriadWebPro',
        fontWeight: 'bold',
        fontSize: 16,
        marginTop: 10,
        padding: 5
    },
    text: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        paddingTop: 2,
        paddingLeft: 10
    },
    chart: {
        width: 400,
        height: 300,
        margin: 30,
        alignSelf: 'center'
    },
    date: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        marginTop: 10,
        marginHorizontal: 25,
    }
})

class FeatureReport extends React.Component {
    constructor(props) {
        super(props)
        // console.log(props)
    }

    render() {
        const sections = this.props.data
        const createDate = Date()
        const aquifers = sections.find(s => s.layer === mapData.WMS_AQUIFERS)
        const hydat = sections.find(s => s.layer === mapData.HYDAT)
        console.log(hydat)
        return (
            <Document title="Water Allocation Report">
                {/* Header and report summary */}
                <Page size="LETTER" style={styles.container}>
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
                <Page size="LETTER" wrap style={styles.container}>
                    <Aquifer aquifers={aquifers} chart={this.props.chart1} map={this.props.aqImg}></Aquifer>
                </Page>

                {/* Hydrometric data section */}
                {hydat && hydat.geojson && hydat.geojson.features &&
                <Page size="LETTER" wrap style={styles.container}>
                    <Hydat data={hydat} chart={this.props.chart2} map={this.props.streamImg}></Hydat>
                </Page>
                }

            </Document>
        );
    }
}

export default generateFeatureReport;
