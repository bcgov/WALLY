import axios from "axios";

export default async (bbox) => {
    let url = 'http://maps.gov.bc.ca/arcserver/services/province/roads_wm/MapServer/WMSServer?REQUEST=GetMap' +
        '&SERVICE=WMS&SRS=EPSG:4326&STYLES=&VERSION=1.1.1&LAYERS=0&FORMAT=image%2Fpng&HEIGHT=600&WIDTH=600&BBOX=' +
        bbox[0] + ',' + bbox[1] + ',' + bbox[2] + ',' + bbox[3]

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
