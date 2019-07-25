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
                <Page size="A4">
                    <View style={styles.container}>
                        <Header/>
                        {childTemplate}
                        <Footer style={{alignSelf: 'flex-end'}}/>
                    </View>
                </Page>
            </Document>
        );
    }
}

export default Layout;
