import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet, Link} from  '@react-pdf/renderer'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        justifyContent: 'flex-start'
    },
    row: {
        flex: 1,
        flexDirection: 'row'
    },
    col: {
        flex: 1
    }, 
    Title: {
        fontFamily: 'MyriadWebPro',
        fontSize: 22,
        marginTop: 10,
        marginLeft: 10
    },
    section: {
        margin: 35,
        flex: 1
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
        marginHorizontal: 12,
        marginBottom: 8,
        fontSize: 12,
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
    spacer: {
        flexGrow: 1
    },
    end: {
        alignSelf: 'flex-end'
    },
    link: {
        marginHorizontal: 5
    },
    aqMap: {
        width: 300,
        height: 300
    }
})

class AquiferSummary extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        const aquifers = this.props.aquifers.geojson.features
        return (

            <View style={styles.section}>
                <Text>Aquifers</Text>
                {/* temporary filter for demo purposes. */}
                {aquifers.filter((a) => a.properties.AQNAME !== '49 IIIB (9)').map((a, i) => (
                <View key={i} style={styles.container}>
                    <View style={styles.row}>
                        <View style={styles.col}>
                            <Text style={styles.header}>
                                {a.properties.AQNAME} - {a.properties.DESCRIPTIVE_LOCATION}
                            </Text>
                            <Text style={styles.text}>
                                Type of water use: {a.properties.TYPE_OF_WATER_USE}
                            </Text>
                            <Text style={styles.text}>
                                Material: {a.properties.AQUIFER_MATERIALS}
                            </Text>
                            <Text style={styles.text}>
                                Size (km2): {a.properties.SIZE_KM2}
                            </Text>
                            <Text style={styles.text}>
                                Productivity code: {a.properties.PRODUCTIVITY_CODE}
                            </Text>
                            <Text style={styles.text}>
                                Demand code: {a.properties.DEMAND_CODE}
                            </Text>
                            <Text style={styles.text}>
                                Vulnerability code: {a.properties.VULNERABILITY_CODE}
                            </Text>
                            <Text style={styles.text}>
                                Classification code: {a.properties.CLASSIFICATION_CODE}
                            </Text>
                            <Text style={styles.text}>
                            Groundwater wells in this aquifer: 91
                            <Link src={'https://apps.nrs.gov.bc.ca/gwells/?match_any=false&search=&well=&aquifer=' + + parseInt(a.properties.AQ_TAG)}>
                                (View)
                            </Link>
                            </Text>
                        </View>
                        <View style={styles.col}>
                            <Image style={styles.aqImg} src={this.props.map}></Image>
                        </View>
                    </View>                    
                    <Image src={this.props.chart} style={styles.chart}/>
                    <Text style={styles.text}>
                        Source:
                        <Link style={styles.link} src={'https://apps.nrs.gov.bc.ca/gwells/aquifers/' + parseInt(a.properties.AQ_TAG)}>
                        {'https://apps.nrs.gov.bc.ca/gwells/aquifers/' + parseInt(a.properties.AQ_TAG)}
                        </Link>
                    </Text>
                </View>
              ))}
            </View>
        );
    }
}

export default AquiferSummary
