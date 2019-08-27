import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet, Link} from  '@react-pdf/renderer'

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
        margin: 35
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
                {aquifers.map((a, i) => (
                <View key={i}>
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
                    <Link src={'https://apps.nrs.gov.bc.ca/gwells/aquifers/' + parseInt(a.properties.AQ_TAG)}>
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
