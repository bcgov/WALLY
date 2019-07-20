import React from 'react'
import colors from '../../styles/colors'
import {
    Image, StyleSheet, Text, View,
} from '../../app'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        borderTopWidth: 2,
        backgroundColor: colors.blue,
        borderTopColor: colors.yellow,
        borderTopStyle: 'solid',
        alignItems: 'space-between',
    },
    disclaimerColumn: {
        alignSelf: 'center',
        justifySelf: 'center',
    },
    disclaimerText: {
        fontSize: 10,
        color: colors.white,
        margin: 20
    },
    links: {
        fontSize: 24,
        fontFamily: 'MyriadWebPro',
        fontWeight: 'bold',
        color: colors.white
    }
});

export default () => (
    <View style={styles.container}>
        <Text style={styles.disclaimerText}>
            Disclaimer: Lorem Ipsum is simply dummy text of the printing and typesetting industry.
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an
            unknown printer took a galley of type and scrambled it to make a type specimen book.
            It has survived not only five centuries, but also the leap into electronic typesetting.
        </Text>
    </View>
);
