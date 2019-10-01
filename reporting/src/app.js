import React from "react";
import createRenderServer from '../src/server'
import ReactPDF, {
    Document, Page, View, Image, Text, Canvas, Link, Note, Font, StyleSheet
} from '@react-pdf/renderer'
// export all types from app.js so there is only one render path
export {
    ReactPDF, Document, Page, View, Image, Text, Canvas, Link, Note, Font, StyleSheet
}
import featureReport from './templates/featureReport';

const templates = {
    featureReport
};

export const renderReact = async (template, props) => {
    // Create report template
    // Add generated report template as a child to our template layout
    let rootLayoutComponent = React.createElement(template, props);
    return ReactPDF.renderToStream(rootLayoutComponent);
};

const port = process.env.PORT || 3001;

const log = (level, message) => {
    console.log(JSON.stringify({ level, message, datetime: (new Date()).toISOString() }));
};

const onReady = () => log('info', ('Server is ready on port: ' + port));

createRenderServer(templates, log).listen(port, onReady);
