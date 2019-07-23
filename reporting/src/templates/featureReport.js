import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet} from '../app'
import Header from './common/Header'
import Footer from './common/Footer'
import font from '../assets/MyriadWebPro.ttf'
import List, { Item } from './common/List';

Font.register({
    family: 'MyriadWebPro',
    src: font,
    fontStyle: 'normal',
    fontWeight: 'bold'
});

const styles = StyleSheet.create({
    page: {
        flexDirection: 'column',
        justifyContent: 'space-between'
    },
    container: {
        flexDirection: 'column',
        justifyContent: 'flex-start'
    },
    section: {
        margin: 10,
        padding: 20,
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
    },
    Title: {
        fontFamily: 'MyriadWebPro',
        fontSize: 18,
        margin: 10
    },
    header: {
        fontFamily: 'MyriadWebPro',
        fontWeight: 'bold',
        fontSize: 16,
        marginTop: 20,
        padding: 5
    },
    info: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        paddingLeft: 10
    }
})


class FeatureReport extends React.Component {
    constructor(props) {
        super(props)
        console.log(props)
    }

    render() {
        const items = Object.entries(this.props.data.properties)
        const createDate = Date()

        return (
            <Document>
                <Page size="A4" style={styles.page}>
                    <Header/>
                    <View style={styles.container}>
                        <Text style={styles.date}>
                        Report Created: {createDate}
                        </Text>
                        <Text style={styles.Title}>
                            {this.props.data.featureName}
                        </Text>
                        <View style={styles.section}>
                            <Text style={styles.header}>Id</Text>
                            <Text style={styles.info}>{this.props.data.id}</Text>

                            <Text style={styles.header}>Location</Text>
                            <Text style={styles.info}>Latitude: {this.props.data.coordinates[0]}</Text>
                            <Text style={styles.info}>Longitude: {this.props.data.coordinates[1]}</Text>

                            <Text style={styles.header}>Properties</Text>
                            <List style={styles.section}>
                                {items.map((item, i) => (
                                    <Item key={i}>{item[0]}: {item[1]}</Item>
                                ))}
                            </List>
                            <Image src={this.props.chart} style={styles.chart}/>
                        </View>
                        <View style={styles.section}>
                            <Text></Text>
                        </View>
                    </View>
                    <Footer/>
                </Page>
            </Document>
        );
    }
}

export default FeatureReport;
