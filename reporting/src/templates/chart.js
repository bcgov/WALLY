import React from 'react';
import {Page, Text, View, Document, StyleSheet} from '../app';
import chart from '../charts'

const styles = StyleSheet.create({

});

// Chart Template
export default () => (
    <View>
        <View style={styles.section}>
            <Text>Section #1</Text>
        </View>
        <View>
            <Text>Section #2</Text>
        </View>
    </View>
);
