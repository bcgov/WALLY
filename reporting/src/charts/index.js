import bar from './bar'
import line from './line'

const { CanvasRenderService } = require('chartjs-node-canvas');

const chartTemplates = {
    bar,
    line
}

const width = 500;
const height = 250;

const chartCallback = (ChartJS) => {
    // Global config example: https://www.chartjs.org/docs/latest/configuration/
    ChartJS.defaults.global.elements.rectangle.borderWidth = 2;
    // Global plugin example: https://www.chartjs.org/docs/latest/developers/plugins.html
    ChartJS.plugins.register({
        // plugin implementation
    });
    // New chart type example: https://www.chartjs.org/docs/latest/developers/charts.html
    ChartJS.controllers.MyType = ChartJS.DatasetController.extend({
        // chart implementation
    });
};

const getChartTemplate = (template) => {
    if (template in chartTemplates) {
        return chartTemplates[template];
    }
    throw new Error(`No chart template defined with name ${template}`);
}

export default async (template, data, settings, w = width, h = height) => {
    let chart = getChartTemplate(template)

    // create canvas with double height and width to help render the graphs more nicely on the page
    const canvasRenderService = new CanvasRenderService(w*2, h*2, chartCallback);
    let buffer = await canvasRenderService.renderToBuffer(chart(data, settings));
    return { data: buffer, format: 'png' } // possibly add support to return other image formats?

    // other data return types
    // const dataUrl = await canvasRenderService.renderToDataURL(configuration);
    // const stream = canvasRenderService.renderToStream(configuration);
}

export const exampleData = [ 273, 3028, 730 ]
export const exampleDataLabels = [ "500568", "500361", "500005" ]
export const exampleData2 = [ 1.4, 1.8, 1.9, 1.9, 1.7, 1.2, 1.0, 1.1, 1.3, 1.3, 1.4, 1.4 ]
