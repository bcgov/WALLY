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
      margin: 35,
      flex: 1
    },
    text: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        paddingTop: 2,
    },
    row: {
      flex: 1,
      flexDirection: 'row'
    },
    col: {
      flex: 1
    },
    chart: {
      width: 500,
      height: 250,
      margin: 30,
      alignSelf: 'center'
  },
  streamMap: {
      width: 200,
      height: 200
  }
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
                  <View style={styles.row}>
                    <View style={styles.col}>
                      <Text style={styles.title}>{h.properties.name} ({h.id})</Text>
                      <Text style={styles.text}>Years available: 1997 - 2018</Text>
                      <Text style={styles.text}>
                        <Link style={styles.text} src="https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html">
                        Source: National Water Data Archive
                        </Link>
                      </Text>
                    </View>
                    <View style={styles.col}>
                      <Image src={this.props.map} style={styles.streamMap}/>

                    </View>

                  </View>

                  <Image src={this.props.chart} style={styles.chart}/>
                </View>
              ))}
            </View>
        );
    }
}

export default Hydat
