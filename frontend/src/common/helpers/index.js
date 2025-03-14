// Splits snake case field names into separate words and
// capitalizes first letter of each word
export function humanReadable (str) {
  if (str == null || typeof str === 'number') { return }
  const frags = str.split('_')
  for (let i = 0; i < frags.length; i++) {
    frags[i] = frags[i].toLowerCase()
    if (i === 0) {
      frags[i] = frags[i].charAt(0).toUpperCase() + frags[i].slice(1)
    }
  }
  return frags.join(' ')
}

export function getArrayDepth (value) {
  return Array.isArray(value) ? 1 + Math.max(...value.map(getArrayDepth)) : 0
}

export function scaleImageToFit (ws, hs, wi, hi) {
  const ri = wi / hi
  const rs = ws / hs
  return rs > ri ? [wi * hs / hi, hs] : [ws, hi * ws / wi]
}
