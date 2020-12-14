import {
  createMessageFromErrorArray,
  csvToGeoJSON,
  kmlToGeoJSON,
  xlsxToGeoJSON,
  groupErrorsByRow
} from '../../../../src/common/utils/customLayerUtils'

const fs = require('fs')
const path = require('path')

describe('csvToGeoJSON', () => {
  it('converts csv to geojson', async () => {
    const file = path.join(__dirname, './', 'test_csv.csv')
    const csvData = fs.readFileSync(file, 'utf8', function (err, data) {
      return !err && data
    })
    const geojsonData = await csvToGeoJSON(csvData)
    expect(geojsonData.data.features.length).toBe(6)
  })
  it('reports an error in csv file', async () => {
    const file = path.join(__dirname, './', 'test_csv.csv')
    const csvData = fs.readFileSync(file, 'utf8', function (err, data) {
      return !err && data
    })
    const geojsonData = await csvToGeoJSON(csvData)
    expect(geojsonData.errors.length).toBe(1)
    expect(geojsonData.errors[0].index).toBe(6) // error on row 7
  })
  it('forms an error message from the csv error array', async () => {
    const file = path.join(__dirname, './', 'test_csv.csv')
    const csvData = fs.readFileSync(file, 'utf8', function (err, data) {
      return !err && data
    })
    const geojsonData = await csvToGeoJSON(csvData)
    expect(geojsonData.errors.length).toBe(1)
    const errorMsg = createMessageFromErrorArray(geojsonData.errors)
    expect(errorMsg).toContain('A row contained an invalid value for latitude or longitude')
  })
})
describe('kmlToGeoJSON', () => {
  it('converts kml to geojson', () => {
    const file = path.join(__dirname, './', 'test_kml.kml')
    const kmlData = fs.readFileSync(file, 'utf8', function (err, data) {
      return !err && data
    })
    const geojsonData = kmlToGeoJSON(kmlData)
    expect(geojsonData.features.length).toBe(1)
  })
})
describe('xlsxToGeoJSON', () => {
  it('converts xlsx to geojson', async () => {
    const file = path.join(__dirname, './', 'test_xlsx.xlsx')
    const xlsxData = fs.readFileSync(file, function (err, data) {
      return !err && new Uint8Array(data)
    })
    const geojsonData = await xlsxToGeoJSON(xlsxData)

    expect(geojsonData.data.features.length).toBe(6)
  })
})
describe('groupErrorsByRow', () => {
  it('groups an error array by rows, removing duplicate rows', () => {
    const testErrors = [
      { index: 1 },
      { index: 1 },
      { index: 2 },
      { index: 2 },
      { index: 3 }
    ]
    const expectedIndexValues = [1, 2, 3]

    const groupedErrors = groupErrorsByRow(testErrors)
    expect(groupedErrors.length).toBe(3)
    groupedErrors.map(x => x.index).forEach((v, i) => {
      expect(v).toBe(expectedIndexValues[i])
    })
  })
})
