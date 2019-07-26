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

const generateFeatureReport = async (data) => {
    let props = {}
    props['data'] = Object.assign({}, data)

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
        const items = Object.entries(this.props.data.properties)
        const createDate = Date()

        return (
            <View style={styles.container}>
                <Text style={styles.date}>
                Report Created: {createDate}
                </Text>
                <Text style={styles.Title}>
                    {this.props.data.featureName}
                </Text>
                <View style={styles.section}>
                    <Text style={styles.header}>Id</Text>
                    <Text style={styles.text}>{this.props.data.id}</Text>

                    <Text style={styles.header}>Location</Text>
                    <Text style={styles.text}>Latitude: {this.props.data.coordinates[0]}</Text>
                    <Text style={styles.text}>Longitude: {this.props.data.coordinates[1]}</Text>
                    <Image src={this.props.map} style={styles.chart} />

                    <Text style={styles.header} break>Properties</Text>
                    <List style={styles.section}>
                        {items.map((item, i) => (
                            <Item key={i}>{item[0]}: {item[1]}</Item>
                        ))}
                    </List>
                    <Image src={this.props.chart1} style={styles.chart}/>
                    <Image src={this.props.chart2} style={styles.chart}/>
                </View>
            </View>
        );
    }
}

export default generateFeatureReport;
