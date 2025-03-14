export const dataMarts = {
  'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV': {
    id: 1,
    name: 'Water Rights',
    type: 'wms',
    description: '',
    source_url: '',
    data_format: '',
    last_updated: '',
    time_relevance: '',
    field_names: [],
    field_descriptions: [],
    highlight_fields: {
      // possibly scrap this
      label: 'Water Quantity',
      data_labels: ['LICENCE_NUMBER'],
      datasets: ['QUANTITY']
    },
    context: [
      {
        id: 1,
        type: 'chart',
        data: {
          type: 'bar', // combo, line, pie, etc
          label: 'Water Quantity',
          datasets_labels: ['Water Quantity'],
          label_key: 'LICENCE_NUMBER',
          datasets_key: ['QUANTITY']
        }
      },
      {
        id: 2,
        type: 'image',
        source: 'https://cdn.vuetifyjs.com/images/cards/desert.jpg'
      },
      {
        id: 3,
        type: 'card',
        title: 'Hatch Creek Ranch',
        description: 'Maximum licensed demand for purpose, multiple PODs, ' +
                     'quantity at each POD unknown'
      }
    ]
  },
  HYDROMETRIC_STREAM_FLOW: {
    id: 2,
    name: 'Hydrometric Stream Flow',
    type: 'api',
    description: '',
    source_url: '',
    data_format: '',
    last_updated: '',
    time_relevance: '',
    field_names: [],
    field_descriptions: [],
    highlight_fields: {
      label: 'Flow Levels',
      data_labels: ['month'],
      datasets: ['monthly_mean']
    },
    context: [
      {
        id: 1,
        type: 'title',
        data: 'Hydrometric Stream Flow'

      },
      {
        id: 2,
        type: 'link',
        name: 'Link to the data',
        description: 'Sample description',
        url: 'http://www.gov.bc.ca'
      },
      {
        id: 3,
        type: 'chart',
        data: {
          type: 'line',
          label: 'Flows',
          data_labels: ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
              label: 'Min',
              data: [5, 6, 3, 5, 3, 1, 2, 4, 5, 1, 2, 3, 5]
            },
            {
              label: 'Max',
              data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 54]
            },
            {
              label: 'Mean',
              data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 54]
            }
          ]
        }
      },
      {
        id: 4,
        type: 'chart',
        data: {
          type: 'bar',
          label: 'Levels',
          data_labels: ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
              label: 'Min',
              data: [5, 6, 3, 5, 3, 1, 2, 4, 5, 1, 2, 3, 5]
            },
            {
              label: 'Max',
              data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 54]
            },
            {
              label: 'Mean',
              data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 54]
            }
          ]
        }
      },
      {
        id: 5,
        type: 'chart',
        data: {
          type: 'area_dataset',
          label: 'Flows',
          data_labels: ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
              label: 'Min',
              data: [5, 6, 3, 5, 3, 1, 2, 4, 5, 1, 2, 3, 5]
            },
            {
              label: 'Max',
              data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 54]
            },
            {
              label: 'Mean',
              data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 54]
            }
          ]
        }
      }
    ]
  }
}
