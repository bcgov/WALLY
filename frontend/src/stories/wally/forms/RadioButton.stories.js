// import vuetify from '@/plugins/vuetify';
// import vuetify from '../../plugins/vuetify'
import RadioButton from '@/stories/wally/forms/RadioButton'

export default {
  title: 'wally/Forms/RadioButton',
  component: RadioButton,
  argTypes: {
    backgroundColor: { control: 'color' },
    size: { control: { type: 'select', options: ['small', 'medium', 'large'] } }
  }
}

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { RadioButton },
  template:
    '<RadioButton v-bind="$props" />'
  // decorators: vuetify
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
  primary: true,
  optionsCount: 4
}
