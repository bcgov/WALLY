# Wally PDF Generator App

## Introduction
This app provides an express.js API that uses the npm package [React-PDF](https://react-pdf.org/) to render 
PDF's based pre-built react templates.
The API allows named parameters to be passed in a request that will auto-populate key fields in a pdf template. 

The template API endpoint looks like:
``
http://localhost:3000/:template
``
The endpoint can accept any template name and will generate the matching report if the template name exists. 

The templates are created using a limited set of react components:

``
Document, Page, View, Image, Text, Canvas, Link, Note, Font, StyleSheet
``

Example Template:
```
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
```
## Setup
``
npm install
``
: Install dependancies

``
npm run start
``
: This will build the app with babel and run it with node 
## 
