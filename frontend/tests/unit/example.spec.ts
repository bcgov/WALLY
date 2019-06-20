import { shallowMount } from '@vue/test-utils';
import Home from '@/views/Home.vue';

describe('Home.vue', () => {
  it('renders props.msg when passed', () => {
    const testMsg = 'new message';
    const wrapper = shallowMount(Home);
    wrapper.setData({
      msg: testMsg,
    });
    expect(wrapper.text()).toMatch(testMsg);
  });
});
