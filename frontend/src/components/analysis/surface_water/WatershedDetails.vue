<template>
  <v-card flat>
    <v-card-text>
      <v-dialog v-model="show.editingModelInputs" persistent>
        <EditableModelInputs
          @close="closeEditableModelInputsDialog"/>
      </v-dialog>
      <v-row v-if="customModelInputsActive">
        <v-col>
          <v-alert
            outlined
            type="warning"
            prominent
            border="left"
          >
            <p>
              You are using custom model inputs and not the values supplied by the
              Wally API.
            </p>
          </v-alert>
        </v-col>
      </v-row>
      <v-row v-if="modelOutputs && modelOutputs.sourceDescription">
        <v-alert tile color="" dense class="ma-3" width="100%" text>
          {{ modelOutputs.sourceDescription }}
        </v-alert>
        <ModelExplanations/>
      </v-row>

      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Drainage area
              <Dialog v-bind="wmd.drainageArea" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="watershedDetails.drainage_area">
                {{ watershedDetails.drainage_area.toFixed(2) }}
                <strong>km²</strong>
              </span>
              <span v-else>
                {{ noValueText }}
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card flat >
            <v-card-title>
              Mean Annual Discharge
              <Dialog v-bind="wmd.meanAnnualDischarge" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="modelOutputs.mad">
                {{ modelOutputs.mad }}
                <strong>m³/s</strong>
              </span>
              <span v-else>
                {{ noValueText }}
              </span>
            </v-card-text>
          </v-card>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
          <v-card flat >
            <v-card-title>
              Total Annual Quantity
              <Dialog v-bind="wmd.totalAnnualQuantity" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="availabilityPlotData">
                {{ this.availabilityPlotData.reduce((a, b) => a + b, 0)
                                            .toLocaleString('en', {maximumFractionDigits: 0}) }}
                <strong>m³</strong>
              </span>
              <span v-else>
                {{ noValueText }}
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col>
        <v-card flat >
          <v-card-title>
            Mean Annual Runoff
            <Dialog v-bind="wmd.meanAnnualRunoff" smallIcon/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.mar">
              {{ modelOutputs.mar }}
              <strong>
                l/s/km²
              </strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
          <v-card flat>
            <v-card-title>
              Low7Q2
              <Dialog v-bind="wmd.low7Q2" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="modelOutputs.low7q2">
                {{ modelOutputs.low7q2 }}
                <strong>m³</strong>
              </span>
              <span v-else>{{ noValueText }}</span>
            </v-card-text>
          </v-card>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
          <v-card flat >
            <v-card-title>
              Dry7Q10
              <Dialog v-bind="wmd.dry7Q10" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="modelOutputs.dry7q10">
                {{ modelOutputs.dry7q10 }}
                <strong>m³/s</strong>
              </span>
              <span v-else>{{ noValueText }}</span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col>
          <v-card flat>
            <v-card-title>
              Annual Precipitation
              <Dialog v-bind="wmd.annualPrecipitation" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="watershedDetails.annual_precipitation">
                {{ watershedDetails.annual_precipitation.toFixed(0) }}
                <strong>mm</strong>
              </span>
              <span v-else>{{ noValueText }}</span>
            </v-card-text>
          </v-card>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
          <v-card flat >
            <v-card-title>
              Glacial Coverage
              <Dialog v-bind="wmd.glacialCoverage" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="watershedDetails.glacial_coverage">
                {{ watershedDetails.glacial_coverage.toFixed(2) }}
              </span>
              <span v-else>{{ noValueText }}</span>
            </v-card-text>
          </v-card>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
          <v-card flat >
            <v-card-title>
              Median Elevation
              <Dialog v-bind="wmd.medianElevation" smallIcon/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="watershedDetails.median_elevation">
                {{ watershedDetails.median_elevation.toFixed(0) }}
                <strong>mASL</strong>
              </span>
              <span v-else>{{ noValueText }}</span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-card-actions>
          <v-tooltip bottom v-if="this.scsb2016ModelInputs" smallIcon>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" small depressed light @click="openEditableModelInputsDialog">
                <v-icon small color="primary">
                  mdi-tune
                </v-icon>
                Model Inputs
              </v-btn>
            </template>
            <span>Customize model inputs</span>
          </v-tooltip>
        </v-card-actions>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'

import Dialog from '../../common/Dialog'
import { WatershedModelDescriptions } from '../../../constants/descriptions'
import ModelExplanations from './ModelExplanations'
import EditableModelInputs from './EditableModelInputs'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { scaleImageToFit } from '../../../common/helpers'

export default {
  name: 'WatershedDetails',
  components: {
    Dialog,
    ModelExplanations,
    EditableModelInputs
  },
  props: ['modelOutputs', 'watershedName'],
  data: () => ({
    watershedLoading: false,
    error: null,
    noValueText: 'No info available',
    wmd: WatershedModelDescriptions,
    show: {
      editingModelInputs: false
    }
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['availabilityPlotData', 'watershedDetails', 'customModelInputsActive',
      'scsb2016ModelInputs'])
  },
  methods: {
    openEditableModelInputsDialog () {
      this.show.editingModelInputs = true
    },
    closeEditableModelInputsDialog () {
      this.show.editingModelInputs = false
    },
    downloadWatershedInfo () {
      // currently unused; to be updated and re-enabled.
      // See JIRA ticket WATER-1951.
      // see commit 46e3623097384b6cd709ff8e58f7bd22201c9b30 for the removed button code.

      console.log('download watershed')
      const doc = jsPDF('p', 'in', [230, 200])
      const width = doc.internal.pageSize.getWidth()
      const height = doc.internal.pageSize.getHeight()
      const filename = 'watershed--'.concat(this.watershedName) +
        '--'.concat(new Date().toISOString()) + '.pdf'

      const watershedContainers = [...document.getElementsByClassName('watershedInfo')]

      const myPromises = []
      watershedContainers.forEach((container) => {
        myPromises.push(
          html2canvas(container)
            .then(canvas => {
              const img = canvas.toDataURL('image/png')
              const imgProps = doc.getImageProperties(img)
              const size = scaleImageToFit(width, height, imgProps.width,
                imgProps.height)
              doc.addImage(img, 'PNG', 0, 0, size[0], size[1])
              doc.addPage()
            })
        )
      })

      // Save file and download
      Promise.all(myPromises).then(() => {
        doc.save(filename)
      })
    }
  },
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>
