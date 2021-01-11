// import vuetify from '@/plugins/vuetify';
// import vuetify from '../../plugins/vuetify'
import Header from '../../components/Header'

export default {
  title: 'wally/Header',
  component: Header
}

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { Header },
  template:
    '<Header :appInfo="appInfo" />'
  // decorators: vuetify
})

export const Production = Template.bind({})
Production.args = {
  appInfo: {
    wally_env: 'production'
  }
}

export const Development = Template.bind({})
Development.args = {
  appInfo: {
    wally_env: 'DEV'
  }
}

export const Staging = Template.bind({})
Staging.args = {
  appInfo: {
    wally_env: 'Staging'
  }
}

// Template.
// Template.decorators = [() =>{}]
