import React from 'react'
import {Page, Text, View, Image, Document, Font, StyleSheet} from '../app'
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
    container: {
        flexDirection: 'column',
        justifyContent: 'flex-start'
    },
    footer: {
        alignSelf: 'flex-end'
    },
    flexGrow: {
        flexGrow: 1
    }
})

class Layout extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        const { childTemplate } = this.props
        return (
            <Document>
                    {childTemplate}
            </Document>

        );
    }
}

export default Layout;
