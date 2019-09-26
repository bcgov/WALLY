import React from 'react'
import fs from 'fs';
import colors from '../../styles/colors'
import logo from '../../assets/BCID_H_rgb_pos.jpg'
import {
    Image, StyleSheet, Text, View,
} from '../../app'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        borderBottomWidth: 0,
        borderBottomColor: colors.darkGrey,
        borderBottomStyle: 'solid',
        backgroundColor: colors.white,
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    logoContainer: {
        flex: 1
    },
    logo: {
        alignSelf: 'flex-start',
        width: 170,
        height: 66
    },
    titleContainer: {
        flex: 2,
        flexDirection: 'row',
        justifyContent: 'flex-start',
        alignItems: 'center'
    },
    title: {
        fontSize: 24,
        fontFamily: 'MyriadWebPro',
        fontWeight: 'bold',
        color: colors.blue
    }
});

const logoFile = fs.readFileSync(logo)

export default () => (
    <View style={styles.container}>
        <View style={styles.logoContainer}>
            <Image src={logoFile} style={styles.logo}/>
        </View>
        <View style={styles.titleContainer}>
            <Text style={styles.title}>Water Allocation Report</Text>
        </View>
    </View>
);
