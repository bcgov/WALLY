export const daysInMonth = { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31 }
export const secondsInDay = 86400
export const secondsInYear = 31536000

export const secondsInMonth = (month, leapYear = false) => {
  let seconds = daysInMonth[month] * secondsInDay
  if (month === 2 && leapYear) {
    seconds += secondsInDay
  }
  return seconds
}
