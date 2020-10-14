import {
  createMessageFromErrorArray,
  csvToGeoJSON,
  kmlToGeoJSON,
  xlsxToGeoJSON
} from '../../../../src/common/utils/customLayerUtils'

const fs = require('fs')
const path = require('path')

describe('customLayers.js', () => {
  it('converts csv to geojson', async () => {
    const file = path.join(__dirname, './', 'test_csv.csv')
    const csvData = fs.readFileSync(file, 'utf8', function (err, data) {
      return !err && data
    })
    const geojsonData = await csvToGeoJSON(csvData)
    expect(geojsonData.data.features.length).toBe(6)
  })
  it('converts kml to geojson', () => {
    const file = path.join(__dirname, './', 'test_kml.kml')
    const kmlData = fs.readFileSync(file, 'utf8', function (err, data) {
      return !err && data
    })
    const geojsonData = kmlToGeoJSON(kmlData)
    expect(geojsonData.features.length).toBe(1)
  })
  it('converts xlsx to geojson', async () => {
    const file = path.join(__dirname, './', 'test_xlsx.xlsx')
    const xlsxData = fs.readFileSync(file, function (err, data) {
      return !err && new Uint8Array(data)
    })
    const geojsonData = await xlsxToGeoJSON(xlsxData)

    expect(geojsonData.data.features.length).toBe(6)
  })
})
