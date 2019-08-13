import {HYDROMETRIC_STREAM_FLOW} from "./metadataUtils"

export const dataMarts = {
  'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV': {
    id: 1,
    name: 'Water Rights',
    description: '',
    source_url: '',
    data_format: '',
    last_updated: '',
    time_relevance: '',
    field_names: [],
    field_descriptions: [],
    highlight_fields: {
      label: 'Water Quantity',
      data_labels: ['LICENCE_NUMBER'],
      datasets: ['QUANTITY']
    }
  },
  'HYDROMETRIC_STREAM_FLOW': {
    id: 2,
    name: 'Hydrometric Stream Flow',
    description: '',
    source_url: '',
    data_format: '',
    last_updated: '',
    time_relevance: '',
    field_names: [],
    field_descriptions: [],
    highlight_fields: {
      label: 'Flow Levels',
      data_labels: ['monthly_mean'],
      datasets: ['month']
    }
  }
}
