import vuetify from '@/plugins/vuetify'

import Header from '../../components/Header'

export default {
  title: 'wally/Header',
  component: Header
}

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { Header },
  template:
    '<Header :appInfo="user" />'
})

export const Production = Template.bind({})
Production.args = {
  wally_env: 'PROD'
}

export const Development = Template.bind({})
Development.args = {
  wally_env: 'DEV'
}

export const Staging = Template.bind({})
Staging.args = {
  wally_env: 'DEV'
}

// Template.decorators = [() =>{}]
