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
    }
})

class GenericDatasheet extends React.Component {
    render() {
        const features = this.props.data.geojson.features || []
        return (

            <View wrap style={styles.section}>
              <Text style={styles.sectionTitle}>{this.props.data.layer}</Text>
              {features.map((feat, i) => (
                <View wrap={false} key={i} style={styles.col}>

                  {/* If a name field is supplied, display it. */}
                  <Text style={styles.title}>{feat.name}</Text>

                  {/* Generate one line for every item in the GeoJSON properties */}
                  {Object.keys(feat.properties).filter((key) => {
                    return this.props.highlightFields.includes(key)
                  }).map((geojsonProperty, j) => (
                    <View style={styles.row} key={j}>
                      <View style={styles.col}>
                        <Text style={styles.text}>{geojsonProperty}</Text>
                      </View>
                      <View style={styles.col}>
                        <Text style={styles.text}>{feat.properties[geojsonProperty]}</Text>
                      </View>
                    </View>
                  ))}
                </View>
              ))}
            </View>
        );
    }
}

export default GenericDatasheet
