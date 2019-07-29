import colors from '../src/styles/colors'
import {shortMonthNames,fullMonthNames} from '../src/styles/labels'
import _ from 'lodash'

test('colors are not empty', () => {
    expect(_.isEmpty(colors)).toBe(false)
})

test('year labels should have 12 months', () => {
    expect(shortMonthNames.length).toBe(12)
    expect(fullMonthNames.length).toBe(12)
})
