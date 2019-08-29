import React from 'react'
import axios from 'axios'
import {Page, Text, View, Image, Document, Font, StyleSheet} from '../app'
import Header from './common/Header'
import Footer from './common/Footer'
import List, { Item } from './common/List';
import { renderReact } from "../app";
import createChart, {exampleData, exampleData2, exampleDataLabels} from "../charts";
import SummaryMap from "./components/SummaryMap";
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
    const layerData = await axios.get(
        "http://" +
        (process.env.API_SERVICE || "") +
        "/api/v1/aggregate?" +
        querystring.stringify({
            bbox: bbox,
            layers: layers
        })
    )
    props['bbox'] = bbox
    props['data'] = layerData.data

    // Transformers
    const map = new SummaryMap()
    const watersheds = layerData.data.find(s => s.layer === mapData.WMS_WATERSHEDS)
    const aquifers = layerData.data.find(s => s.layer === mapData.WMS_AQUIFERS)
    const licences = layerData.data.find(s => s.layer === mapData.WMS_WATER_RIGHTS_LICENCES)

    map.withWatersheds(watersheds)
    map.withAquifers(aquifers)
    map.withLicences(licences)

    const mapImage = await map.png()

    props['map'] =  { data: mapImage, format: 'png' }

    props['chart1'] = await createChart('bar', exampleData, {
        xLabels: exampleDataLabels,
        ylabel: 'Licensed volume by licence (m3/day)',
        title: 'Annual licensed volume (m3/day)',
        suffix: 'm3'
    }, 400, 300)
    props['chart2'] = await createChart('line', exampleData2, {
        xLabels: shortMonthNames,
        ylabel: 'Stream Level (m)',
        title: 'Stream Levels 2010-2019 (Average) (m)',
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
                    <Aquifer aquifers={aquifers} chart={this.props.chart1}></Aquifer>
                </Page>

                {/* Hydrometric data section */}
                {hydat && hydat.geojson && hydat.geojson.features &&
                <Page size="LETTER" wrap style={styles.container}>
                    <Hydat data={hydat} chart={this.props.chart2}></Hydat>
                </Page>
                }
                
                {/* Additional layers that were selected */}

                {/* {sections.map((s, i) => (
                    <Page size="LETTER" wrap style={styles.container} key={i}>
                        <View style={styles.section} key={i}>
                            <Text style={styles.title}>{s.layer}</Text>
                            {s.geojson.features.map((f, j) => (
                                <List style={styles.section} key={j}>
                                    <Text style={styles.header}>{s.layer} {j}</Text>
                                    {Object.keys(f.properties).map((k, m) => (
                                        <Text style={styles.text} key={m}>{k}: {f.properties[k]}</Text>
                                        
                                    ))}
                                </List>
                            ))}
                            
                            <Image src={this.props.chart1} style={styles.chart}/>
                            <Image src={this.props.chart2} style={styles.chart}/>
                        </View>
                    </Page>
                ))} */}
            </Document>
        );
    }
}

export default generateFeatureReport;
