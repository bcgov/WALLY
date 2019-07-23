import React from 'react'
import colors from '../../styles/colors'
import {
    Image, StyleSheet, Text, View,
} from '../../app'

const styles = StyleSheet.create({
    container: {
        flexDirection: 'col',
        borderTopWidth: 2,
        backgroundColor: colors.blue,
        borderTopColor: colors.yellow,
        borderTopStyle: 'solid',
        alignItems: 'space-between'
    },
    disclaimerColumn: {
        alignSelf: 'center',
        justifySelf: 'center'
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
            Annotations:
            Walmsly, N., & Pearce, G. (2010). Towards Sustainable Water Resources Management: Bringing the Strategic Approach up-to-date. Irrigation & Drainage Systems, 24(3/4), 191–203.
            USGS - Earth's water distribution
        </Text>
    </View>
);
