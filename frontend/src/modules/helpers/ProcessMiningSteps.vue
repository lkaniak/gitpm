<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
      <v-btn
        slot="activator"
        icon>
        <v-icon>help_outline</v-icon>
      </v-btn>
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark v-on:click.native="dialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>Ajuda</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-stepper v-model="step" vertical>
          <v-stepper-step v-bind:complete="step > 1" step="1" color="primary darken-1">
            Insira a Url de um repositório GitHub e clique em "Buscar".
          </v-stepper-step>

          <v-stepper-content step="1">
            <v-card flat class="mb-5">
              <img src="@/assets/images/step1.png">
            </v-card>
            <v-btn color="primary" v-on:click="step = 2">Próximo</v-btn>
          </v-stepper-content>

          <v-stepper-step v-bind:complete="step > 2" step="2" color="primary darken-1">
            Gere o Log de Eventos clicando no menu no topo superior esquerdo e em "Gerar Log".<br/>
             - É necessário dar um nome ao log.<br/>
             - (opcional) pode-se passar o número de commits mínimos para que um desenvolvedor seja considerado integrante do projeto.
          </v-stepper-step>

          <v-stepper-content step="2">
            <v-card flat class="mb-5">
              <img src="@/assets/images/step2.png">
            </v-card>
            <v-btn color="primary" v-on:click="step = 3">Próximo</v-btn>
            <v-btn color="tertiary white--text" v-on:click="step = 1">Anterior</v-btn>
          </v-stepper-content>

          <v-stepper-step v-bind:complete="step > 3" step="3" color="primary darken-1">
            Gere o processo ao clicar em "Gerar processo".<br/>
            - É possível passar parâmetros para o algoritmo ao clicar no botão de "+" para o número de parâmetros desejados.<br/>
            - os parâmetros estão disponíveis no helper do menu de opções.
          </v-stepper-step>

          <v-stepper-content step="3">
            <v-card flat class="mb-5">
              <img src="@/assets/images/step3.png">
            </v-card>
            <v-btn color="primary" v-on:click="step = 4">Próximo</v-btn>
            <v-btn color="tertiary white--text" v-on:click="step = 2">Anterior</v-btn>
          </v-stepper-content>

          <v-stepper-step step="4" color="primary darken-1">Visualize o log caso o parâmetro foi passado ou baixe os resultados para utilizar em outras ferramentas de Process Mining.</v-stepper-step>
          <v-stepper-content step="4">
            <v-btn color="tertiary white--text" v-on:click="step = 3">Anterior</v-btn>
          </v-stepper-content>
        </v-stepper>
      </v-card>
    </v-dialog>
  </v-layout>
</template>


<script>
export default {
  name: 'pm-steps',
  data() {
    return {
      dialog: false,
      step: 1,
    };
  },
};
</script>

<style scoped>

</style>
