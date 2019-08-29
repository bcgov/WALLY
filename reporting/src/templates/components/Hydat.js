import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet, Link} from  '@react-pdf/renderer'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        justifyContent: 'flex-start'
    },
    sectionTitle: {
      fontFamily: 'MyriadWebPro',
      fontSize: 22,
      marginTop: 10,
      marginBottom: 10
    },
    title: {
      fontFamily: 'MyriadWebPro',
      fontSize: 16,
      marginTop: 10,
      marginBottom: 10
    },
    row: {
      flexDirection: 'row',
      flex: 1,
    },
    section: {
      margin: 35
    },
    text: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        paddingTop: 2,
    },
    col1: {
      flex: 1
    },
    chart: {
      width: 500,
      height: 250,
      margin: 30,
      alignSelf: 'center'
  },
})

class Hydat extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        const hydat = this.props.data.geojson.features
        return (

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Hydrometric Data - Stream Stations</Text>
              {hydat.map((h, i) => (
                <View key={i}>
                  <Text style={styles.title}>{h.properties.name} ({h.id})</Text>
                  <Image src={this.props.chart} style={styles.chart}/>
                </View>
              ))}
            </View>
        );
    }
}

export default Hydat
