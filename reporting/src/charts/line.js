import colors from '../styles/colors'

// Data Format: 12 points, single int values
// [ 26, 2, 5, 16, 111, 200, 254, 140, 75, 31, 20, 30 ]
// number of labels should match number of data points

export default (data, settings) => {
    const {
        title = '',
        xLabels = '',
        yLabel = '',
        prefix = '',
        suffix = '',
        color = colors.blue
    } = settings

    return {
        type: 'line',
        data: {
            labels: xLabels,
            datasets: [
                {
                    label: yLabel,
                    backgroundColor: color,
                    data: data
                }
            ]
        },
        options: {
            title: {
                display: title !== '',
                text: title
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: (value) => prefix + value + suffix
                    }
                }]
            }
        }
    }
};

// Raw Config Example
// const lineConfig = {
//     type: 'line',
//     data: {
//         labels: [ 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May' ],
//         datasets: [
//             {
//                 label: 'Precipitation Levels 2017 (mm)',
//                 backgroundColor: '#086CA2',
//                 data: [ 26, 2, 5, 16, 111, 200, 254, 140, 75, 31, 20, 30 ]
//             }
//         ]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero: true,
//                     callback: (value) => value + 'mm'
//                 }
//             }]
//         }
//     }
// };
