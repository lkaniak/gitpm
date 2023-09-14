<template>
  <v-layout align-center>
    <alert
      v-bind:message="alertMessage"
      v-bind:color="alertStatus"
      v-on:alertClose="alertMessage = ''"></alert>
    <v-flex xs8>
      <v-text-field
        ref="repositorySearch"
        v-model="repositoryURL"
        v-bind:error-messages="errors"
        v-on:click:clear="clear()"
        v-on:input="validation(repositoryURL)"
        v-on:change="$emit('changed', $event)"
        clear-icon="backspace"
        clearable
        color="primary"
        background-color="secondary"
        flat
        label="Buscar Repositório"
        prepend-inner-icon="search"
        solo>
      </v-text-field>
    </v-flex>
    <v-flex xs2 align-content-center>
      <v-btn
        v-bind:loading="loading"
        v-bind:disabled="loading || !repositoryURL || !valid"
        color="success"
        v-on:click="searchRepository()">
          Buscar
        <span slot="loader" class="custom-loader">
          <v-icon light>cached</v-icon>
        </span>
      </v-btn>
    </v-flex>
  </v-layout>
</template>


<script>

import Alert from  '@/components/Alert.vue';
import { debounce } from 'lodash';
import { getRepository } from '@/services/repositories.js';
import { wellDefinedURL, repoOwnerFormat } from '@/utils/string';

export default {
  name: 'repo-search-bar',
  data() {
    return {
      showNav: false,
      loading: false,
      valid: false,
      repositoryURL: '',
      alertStatus: '',
      alertMessage: '',
      errors: [],
      commits: {},
      validations: [repoOwnerFormat],
    };
  },

  components: {
    'alert': Alert
  },

  watch: {
    valid(val) {
      this.$emit('urlValidation', val)
    },
  },

  methods: {
    debounceRepoSearch: debounce(function debounceInput(input) {
      if (this.$refs.repositorySearch.validate()) {
        this.repositoryURL = input;
        const searchParameters = {
          url: this.repositoryURL,
          parameters: '',
        };
        getRepository(searchParameters)
          .then((data) => {
            this.commits = data;
          })
          .catch(() => { });
      }
    }, 2000),

    validation(toValidate) {
      let count = 0;
      let ret = true;
      let result = null;
      this.validations.forEach((validation) => {
        result = validation(toValidate);
        if (typeof result === 'string') {
          ret = false;
          if (!this.errors.find((err => err === result))) {
            this.errors.push(result);
          }
        }
        count += 1;
      });
      if (ret) {
        this.errors = [];
      }
      this.valid = ret;
      return ret;
    },

    popAlert(message, status) {
      this.alertStatus = status;
      this.alertMessage = message;
    },

    searchRepository() {
      const searchParameters = {
        url: this.repositoryURL,
        parameters: '',
      };
      this.loading = true;
      getRepository(searchParameters)
        .then((data) => {
          this.loading = false;
          this.commits = data;
          this.$emit('commitsReturned', this.commits);
          this.popAlert('commits buscados com sucesso.', 'success');
        })
        .catch((err) => {
          this.popAlert('ocorreu um erro ao buscar os commits.', 'error');
          this.loading = false;
        });
    },
    clear() {
      this.repositoryURL = '';
      this.$refs.repositorySearch.reset();
    },
  },
};
</script>

<style scoped>

.search-input {
  width: 275px;
}

</style>
