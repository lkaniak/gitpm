<template>
  <v-navigation-drawer
  v-model="drawer"
  v-on:input="checkIfClosed()"
  absolute
  temporary
  app
  width="340">
  <alert
    v-bind:alertMessage="alertMessage"
    v-on:alertClose="alertMessage = ''"></alert>
    <v-list>
      <v-list-tile>
        <v-list-tile-action>
          <v-icon v-html="'settings'"></v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title v-text="'Opções'"></v-list-tile-title>
        </v-list-tile-content>
        <v-list-tile-avatar>
          <pm-helper>
          </pm-helper>
        </v-list-tile-avatar>
      </v-list-tile>
    </v-list>
    <v-divider></v-divider>
    <v-list>
      <v-list>
        <v-list-tile>
          <v-list-tile-content>
            <v-btn
              block
              v-bind:loading="logLoading"
              v-bind:disabled="disabledParameters"
              v-on:click="getLog()">
                Gerar Log
                <span slot="loader" class="custom-loader">
                  <v-icon light>cached</v-icon>
                </span>
              </v-btn>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
            <v-btn
              block
              v-bind:loading="processLoading"
              v-bind:disabled="disabledParameters"
              v-on:click="getProcess()">
                Gerar Processo
                <span slot="loader" class="custom-loader">
                  <v-icon light>cached</v-icon>
                </span>
              </v-btn>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-action>
            <v-icon v-html="'description'"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-layout>
              <v-layout align-center>
                <v-flex xs12>
                  <v-list-tile-title v-text="'Nome do Log:'"></v-list-tile-title>
                </v-flex>
              </v-layout>
              <v-flex xs6>
                <v-text-field
                  clearable
                  label="Nome"
                  single-line
                  v-on:click:clear="$emit('validLog', '')"
                  v-on:change="$emit('validLog', logName)"
                  v-model="logName">
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-action>
            <v-icon v-html="'people_outline'"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-layout>
              <v-layout align-center>
                <v-flex xs12>
                  <v-list-tile-title v-text="'Commits por pessoa:'"></v-list-tile-title>
                </v-flex>
              </v-layout>
              <v-flex xs6>
                <v-text-field
                  clearable
                  single-line
                  v-bind:mask="'####'"
                  v-model="minCommits">
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-action>
            <v-icon v-html="'settings_ethernet'"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="'Parâmetros'"></v-list-tile-title>
          </v-list-tile-content>
          <v-list-tile-avatar>
            <v-btn v-on:click="addParameter()" small depressed color="primary">
              <v-icon>add</v-icon>
            </v-btn>
          </v-list-tile-avatar>
          <v-list-tile-avatar>
            <v-btn v-on:click="removeParameter()" small depressed color="primary">
              <v-icon>remove</v-icon>
            </v-btn>
          </v-list-tile-avatar>
        </v-list-tile>
      </v-list>
        <v-list-tile
          v-for="(parameter, i) in parameters"
          v-bind:key="i">
          <v-list-tile-action>
            <v-icon v-text="parameters[i].icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-layout>
              <v-layout align-center>
                <v-flex xs12>
                  <v-list-tile-title>Parâmetro {{ i+1 }}</v-list-tile-title>
                </v-flex>
              </v-layout>
              <v-flex xs6>
                <v-text-field
                  clearable
                  single-line
                  v-model="parameters[i].value">
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
  </v-navigation-drawer>
</template>

<script>

import { generateLog } from '@/services/log.js';
import { generateProcess } from '@/services/process.js';
import ProcessMiningHelper from '@/modules/helpers/ProcessMiningHelper.vue';
import Alert from  '@/components/Alert.vue';

export default {
  name: 'navigation-drawer',
  props: {
    drawerAnimator: {
      required: true,
      type: Boolean,
    },
    gitRepository: {
      required: false,
      type: String,
    },
  },
  components: {
    'pm-helper': ProcessMiningHelper,
    'alert': Alert
  },
  data() {
    return {
      drawer: this.drawerAnimator,
      logName: '',
      minCommits: '',
      alertMessage: '',
      logLoading: false,
      processLoading: false,
      parameters: [],
    };
  },

  watch: {
    drawerAnimator(val) {
      this.drawer = val;
    },
  },

  computed: {
    disabledParameters() {
      return !(this.logName && this.gitRepository);
    },
  },

  methods: {
    checkIfClosed() {
      if (!this.drawer) {
        this.$emit('closedDrawer');
      }
    },

    getLog() {
      const parameters = {
        url: this.gitRepository,
        minCommits: this.minCommits,
        logName: this.logName,
      };
      this.logLoading = true;
      generateLog(parameters)
        .then((res) => {
          this.logLoading = false;
          this.popAlert('log gerado com sucesso.', 'success');
        })
        .catch((err) => {
          this.logLoading = false;
          this.popAlert('houve um erro ao gerar o log.', 'error');
          });
    },

    getProcess() {
      const parameters = {
        logName: this.logName,
        params: this.parameters.map(parameter => parameter.value),
      };

      this.processLoading = true;
      generateProcess(parameters)
        .then((res) => {
          this.processLoading = false;
          this.$emit('processGenerated', res.automaton);
          this.popAlert('processo gerado com sucesso.', 'success');
        })
        .catch((err) => {
          this.processLoading = false;
          this.popAlert('houve um erro ao gerar o processo.', 'error');
        });
    },

    addParameter() {
      this.parameters.push({
        icon: 'keyboard_arrow_right',
        value: '',
      });
    },

    popAlert(message, status) {
      this.alertStatus = status;
      this.alertMessage = message;
    },

    removeParameter() {
      if (this.parameters.length > 0) {
        this.parameters.pop();
      }
    },
  },
};
</script>

<style scoped>

.v-btn--small {
  min-width: 10px;
  height: 22px;
}

.v-list__tile__action {
  min-width: 30px;
}

</style>
