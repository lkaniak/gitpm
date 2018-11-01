<template>
    <div
      style="max-height: 120px;  min-height: 120px; margin: 0">
      <alert
        v-bind:message="alertMessage"
        v-bind:color="alertStatus"
        v-on:alertClose="alertMessage = ''"></alert>
      <navi-drawer
        v-bind:drawerAnimator="drawer"
        v-bind:gitRepository="repositoryURL"
        v-on:closedDrawer="drawer = false"
        v-on:processGenerated="updateProcess"
        v-on:validLog="validLog = $event"></navi-drawer>
      <v-toolbar
      app
      color="primary"
      v-bind:clipped-left="clipped"
      class="pb-3"
      height="80">
        <v-layout align-center>
          <v-flex xs1 style="flex-basis: 4%">
            <v-toolbar-side-icon v-on:click.stop="drawer = !drawer" class="pt-2"></v-toolbar-side-icon>
          </v-flex>
          <v-flex xs1 style="flex-basis: 6%">
            <v-toolbar-title v-text="title" class="pt-2"></v-toolbar-title>
          </v-flex>
          <v-flex xs3>
            <repo-search-bar
              v-on:commitsReturned="updateCommits"
              v-on:changed="updateRepositoryURL($event)"
              v-on:urlValidation="validRepo = $event">
            </repo-search-bar>
          </v-flex>
          <v-flex xs1>
            <v-spacer></v-spacer>
          </v-flex>
          <v-flex xs6>
            <v-btn
              v-bind:loading="logLoading"
              v-bind:disabled="logLoading || !repositoryURL || !validLog"
              color="success"
              v-on:click="download('log')">
                Baixar Log CSV
              <span slot="loader" class="custom-loader">
                <v-icon light>cached</v-icon>
              </span>
            </v-btn>
            <v-btn
              v-bind:loading="processLoading"
              v-bind:disabled="processLoading || !repositoryURL || !validLog"
              color="success"
              v-on:click="download('process')">
                Baixar Log XES
              <span slot="loader" class="custom-loader">
                <v-icon light>cached</v-icon>
              </span>
            </v-btn>
            <v-btn
              v-bind:loading="commitsLoading"
              v-bind:disabled="commitsLoading || !repositoryURL || !validRepo"
              color="success"
              v-on:click="download('commits')">
                Baixar Commits CSV
              <span slot="loader" class="custom-loader">
                <v-icon light>cached</v-icon>
              </span>
            </v-btn>
          </v-flex>
          <v-flex xs1>
            <pm-steps>
            </pm-steps>
          </v-flex>
        </v-layout>
      </v-toolbar>
    </div>
</template>


<script>

import RepositorySearchBar from '@/components/RepositorySearchBar.vue';
import NavigationDrawer from '@/components/NavigationDrawer.vue';
import ProcessMiningSteps from '@/modules/helpers/ProcessMiningSteps.vue';
import Alert from  '@/components/Alert.vue';
import saveAs from 'file-saver';

import { downloadRepository } from '@/services/repositories';
import { downloadLog } from '@/services/log';
import { downloadProcess } from '@/services/process';

export default {
  name: 'app-header',
  data() {
    return {
      showNav: false,
      logLoading: false,
      processLoading: false,
      commitsLoading: false,
      alertMessage: '',
      alertStatus: '',
      repositoryURL: '',
      clipped: false,
      validRepo: false,
      validLog: '',
      drawer: false,
      fixed: false,
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Gitpm',
      commits: {},
      process: ''
    }
  },
  components: {
    'repo-search-bar': RepositorySearchBar,
    'navi-drawer': NavigationDrawer,
    'pm-steps': ProcessMiningSteps,
    'alert': Alert
  },

  computed: {

    responsive() {
      let responsive = true;
      if (document.documentElement.clientWidth < 1000) {
        responsive = false;
      }
      return responsive;
    }
  },
  methods: {
    updateCommits(commits) {
      this.commits = commits;
      this.$emit('commitsReturned', this.commits);
    },

    updateProcess(process) {
      this.process = process;
      this.$emit('processGenerated', this.process);
    },

    popAlert(message, status) {
      this.alertStatus = status;
      this.alertMessage = message;
    },

    download(entity) {
      switch (entity) {
        case 'commits':
          this.commitsLoading = true;
          downloadRepository({
            'url': this.repositoryURL,
          }).then((data) => {
            let content = "hash,author,email,timestamp,message,modifiedfiles\n\n";
            const commits = data;
            commits.forEach((commit) => {
              content += `${commit.hashID},${commit.user},${commit.email},${commit.date},${commit.message}\n`;
              commit.modifiedFiles.forEach((mFile) => {
                content += `${mFile.status}\t\t\t\t${mFile.modifiedFile}`;
              })
              content += '\n\n';
            });
            const repositoryNameParse = this.repositoryURL.split('/');
            const repo = repositoryNameParse.pop();
            const onwer = repositoryNameParse.pop();
            const filename = `gitlog_${onwer}-${repo}.csv`;
            const blob = new Blob([content], {
              type: "text/plain;charset=utf-8"
            });

            saveAs(blob, filename);
            this.commitsLoading = false;
          }).catch((err) => {
            this.popAlert('Ocorreu um erro ao baixar os commits.', 'error');
            this.commitsLoading = false;
          })
          break;

        case 'process':
        this.processLoading = true;
          downloadProcess({
            'logName': this.validLog,
          }).then((response) => {
            const filename = response.headers['content-disposition'].split('filename=')[1];
            const blob = new Blob([response.data], {
              type: "text/plain;charset=utf-8"
            });
            saveAs(blob, filename);
            this.processLoading = false;
          }).catch(() => {
            this.popAlert('Ocorreu um erro ao baixar o log XES do processo.', 'error');
            this.processLoading = false;
          });

          break;

        case 'log':
          this.logLoading = true;
          downloadLog({
            'logName': this.validLog,
          }).then((response) => {
            const filename = response.headers['content-disposition'].split('filename=')[1];
            const blob = new Blob([response.data], {
              type: "text/plain;charset=utf-8"
            });
            saveAs(blob, filename);
            this.logLoading = false;
          }).catch(() => {
            this.popAlert('Ocorreu um erro ao baixar o log CSV do processo.', 'error');
            this.logLoading = false;
          });

          break;

        default:
          break;
      }
    },

    updateRepositoryURL(repo) {
      this.repositoryURL = repo;
    }
  },
};

</script>

<style scoped>

</style>

