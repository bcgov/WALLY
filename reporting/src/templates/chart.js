import React from 'react';
import {Page, Text, View, Document, StyleSheet} from '../app';

const styles = StyleSheet.create({

});

// Chart Template
export default () => (
    <Document>
        <Page size="A4" style={styles.page}>
            <View style={styles.section}>
                <Text>Section #1</Text>
            </View>
            <View style={styles.section}>
                <Text>Section #2</Text>
            </View>
        </Page>
    </Document>
);
