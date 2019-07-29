import axios from "axios";

export default async (latlng, radius = 0.5) => {
    let url = 'http://maps.gov.bc.ca/arcserver/services/province/roads_wm/MapServer/WMSServer?REQUEST=GetMap' +
        '&SERVICE=WMS&SRS=EPSG:4326&STYLES=&VERSION=1.1.1&LAYERS=0&FORMAT=image%2Fpng&HEIGHT=600&WIDTH=887&BBOX=' +
        (latlng[1] - radius) + ',' + (latlng[0] - radius) + ',' + (latlng[1] + radius) + ',' + (latlng[0] + radius)

    return await axios({
        url: url,
        method: 'get',
        responseType: 'arraybuffer'
    }).then((res) => {
        return { data: new Buffer.from(res.data), format: 'png' }
    }).catch((err) => {
        return Promise.reject(err)
    })
}
