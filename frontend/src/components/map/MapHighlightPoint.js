export default (map, size) => {
  return {
    width: size,
    height: size,
    data: new Uint8Array(size * size * 4),

    onAdd: function () {
      var canvas = document.createElement('canvas')
      canvas.width = this.width
      canvas.height = this.height
      this.context = canvas.getContext('2d')
    },

    render: function () {
      var duration = 1750
      var t = (performance.now() % duration) / duration

      var radius = size / 2 * 0.3
      var outerRadius = size / 2 * 0.5 * t + radius
      var context = this.context

      // draw outer circle
      context.clearRect(0, 0, this.width, this.height)
      context.beginPath()
      context.arc(this.width / 2, this.height / 2, outerRadius, 0, Math.PI * 2)
      context.fillStyle = 'rgba(243, 255, 255,' + (1 - t) + ')'
      context.fill()

      // draw inner circle
      context.beginPath()
      context.arc(this.width / 2, this.height / 2, radius, 0, Math.PI * 2)
      context.fillStyle = 'rgba(0, 173, 252, 0.2)'
      context.strokeStyle = 'white'
      context.lineWidth = 2 + 4 * (1 - t)
      context.fill()
      context.stroke()

      // update this image's data with data from the canvas
      this.data = context.getImageData(0, 0, this.width, this.height).data

      // keep the map repainting
      map.triggerRepaint()

      // return `true` to let the map know that the image was updated
      return true
    }
  }
}
