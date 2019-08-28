import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet, Link} from  '@react-pdf/renderer'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
        justifyContent: 'flex-start'
    },
    title: {
      fontFamily: 'MyriadWebPro',
      fontSize: 22,
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
              <Text style={styles.title}>Hydrometric Data - Stream Stations</Text>
              {hydat.map((h, i) => (
                <Text style={styles.text} key={i}>{h.properties.name}</Text>
              ))}
            </View>
        );
    }
}

export default Hydat
