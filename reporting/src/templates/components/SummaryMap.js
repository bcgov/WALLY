import axios from "axios"
import StaticMaps from "staticmaps"

class SummaryMap {
    constructor() {
        this.map = new StaticMaps({
            width: 550,
            height: 300,
            paddingX: 10,
            paddingY: 10,
            tileUrl: "https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/{z}/{y}/{x}"
        });
    }

    addPolygon(options = { coords: [[]], color: '#0000FFBB', width: 2}) {
        this.map.addPolygon(options)
    }

    async png() {
        // render map and return as a promise that resolves a Buffer.
        // the calling function can use await map.png() to use the buffer.
        return await this.map.render().then(() => {
            return this.map.image.buffer('image/png')
        })
    }
}

export default SummaryMap;
