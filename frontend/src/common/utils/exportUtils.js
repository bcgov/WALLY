const XLSX_FILE_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
const ZIP_FILE_TYPE = 'application/zip'

export function downloadXlsx (r, defaultFilename) {
  global.config.debug && console.log('[wally]', r)
  let filename = defaultFilename

  // default filename, and inspect response header Content-Disposition
  // for a more specific filename (if provided).
  const filenameData = r.headers['content-disposition'] && r.headers['content-disposition'].split('filename=')
  if (filenameData && filenameData.length === 2) {
    filename = filenameData[1]
  }

  // TODO: Refactor code duplication
  const blob = new Blob([r.data], { type: XLSX_FILE_TYPE })
  const link = document.createElement('a')
  link.href = window.URL.createObjectURL(blob)
  link.download = filename
  document.body.appendChild(link)
  link.click()
  setTimeout(() => {
    document.body.removeChild(link)
    window.URL.revokeObjectURL(link.href)
  }, 0)
}

export function downloadZip (r, defaultFilename) {
  global.config.debug && console.log('[wally]', r)
  let filename = defaultFilename

  // default filename, and inspect response header Content-Disposition
  // for a more specific filename (if provided).
  const filenameData = r.headers['content-disposition'] && r.headers['content-disposition'].split('filename=')
  if (filenameData && filenameData.length === 2) {
    filename = filenameData[1]
  }

  const blob = new Blob([r.data], { type: ZIP_FILE_TYPE })
  const link = document.createElement('a')
  link.href = window.URL.createObjectURL(blob)
  link.download = filename
  document.body.appendChild(link)
  link.click()
  setTimeout(() => {
    document.body.removeChild(link)
    window.URL.revokeObjectURL(link.href)
  }, 0)
}

export function downloadFile (r, defaultFilename, zip = false) {
  global.config.debug && console.log('[wally]', r)
  let filename = defaultFilename

  // default filename, and inspect response header Content-Disposition
  // for a more specific filename (if provided).
  const filenameData = r.headers['content-disposition'] && r.headers['content-disposition'].split('filename=')
  if (filenameData && filenameData.length === 2) {
    filename = filenameData[1]
  }

  const blob = zip ? new Blob([r.data], { type: 'application/zip' }) : new Blob([r.data])
  const link = document.createElement('a')
  link.href = window.URL.createObjectURL(blob)
  link.download = filename
  document.body.appendChild(link)
  link.click()
  setTimeout(() => {
    document.body.removeChild(link)
    window.URL.revokeObjectURL(link.href)
  }, 0)
}
