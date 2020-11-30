import Importer from '../../../src/common/utils/Importer'

describe('Importer', () => {
  it('Determines a file type and if it is accepted', () => {
    const geojsonFile = Importer.determineFileType('test.geojson')
    expect(geojsonFile.fileType).toBe('geojson')
    expect(geojsonFile.fileSupported).toBeTruthy()
    expect(geojsonFile.fileExtension).toBe('geojson')

    const csvFile = Importer.determineFileType('test.csv')
    expect(csvFile.fileType).toBe('csv')
    expect(csvFile.fileSupported).toBeTruthy()
    expect(csvFile.fileExtension).toBe('csv')

    const kmlFile = Importer.determineFileType('test.kml')
    expect(kmlFile.fileType).toBe('kml')
    expect(kmlFile.fileSupported).toBeTruthy()
    expect(kmlFile.fileExtension).toBe('kml')

    const jsonFile = Importer.determineFileType('test.json')
    expect(jsonFile.fileType).toBe('geojson')
    expect(jsonFile.fileSupported).toBeTruthy()
    expect(jsonFile.fileExtension).toBe('json')

    const exeFile = Importer.determineFileType('test.exe')
    expect(exeFile.fileType).toBe('exe')
    expect(exeFile.fileSupported).toBeFalsy()
    expect(exeFile.fileExtension).toBe('exe')

    const shpFile = Importer.determineFileType('test.shp')
    expect(shpFile.fileSupported).toBeTruthy()
    expect(shpFile.fileType).toBe('shapefile')
    expect(shpFile.fileExtension).toBe('shp')

    const shxFile = Importer.determineFileType('test.shx')
    expect(shxFile.fileSupported).toBeTruthy()
    expect(shxFile.fileType).toBe('shapefile')
    expect(shxFile.fileExtension).toBe('shx')

    const dbfFile = Importer.determineFileType('test.dbf')
    expect(dbfFile.fileSupported).toBeTruthy()
    expect(dbfFile.fileType).toBe('shapefile')
    expect(dbfFile.fileExtension).toBe('dbf')
  })

  const testCases = [
    { files: [
      { name: 'test.shp' },
      { name: 'test.dbf' },
      { name: 'test.shx' },
      { name: 'test.kml' },
      { name: 'test.geojson' }
    ],
    readFileCount: 2,
    readShapeFile: true
    },
    { files: [

      { name: 'test.geojson' }
    ],
    readFileCount: 1,
    readShapeFile: false
    },
    { files: [
      { name: 'test.dbf' },
      { name: 'test.shx' },
      { name: 'test.geojson' }
    ],
    readFileCount: 1,
    readShapeFile: false
    }
  ]

  for (const testCase of testCases) {
    it('Determines how to read files', () => {
      Importer.readShapefile = jest.fn()
      Importer.readFile = jest.fn()

      Importer.readFiles(testCase.files)
      if (testCase.readShapeFile) {
        expect(Importer.readShapefile).toHaveBeenCalled()
      }
      expect(Importer.readFile).toHaveBeenCalledTimes(testCase.readFileCount)
    })
  }
})
