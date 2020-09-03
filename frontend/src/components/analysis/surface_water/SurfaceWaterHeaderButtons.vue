<template>
  <v-row>
    <v-col>
      <v-btn-toggle>
        <v-btn outlined small
               color="primary" class="">
            <span class="hidden-sm-and-down">
            See on map
            </span>
        </v-btn>
        <v-menu bottom right>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              small
              dark
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>layers</v-icon>
            </v-btn>
          </template>
          <v-card class="pa-5">
            <v-checkbox small label="Hydrometric Stations" class="mt-0"/>
            <v-checkbox small label="Water Rights Applications" class="mt-0"/>
            <v-checkbox small label="Water Rights Licences" class="mt-0"/>
            <v-checkbox small label="Known BC Fish Observations & Distributions" class="mt-0"/>
            <v-checkbox small label="Water Approval Points" class="mt-0"/>
          </v-card>
        </v-menu>

      </v-btn-toggle>
    </v-col>
    <v-col>
    </v-col>
    <v-col class="text-right">
      <v-btn-toggle>
        <v-btn outlined small
               color="primary" class="">
            <span class="hidden-sm-and-down">
            Export
            </span>
        </v-btn>
        <v-menu bottom right>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              small
              dark
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>expand_more</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>
                PDF
                <v-icon class="ml-1">cloud_download</v-icon>
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>
                Excel
                <v-icon class="ml-1">cloud_download</v-icon>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

      </v-btn-toggle>
      <v-btn outlined small color="primary" class="ml-1"
             v-on:click="$emit('reset-watershed')">
        <v-icon small>refresh</v-icon>
        Reset
      </v-btn>
    </v-col>
  </v-row>
</template>
<script>
export default {
  name: 'SurfaceWaterHeaderButtons'
}
</script>
