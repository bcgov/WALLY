import { getFileExtension } from '../../../src/common/utils/fileUtils'

describe('File utils', () => {
  beforeEach(function () {
    console.warn = jest.fn()
  })

  it('Returns the file extension', () => {
    expect(getFileExtension('test.hello')).toBe('hello')
    expect(getFileExtension('test')).toBe(null)
    expect(getFileExtension('test.hello.world')).toBe('world')
    expect(getFileExtension(null)).toBe(null)
  })
})
