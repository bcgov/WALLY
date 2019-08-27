import React from 'react'
import axios from 'axios'
import {Page, Text, View, Image, Document, Font, StyleSheet} from '../app'
import Header from './common/Header'
import Footer from './common/Footer'
import List, { Item } from './common/List';
import { renderReact } from "../app";
import createChart, {exampleData, exampleData2} from "../charts";
import Map from "../transformers/locationToMapImage";
import {fullMonthNames, shortMonthNames} from "../styles/labels";
import { sampleData } from './sampleData'
import querystring from 'querystring'

import Aquifer from './components/Aquifer'
import ReportSummary from './components/Summary'
import Hydat from './components/Hydat'
import font from '../assets/MyriadWebPro.ttf'

Font.register({
    family: 'MyriadWebPro',
    src: font,
    fontStyle: 'normal',
    fontWeight: 'bold'
});

const generateFeatureReport = async (data) => {
    let props = {}

    const bbox = data.bbox
    const layers = data.layers

    if (!bbox || !bbox.length || bbox.length !== 4) {
        throw "bbox must be a list of 4 numbers representing corners of a bounding box, e.g. x1,y1,x2,y2"
    }

    if (!layers) {
        throw "layers must be supplied"
    }

    const layerData = await axios.get("http://backend:8000/api/v1/aggregate?" +
        querystring.stringify({
            bbox: bbox,
            layers: layers
        })
    )
    props['bbox'] = bbox
    props['data'] = layerData.data

    // Transformers
    const map = new Map(bbox)
    const mapImage = await map.png()

    props['map'] =  { data: mapImage, format: 'png' }

    props['chart1'] = await createChart('line', exampleData, {
        xLabels: shortMonthNames,
        ylabel: 'Precipitation Levels 2017 (mm)',
        title: 'Monthly Precipitation Levels 2017 (mm)',
        suffix: 'mm'
    })
    props['chart2'] = await createChart('bar', exampleData2, {
        xLabels: fullMonthNames,
        ylabel: '# of Votes',
        title: 'Number of Votes'
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
        const aquifers = sections.find(s => s.layer === 'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW')
        const hydat = sections.find(s => s.layer === 'HYDAT')

        console.log(aquifers)

        return (
            <Document>
                {/* Header and report summary */}
                <Page size="LETTER" style={styles.container}>
                    <Header/>
                    <Text style={styles.date}>
                        Report Created: {createDate}
                    </Text>
                    <View style={styles.section}>
                        <ReportSummary map={this.props.map}></ReportSummary>
                    </View>
                </Page>

                {/* Aquifer section */}
                <Page size="LETTER" wrap style={styles.container}>
                    <Aquifer aquifers={aquifers}></Aquifer>
                </Page>

                {/* Hydrometric data section */}
                {hydat && hydat.geojson && hydat.geojson.features &&
                <Page size="LETTER" wrap style={styles.container}>
                    <Hydat data={hydat}></Hydat>
                </Page>
                }
                
                {/* Additional layers that were selected */}

                {/* {sections.map((s, i) => (
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
                ))} */}
            </Document>
        );
    }
}

export default generateFeatureReport;
