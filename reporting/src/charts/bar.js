import colors from '../styles/colors'

// Data Format, 12 points, single int values
// [ 26, 2, 5, 16, 111, 200, 254, 140, 75, 31, 20, 30 ]
// number of labels should match number of data points

export default (data, settings) => {
    const {
        xLabels = '',
        yLabel = '',
        prefix = '',
        suffix = '',
        backgroundColor = colors.lightBlue,
        borderColor = colors.blue,
        borderWidth = 1
    } = settings

    return {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [{
                label: yLabel,
                data: data,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: borderWidth
            }]
        },
        options: {
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
// const barConfig = {
//     type: 'bar',
//     data: {
//         labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//         datasets: [{
//             label: '# of Votes',
//             data: [12, 19, 3, 5, 2, 3],
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.2)',
//                 'rgba(54, 162, 235, 0.2)',
//                 'rgba(255, 206, 86, 0.2)',
//                 'rgba(75, 192, 192, 0.2)',
//                 'rgba(153, 102, 255, 0.2)',
//                 'rgba(255, 159, 64, 0.2)'
//             ],
//             borderColor: [
//                 'rgba(255,99,132,1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)'
//             ],
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero: true,
//                     callback: (value) => '$' + value
//                 }
//             }]
//         }
//     }
// };
