import bar from './bar'
import line from './line'

const { CanvasRenderService } = require('chartjs-node-canvas');

const chartTemplates = {
    bar,
    line
}

const width = 500;
const height = 400;

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

export default async (template, data, settings) => {
    let chart = getChartTemplate(template)
    const canvasRenderService = new CanvasRenderService(width, height, chartCallback);
    let buffer = await canvasRenderService.renderToBuffer(chart(data, settings));
    return { data: buffer, format: 'png' } // possibly add support to return other image formats?

    // other data return types
    // const dataUrl = await canvasRenderService.renderToDataURL(configuration);
    // const stream = canvasRenderService.renderToStream(configuration);
}

export const exampleData = [ 26, 2, 5, 16, 111, 200, 254, 140, 75, 31, 20, 30 ]
export const exampleData2 = [ 1, 2, 5, 5, 4, 9, 15, 12, 3, 22, 1, 3 ]
