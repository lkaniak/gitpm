<template>
  <v-card>
    <v-snackbar
    v-model="snackbar"
    v-bind:color="color"
    v-bind:multi-line="mode === 'multi-line'"
    v-bind:timeout="timeout"
    v-bind:vertical="mode === 'vertical'">
    {{ message }}
      <v-btn
        dark
        flat
        v-on:click="deactivateSnackbar()">
        Fechar
      </v-btn>
    </v-snackbar>
  </v-card>
</template>

<script>
export default {
  name: 'alert',
  props: {
    message: {
      required: false,
      type: String,
    },
    color: {
      required: false,
      type: String,
      default: ''
    }
  },

  watch: {
    message(val) {
      this.snackbar = val;
    },
  },

  data() {
    return {
      snackbar: false,
      mode: '',
      timeout: 6000,
    };
  },

  methods: {
    deactivateSnackbar() {
      this.snackbar = false;
      this.$emit('alertClose')
    }
  }
};
</script>

<style scoped>

</style>
