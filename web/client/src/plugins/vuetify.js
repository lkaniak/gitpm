import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import colors from 'vuetify/es5/util/colors';

Vue.use(Vuetify, {
  theme: {
    primary: {
      base: '#00BCD4',
      darken1: colors.purple.darken2,
    },
    secondary: '#B2EBF2',
    tertiary: '#3056bf',
    accent: '#0091EA',
    error: '#E57373',
    warning: '#ffeb3b',
    info: '#8E24AA',
    success: '#4caf50',
  },
});
