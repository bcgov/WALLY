import React from "react";
import createRenderServer from '../src/server'
import ReactPDF, {
    Document, Page, View, Image, Text, Canvas, Link, Note, Font, StyleSheet
} from '@react-pdf/renderer'
// export all types from app.js so there is only one render path
export {
    ReactPDF, Document, Page, View, Image, Text, Canvas, Link, Note, Font, StyleSheet
}
import layout from './templates'
import featureReport from './templates/featureReport';

const props = {}

// Create report template
const templateElemComponent = React.createElement(featureReport, props);
// Add generated report template as a child to our template layout
let rootLayoutComponent = React.createElement(layout, { childTemplate: templateElemComponent });
return ReactPDF.renderToStream(rootLayoutComponent);

