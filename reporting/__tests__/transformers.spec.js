import locationToMapImage from '../src/transformers/locationToMapImage'
import _ from "lodash";

test('locationToMapImage returns a buffer', async () => {
    let image = await locationToMapImage([-123.213,48.3432])
    expect(_.size(image)).toBe(2)
    expect(Buffer.isBuffer(image.data)).toBe(true)
})
