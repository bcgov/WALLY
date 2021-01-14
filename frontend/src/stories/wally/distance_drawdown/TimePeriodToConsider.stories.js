import TimePeriodToConsider from '@/stories/wally/distance_drawdown/TimePeriodToConsider'
export default {
  title: 'wally/DistanceDrawdown/TimePeriodToConsider',
  component: TimePeriodToConsider,
  argTypes: {
  }
}

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { TimePeriodToConsider },
  template:
    '<TimePeriodToConsider v-bind="$props" />'
})

// export const Production = Template.bind({})
// Production.args = {
//   appInfo: {
//     wally_env: 'production'
//   }
// }
//
// export const Development = Template.bind({})
// Development.args = {
//   appInfo: {
//     wally_env: 'DEV'
//   }
// }
//
// export const Staging = Template.bind({})
// Staging.args = {
//   appInfo: {
//     wally_env: 'Staging'
//   }
// }

// Template.
// Template.decorators = [() =>{}]

export const Primary = Template.bind({})
Primary.args = {
  primary: true
}
