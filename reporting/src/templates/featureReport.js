import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet} from '../app'
import Header from './common/Header'
import Footer from './common/Footer'
import List, { Item } from './common/List';
import font from '../assets/MyriadWebPro.ttf'
import { renderReact } from "../app";
import createChart, {exampleData, exampleData2} from "../charts";
import locationToMapImage from "../transformers/locationToMapImage";
import {fullMonthNames, shortMonthNames} from "../styles/labels";
import sampleData from './sampleData'

const generateFeatureReport = async (data) => {
    let props = {}
    props['data'] = sampleData

    // Transformers
    props['map'] = await locationToMapImage(props.data.coordinates)
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
        justifyContent: 'flex-start'
    },
    Title: {
        fontFamily: 'MyriadWebPro',
        fontSize: 22,
        marginTop: 10,
        marginLeft: 10
    },
    section: {
        marginHorizontal: 20
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
        fontSize: 10,
        margin: 10
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

        return (
            <View style={styles.container}>
                <Text style={styles.date}>
                Report Created: {createDate}
                </Text>
                {sections.map((s, i) => {
                    <View style={styles.section}>
                        <Text style={styles.title}>{s.layer_id}</Text>
    
                        {s.geojson.filter(x => x.features && x.features.length).features.map((f, j) => {
                            <List style={styles.section}>
                                <Text style={styles.header}>{s.layer_id} {j}</Text>
                                {Object.keys(f.properties).map((k, m) => {
                                    <Text style={styles.text}>{k}: {f.properties[k]}</Text>
                                    
                                })}
                            </List>
                        })}
                        
                        <Image src={this.props.chart1} style={styles.chart}/>
                        <Image src={this.props.chart2} style={styles.chart}/>
                    </View>
                })}

            </View>
        );
    }
}

export default generateFeatureReport;
