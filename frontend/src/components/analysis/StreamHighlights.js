export default (map) => {
    var featureCollection = {
        "type": "FeatureCollection",
        "features": []
    };

    map.on('load', function() {
        // Add the streams vector layer as a source dataset
        map.addSource('fwa_streams_data', {
            "type": "vector",
            "url": "mapbox://iit-water.6ihj1ke0"
        });
        map.addLayer({
            "id": "streams",
            "type": "line",
            "source": "fwa_streams_data",
            "source-layer": "FWA_STREAM_NETWORKS_SP-bdhkfq",
            "paint": {
                "line-color": "#4C4CFF"
            }
        });

        this.map.addSource('upstreamSource', { type: 'geojson', data: featureCollection })
        map.addLayer({
            "id": "upstream",
            "type": "line",
            "source": "upstreamSource",
            "paint": {
                "line-color": "#CE0000"
            }
        });

        this.map.addSource('downstreamSource', { type: 'geojson', data: featureCollection }) 
        map.addLayer({
            "id": "downstream",
            "type": "line",
            "source": "downstreamSource",
            "paint": {
                "line-color": "#000063"
            }
        });
         
        map.on('mousemove', 'streams', function(e) {
            // Change the cursor style as a UI indicator.
            map.getCanvas().style.cursor = 'pointer';
            
            // Single out the first found feature.cc
            var hoveredStreamSegment = e.features[0];
            
            // Query the counties layer visible in the map. Use the filter
            // param to only collect results that share the same county name.
            // var relatedFeatures = map.querySourceFeatures('fwa_streams_data', {
            //     sourceLayer: 'FWA_STREAM_NETWORKS_SP-bdhkfq',
            //     filter: ['in', 'FWA_WATERSHED_CODE', feature.properties.FWA_WATERSHED_CODE]
            // });

            var streams = map.querySourceFeatures('fwa_streams_data', {
                sourceLayer: 'FWA_STREAM_NETWORKS_SP-bdhkfq'
            });
            var upstreamFeatures = streams.filter((s) => {
                return s.properties["FWA_WATERSHED_CODE"]
                    .includes(hoveredStreamSegment.properties["FWA_WATERSHED_CODE"])
            })
            var streamCollection = Object.assign({}, featureCollection)
            streamCollection["features"] = upstreamFeatures
            map.getSource('upstreamSource').setData(streamCollection)
            // var downstreams = streams.filter((s) => {
            //     return s.properties["FWA_WATERSHED_CODE"]
            //         .includes(hoveredStreamSegment.properties["FWA_WATERSHED_CODE"])
            // })
            
            // // Render found features in an overlay.
            // overlay.innerHTML = '';
            
            // Total the population of all features
            // var populationSum = relatedFeatures.reduce(function(memo, feature) {
            //     return memo + feature.properties.population;
            // }, 0);
            
            // var title = document.createElement('strong');
            // title.textContent = feature.properties.COUNTY + ' (' + relatedFeatures.length + ' found)';
            
            // var population = document.createElement('div');
            // population.textContent = 'Total population: ' + populationSum.toLocaleString();
            
            // overlay.appendChild(title);
            // overlay.appendChild(population);
            // overlay.style.display = 'block';
            
            // Add features that share the same county name to the highlighted layer.
            // map.setFilter('counties-highlighted', ['in', 'COUNTY', feature.properties.COUNTY]);
            
            // Display a popup with the name of the county
            // popup.setLngLat(e.lngLat)
            // .setText(feature.properties.COUNTY)
            // .addTo(map);
        });
         
        map.on('mouseleave', 'streams', function() {
            map.getSource('upstreamSource').setData(geojson)
            map.getCanvas().style.cursor = '';
            // popup.remove();
            // map.setFilter('counties-highlighted', ['in', 'COUNTY', '']);
            // overlay.style.display = 'none';
        });
    });
}
  