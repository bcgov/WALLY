<template>
  <InfoSheet :width=panelWidth panelName="Analysis">
  <router-view>
  </router-view>
  </InfoSheet>
</template>
<script>
  import InfoSheet from '../common/InfoSheet'
export default {
  name: 'Analysis',
  components: {
    InfoSheet
  },
  data: () => {
    return {
      panelWidth: 1000
    }
  }
}
</script>
