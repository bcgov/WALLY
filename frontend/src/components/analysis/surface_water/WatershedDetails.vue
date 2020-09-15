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
      <v-row>
        <v-alert tile color="" dense class="ma-3" width="100%" text
          v-if="modelOutputs && modelOutputs.sourceDescription">
          {{ modelOutputs.sourceDescription }}
        </v-alert>
        <ModelExplanations/>
      </v-row>

      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Drainage area
              <Dialog v-bind="wmd.drainageArea"/>
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
        <v-card flat >
          <v-card-title>
            Mean Annual Discharge
            <Dialog v-bind="wmd.meanAnnualDischarge"/>
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
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Total Annual Quantity
            <Dialog v-bind="wmd.totalAnnualQuantity"/>
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
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Runoff
            <Dialog v-bind="wmd.meanAnnualRunoff"/>
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
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Low7Q2
            <Dialog v-bind="wmd.low7Q2"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.low7q2">
              {{ modelOutputs.low7q2 }}
              <strong>m³</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Dry7Q10
            <Dialog v-bind="wmd.dry7Q10"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.dry7q10">
              {{ modelOutputs.dry7q10 }}
              <strong>m³/s</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Annual Precipitation
            <Dialog v-bind="wmd.annualPrecipitation"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.annual_precipitation">
              {{ watershedDetails.annual_precipitation.toFixed(0) }}
              <strong>mm</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Glacial Coverage
            <Dialog v-bind="wmd.glacialCoverage"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.glacial_coverage">
              {{ watershedDetails.glacial_coverage.toFixed(2) }}
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Median Elevation
            <Dialog v-bind="wmd.medianElevation"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.median_elevation">
              {{ watershedDetails.median_elevation.toFixed(0) }}
              <strong>mASL</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
      </v-row>
      <v-row>
        <v-card-actions>
          <v-tooltip bottom v-if="this.scsb2016ModelInputs">
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
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" small depressed light @click="openEditableModelInputsDialog">
                <v-icon small color="primary">
                  cloud_download
                </v-icon>
                Download Watershed Info
              </v-btn>
            </template>
            <span>Download Watershed Info</span>
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
import jsPDF from "jspdf"
import html2canvas from "html2canvas"

export default {
  name: 'WatershedDetails',
  components: {
    Dialog,
    ModelExplanations,
    EditableModelInputs
  },
  props: ['modelOutputs'],
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
      let doc = jsPDF('p', 'in', [230, 200])
      let width = doc.internal.pageSize.getWidth()
      let height = doc.internal.pageSize.getHeight()
      let filename = 'watershed--'.concat(this.watershedName) +
        '--'.concat(new Date().toISOString()) + '.pdf'

      let watershedContainers = [...document.getElementsByClassName('watershedInfo')]

      let myPromises = []
      watershedContainers.forEach((container) => {
        myPromises.push(
          html2canvas(container)
            .then(canvas => {
              let img = canvas.toDataURL('image/png')
              const imgProps = doc.getImageProperties(img)
              let size = this.scaleImageToFit(width, height, imgProps.width,
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
    },
  },
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>
