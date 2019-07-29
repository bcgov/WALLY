import createChart from '../src/charts'
import _ from 'lodash'

test('chart buffer created', async () => {
    let chart = await createChart('bar', [0,1], {title: 'test', xLabels: ['1', '2']})
    expect(_.size(chart)).toBe(2)
    expect(Buffer.isBuffer(chart.data)).toBe(true)
})
