import { determineFileType, getFileExtension } from '../../../src/common/utils/fileUtils'

describe('File utils', () => {
  beforeEach(function () {
    console.warn = jest.fn()
  })

  it('Determines a file type and if it is accepted', () => {
    const geojsonFile = determineFileType('test.geojson')
    expect(geojsonFile.fileType).toBe('geojson')
    expect(geojsonFile.fileSupported).toBeTruthy()
    expect(geojsonFile.fileExtension).toBe('geojson')

    const csvFile = determineFileType('test.csv')
    expect(csvFile.fileType).toBe('csv')
    expect(csvFile.fileSupported).toBeTruthy()
    expect(csvFile.fileExtension).toBe('csv')

    const kmlFile = determineFileType('test.kml')
    expect(kmlFile.fileType).toBe('kml')
    expect(kmlFile.fileSupported).toBeTruthy()
    expect(kmlFile.fileExtension).toBe('kml')

    const jsonFile = determineFileType('test.json')
    expect(jsonFile.fileType).toBe('geojson')
    expect(jsonFile.fileSupported).toBeTruthy()
    expect(jsonFile.fileExtension).toBe('json')

    const exeFile = determineFileType('test.exe')
    expect(exeFile.fileType).toBe('exe')
    expect(exeFile.fileSupported).toBeFalsy()
    expect(exeFile.fileExtension).toBe('exe')

    const shpFile = determineFileType('test.shp')
    expect(shpFile.fileSupported).toBeTruthy()
    expect(shpFile.fileType).toBe('shapefile')
    expect(shpFile.fileExtension).toBe('shp')

    const shxFile = determineFileType('test.shx')
    expect(shxFile.fileSupported).toBeFalsy()
    expect(shxFile.fileExtension).toBe('shx')

    const dbfFile = determineFileType('test.dbf')
    expect(dbfFile.fileSupported).toBeTruthy()
    expect(dbfFile.fileType).toBe('shapefile')
    expect(dbfFile.fileExtension).toBe('dbf')
  })

  it('Returns the file extension', () => {
    expect(getFileExtension('test.hello')).toBe('hello')
    expect(getFileExtension('test')).toBe(null)
    expect(getFileExtension('test.hello.world')).toBe('world')
    expect(getFileExtension(null)).toBe(null)
  })
})
