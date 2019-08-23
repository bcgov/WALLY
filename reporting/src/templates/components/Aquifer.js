import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet} from  '@react-pdf/renderer'

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
                <View break key={i}>
                  <Text>
                    {a.properties.AQNAME} - {a.properties.DESCRIPTIVE_LOCATION}
                  </Text>
                </View>
              ))}
            </View>
        );
    }
}

export default AquiferSummary
