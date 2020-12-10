import Importer from '../../../src/common/utils/Importer'
import store from '../../../src/store/index'

describe('Importer', () => {
  it('Sets error message for file extension not supported', () => {
    store.commit = jest.fn()
    store.dispatch = jest.fn()

    const txtFile = new File([''], 'test.txt')
    Importer.readFile(txtFile)

    expect(store.dispatch).toHaveBeenCalledWith('importer/processFile', {
      filename: txtFile.name,
      message: 'file of type .txt not supported.',
      status: 'error'
    })
    expect(store.commit).toHaveBeenCalledWith('importer/clearQueuedFiles')
  })

  const testCases = [
    { files: [
      { name: 'test.shp' },
      { name: 'test.dbf' },
      { name: 'test.shx' },
      { name: 'test.kml' },
      { name: 'test.geojson' }
    ],
    readFileCount: 3,
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
    readFileCount: 2,
    readShapeFile: true
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

  const testCasesShapefiles = [
    {
      filename: 'test',
      files: [
        { name: 'test.dbf' },
        { name: 'test.shp' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      returnObj: {
        files: [{ name: 'test.geojson' }],
        shapefiles: {
          'shp': { name: 'test.shp' },
          'dbf': { name: 'test.dbf' },
          'prj': { name: 'test.prj' }
        }
      }
    },
    {
      filename: 'test',
      files: [
        { name: 'test.shp' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      returnObj: {
        files: [{ name: 'test.geojson' }],
        shapefiles: {
          'shp': { name: 'test.shp' },
          'dbf': null,
          'prj': { name: 'test.prj' }
        }
      }
    },
    {
      filename: 'test',
      files: [
        { name: 'test.dbf' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      returnObj: {
        files: [{ name: 'test.geojson' }],
        shapefiles: {
          'shp': null,
          'dbf': { name: 'test.dbf' },
          'prj': { name: 'test.prj' }
        }
      }
    },
    {
      filename: 'test',
      files: [
        { name: 'testo.shp' },
        { name: 'test.dbf' },
        { name: 'test.geojson' }
      ],
      returnObj: {
        files: [
          { name: 'testo.shp' },
          { name: 'test.geojson' }
        ],
        shapefiles: {
          'shp': null,
          'dbf': { name: 'test.dbf' },
          'prj': null
        }
      }
    },
    {
      filename: 'tester',
      files: [
        { name: 'test.shp' },
        { name: 'test.dbf' },
        { name: 'test.prj' }
      ],
      returnObj: {
        files: [
          { name: 'test.shp' },
          { name: 'test.dbf' },
          { name: 'test.prj' }
        ],
        shapefiles: {
          'shp': null,
          'dbf': null,
          'prj': null
        }
      }
    },
    {
      filename: 'tester',
      files: [
        { name: 'tester.shp' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      returnObj: {
        files: [
          { name: 'test.prj' },
          { name: 'test.geojson' }
        ],
        shapefiles: {
          'shp': { name: 'tester.shp' },
          'dbf': null,
          'prj': null
        }
      }
    }
  ]
  for (const testCase of testCasesShapefiles) {
    it('Finds all shapefiles', () => {
      const returnObj = Importer.findShapefiles(testCase.files, testCase.filename)
      // expect(Importer.findShapefiles).toHaveBeenCalledTimes(4)
      expect(returnObj).toMatchObject(testCase.returnObj)
    })
  }

  const testCaseFiles = [
    {
      files: [
        { name: 'test.dbf' },
        { name: 'test.shp' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      groupedFileCount: 2
    },
    {
      files: [
        { name: 'test.shp' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      groupedFileCount: 2
    },
    {
      files: [
        { name: 'test.dbf' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      groupedFileCount: 2
    },
    {
      files: [
        { name: 'testo.shp' },
        { name: 'test.dbf' },
        { name: 'test.geojson' }
      ],
      groupedFileCount: 3
    },
    {
      files: [
        { name: 'test.shp' },
        { name: 'test.dbf' },
        { name: 'test.prj' }
      ],
      groupedFileCount: 1
    },
    {
      files: [
        { name: 'tester.geojson' },
        { name: 'testo.kml' },
        { name: 'tester.shp' },
        { name: 'myfile.csv' },
        { name: 'test.prj' },
        { name: 'test.geojson' }
      ],
      groupedFileCount: 6
    }
  ]

  for (const testCase of testCaseFiles) {
    it('Group required files together', () => {
      const returnVal = Importer.groupFiles(testCase.files)
      expect(returnVal.length).toBe(testCase.groupedFileCount)
    })
  }
})
