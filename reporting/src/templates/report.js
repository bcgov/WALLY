import React from 'react'
import {Page, Text, View, Document, Font, StyleSheet} from '../app'
import Header from './common/Header'
import Footer from './common/Footer'
import font from '../assets/MyriadWebPro.ttf'

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
    section: {
        margin: 10,
        padding: 10,
    }
})

// Water Report Template
export default () => (
    <Document>
        <Page size="A4" style={styles.page}>
            <Header/>
            <View style={styles.section}>
                <Text>Section #1</Text>
            </View>
            <View style={styles.section}>
                <Text>Section #2</Text>
            </View>
            <Footer/>
        </Page>
    </Document>
);

