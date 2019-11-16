<template>
  <v-container class="pa-0 ma-0">
    <v-card outlined>
      <v-card-text class="grey--text text--darken-4">
        <dl>
          <dt>
            Nearest community
          </dt>
          <dd></dd>
        </dl>
        <div class="subtitle-1 mt-5">Treaty areas</div>
        <dl>
          <dt>Within treaty area</dt>
          <dd></dd>
          <dt>Nearest treaty area</dt>
          <dd></dd>
        </dl>
        <div class="subtitle-1 mt-5">Treaty lands</div>
        <dl>
          <dt>Within treaty lands</dt>
          <dd></dd>
          <dt>Nearest treaty lands</dt>
          <dd></dd>
        </dl>
      </v-card-text>

    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'FirstNationsContactsNearby',
  props: ['record'],
  data: () => ({

  })
}
</script>

<style>

</style>
