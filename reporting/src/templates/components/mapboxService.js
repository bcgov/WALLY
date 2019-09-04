import axios from "axios"
import StaticMaps from "staticmaps"
import geoViewport from '@mapbox/geo-viewport';

class MapboxAPI {
    constructor() {
    }

    bboxToViewport(bbox = [], imageSize = []) {
        if (bbox.length !== 4) {
            throw "bbox invalid: must be an array of 4 numbers"
        }
        if (imageSize.length !== 2) {
            throw "image size must be an array: [w, h] e.g. [640, 480]"
        }

        return geoViewport.viewport(bbox, imageSize)
    }

    async staticPNG(lnglat = [], zoom, w, h) {

        const token = process.env.MAPBOX_ACCESS_KEY || ''

        // the url needs to contain the style identifier (e.g. mapbox/streets-v1 or username/styleID),
        // and the longitude, latitude, zoom level, bearing, pitch, and image size (width and height)
        // @2x indicates that the image dimensions should be doubled, which helps with rendering quality.
        // https://docs.mapbox.com/help/glossary/static-images-api/
        const url = `
        https://api.mapbox.com/styles/v1/stephenhillier/cjzydtam02lbd1cld4jbkqlhy/static/${lnglat[0]},${lnglat[1]},${zoom},0.00,0.00/${w}x${h}@2x?access_token=${token}
        `

        // return a promise for a PNG image buffer. This can be used with the React-PDF Image component: <Image src={buffer}></Image>
        return await axios({
            url: url,
            method: 'get',
            responseType: 'arraybuffer'
        }).then((res) => {
            return { data: new Buffer.from(res.data), format: 'png' }
        }).catch((err) => {
            console.log(err)
            return Promise.reject(err)
        })
    }
}

export default MapboxAPI;
