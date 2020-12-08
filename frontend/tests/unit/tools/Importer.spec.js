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
