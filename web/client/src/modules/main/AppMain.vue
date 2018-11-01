<template>
  <v-app>
    <app-header
      v-on:commitsReturned="updateCommits"
      v-on:processGenerated="updateProcess"></app-header>
    <v-content style="padding: 0px">
      <router-view></router-view>
      <automaton
        v-if="process"
        v-bind:automatonData="process"></automaton>
    </v-content>
  </v-app>
</template>


<script>

import AppHeader from './AppHeader.vue';
import Automaton from '@/modules/graph/Automaton.vue';

export default {
  name: 'app-main',
  data() {
    return {
      commits: {},
      process: '',
    };
  },

  methods: {
    updateCommits(commits) {
      this.commits = commits;
    },
    updateProcess(process) {
      this.process = process;
    },
  },

  components: {
    AppHeader,
    Automaton,
  },
};

</script>

<style>

@import '../../assets/css/main/theme_styles.css';

</style>
