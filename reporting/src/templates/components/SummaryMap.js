import axios from "axios"
import StaticMaps from "staticmaps"
import geoViewport from '@mapbox/geo-viewport';

class SummaryMap {
    constructor() {
        this.map = new StaticMaps({
            width: 1100,
            height: 600,
            paddingX: 10,
            paddingY: 10,
            tileUrl: "https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/{z}/{y}/{x}"
        });
    }

    addPolygon(options = { coords: [[]], color: '#0000FFBB', width: 2}) {
        console.log(`adding polygon with color ${options.color}`)
        this.map.addLine(options)
    }

    addMarker(args = { coords: []}) {
        const options = {}
        const img = `https://cdnjs.cloudflare.com/ajax/libs/open-iconic/1.1.1/png/media-record.png`
        options.img = img
        options.width = 8
        options.height = 8
        options.offsetX = 4
        options.offsetY = 4
        options.coord = args.coords // the underlying library (staticmaps uses singular here)
                
        this.map.addMarker(options)
    }

    withWatersheds(watersheds) {
        // iterate through watersheds (checking first that watersheds were included in the map layer data),
        // adding a polygon for each watershed.
        watersheds && watersheds.geojson.features && watersheds.geojson.features.forEach((f, i) => {
            if (i > 10) return; // temporary: limit number of polygons drawn
            console.log('watershed', i)
            f.geometry.coordinates.forEach((c) => {
                this.map.addPolygon({
                    coords: c,
                    color: '#0000FFBB',
                    width: 1
                })
            })

        })
    }

    withAquifers(aquifers) {
        aquifers && aquifers.geojson.features && aquifers.geojson.features.forEach((f, i) => {
            console.log('aquifer', i)
            if (i !== 1) return; // temporary: limit number of polygons drawn
            f.geometry.coordinates.forEach((c) => {
                this.map.addPolygon({
                    coords: c,
                    color: '#FF4500BB',
                    width: 2
                })
            })
    
        })
    }

    withLicences(licences) {
        licences && licences.geojson.features && licences.geojson.features.forEach((f, i) => {
            this.addMarker({coords: f.geometry.coordinates})
        })
    }

    async png() {
        // render map and return as a promise that resolves a Buffer.
        // the calling function can use await map.png() to use the buffer.
        return await this.map.render().then(() => {
            return this.map.image.buffer('image/png')
        })
    }

    async mbPng(lng, lat, zoom, w, h) {

        // temporary public token for t esting.
        const token = `pk.eyJ1Ijoic3RlcGhlbmhpbGxpZXIiLCJhIjoiY2p6encxamxnMjJldjNjbWxweGthcHFneCJ9.y5h99E-kHzFQ7hywIavY-w`
        let url = `
        https://api.mapbox.com/styles/v1/stephenhillier/cjzydtam02lbd1cld4jbkqlhy/static/${lng},${lat},${zoom},0.00,0.00/${w}x${h}@2x?access_token=${token}
        `
        console.log(url)
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

export default SummaryMap;
