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

})

class EcoCat extends React.Component {
    render() {
        const ecocat = this.props.data.geojson.features || []

        return (

            <View style={styles.section}>
              <Text style={styles.sectionTitle}>EcoCat Reports</Text>
              {ecocat.map((report, i) => (
                <View key={i}>
                  <View style={styles.row}>
                    <View style={styles.col}>
                      <Text style={styles.text}>{report.properties.TITLE}</Text>
                    </View>

                  </View>
                  <View style={styles.row}>
                    <View style={styles.col}>
                      <Text style={styles.text}>
                        <Link style={styles.text} src={`https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=${report.properties.REPORT_ID}`}>
                          {`https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=${report.properties.REPORT_ID}`}
                        </Link>
                      </Text>
                    </View>
                  </View>
                </View>
              ))}
            </View>
        );
    }
}

export default EcoCat
