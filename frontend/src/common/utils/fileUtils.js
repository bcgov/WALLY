export function getFileExtension (filename) {
  if (!filename || !filename.length) {
    // basic check for validity before trying to parse filename
    console.warn(`invalid filename ${filename}`)
    return null
  }

  const filenameParts = filename.split('.')

  if (filenameParts.length === 1) {
    console.warn(`invalid filename ${filename}`)
    return null
  }
  return filenameParts[filenameParts.length - 1]
}
