import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet, Link} from  '@react-pdf/renderer'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'column',
    },
    row: {
      flexDirection: 'row',
      flex: 1,
    },
    section: {
        marginHorizontal: 40
    },
    text: {
        fontFamily: 'MyriadWebPro',
        fontSize: 12,
        paddingTop: 2,
        paddingLeft: 10
    },
    col1: {
      flex: 1
    },
    mapImg: {
      width: 550,
      height: 300
    }
})

class ReportSummary extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        return (
          <View style={styles.container}>
            <View style={styles.row}>
              <View style={styles.co1}>
                <Image style={styles.mapImg} src={this.props.map}></Image>
              </View>
            </View>
            <View style={styles.row}>
              <View style={styles.col1}>
                <Text style={styles.text}>{`
                  Watershed: Still Creek

                  Number of wells: 37
                  Total well yield: 2100 USGPM
                  
                  Number of groundwater licences: 53
                  Water withdrawal volume (annual): 5455466 cubic metres
                `}
                </Text>
              </View>
              <View style={styles.col1}>
              </View>
            </View>
          </View>
        );
    }
}

export default ReportSummary
