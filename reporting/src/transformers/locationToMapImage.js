import axios from "axios"
import StaticMaps from "staticmaps"

class Map {
    constructor(bbox, featureCollections = []) {
        this.bbox = bbox
        this.featureCollections = featureCollections
    }

    async png() {
        const map = new StaticMaps({
            width: 550,
            height: 300,
            paddingX: 20,
            paddingY: 20,
            tileUrl: "https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/{z}/{y}/{x}"
        });

        const coords = [[-123.04058,49.278113],[-123.040857,49.278978],[-123.042315,49.281739],[-123.042387,49.283511],[-123.041513,49.28518],[-123.040631,49.286026],[-123.038774,49.287011],[-123.03646,49.287444],[-123.0352,49.287444],[-123.032646,49.287108],[-123.025238,49.285765],[-123.022156,49.285563],[-123.012305,49.283824],[-123.010288,49.283793],[-123.00416,49.284792],[-123.000926,49.28499],[-122.999347,49.284913],[-122.998406,49.28467],[-122.995035,49.283132],[-122.990788,49.280874],[-122.989526,49.280469],[-122.987276,49.280095],[-122.97812,49.279815],[-122.970288,49.279831],[-122.959312,49.280274],[-122.956144,49.279944],[-122.95274,49.2788],[-122.951494,49.278113],[-123.04058,49.278113]]

        const polygon = {
            coords: coords,
            color: '#0000FFBB',
            width: 3
          };
        
        map.addPolygon(polygon);

        // render map and return as a promise that resolves a Buffer.
        // the calling function can use await map.png() to use the buffer.
        return await map.render().then(() => {
            return map.image.buffer('image/png')
        })
    }
}

export default Map;
