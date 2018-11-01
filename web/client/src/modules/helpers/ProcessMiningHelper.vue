<template>
  <div class="text-xs-center">
    <v-dialog
      v-model="dialog"
      width="500">
      <v-btn
        slot="activator"
        icon>
        <v-icon>help_outline</v-icon>
      </v-btn>
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title>
          Parâmetros Disponíveis
        </v-card-title>

        <v-card-text>
          <v-expansion-panel focusable>
            <v-expansion-panel-content
              v-for="(parameter, i) in parameters"
              v-bind:key="i">
              <div slot="header">{{ parameter.title }}</div>
              <v-card>
                <v-card-text class="grey lighten-3"> <strong> comando: {{ parameter.command }} </strong> <br/> {{ parameter.description }}</v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <span class="caption">Mais informações disponíveis em: <a href="https://github.com/cdc08x/MINERful"> MINERful </a> </span>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            v-on:click="dialog = false">
            Fechar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  command: 'pm-helper',
  data() {
    return {
      dialog: false,
      parameters: [{
        title: 'Autômato',
        command: 'automaton',
        description: 'Gera o autômato relativo ao processo gerado.',
      }, {
        title: 'Threads para o processamento do log',
        command: '-p',
        description: 'Threads a serem utilizadas para o processamento.',
      }, {
        title: 'Threads para processamento da base de dados',
        command: '-pQ',
        description: 'Threads a serem utilizadas para o processamento da base de conhecimento. Valor deve ser maior ou igual a 1.',
      }, {
        title: 'Fator de Confiança',
        command: '-s',
        description: ' Valor para o fator de confiança (support/reliability); Deve ser um valor entre 0.0 a 1.0. Por padrão é: 0.95',
      }, {
        title: 'Fator de relevância',
        command: '-c',
        description: 'Valor para o fator de incidências do evento gerador baseado no fator de confiança (confidence); Deve ser um valor entre 0.0 a 1.0. Por padrão é: 0.25',
      }, {
        title: 'Fator de Interesse',
        command: '-i',
        description: 'Valor para o fator de incidências do evento alvo baseado no fator de relevância. (interest); Deve ser um valor entre 0.0 a 1.0. Por padrão é: 0.125',
      }, {
        title: 'Branching',
        command: '-b',
        description: 'Sub-nîvel mâximo para utilizar em restrições encontradas. Valor deve ser maior ou igual a 1.',
      }, {
        title: 'Filtro de restrições',
        command: '-cS',
        description: "Regra do filtro de restrições a serem aplicadas. Tipos possîveis: 'type', 'support', 'interest'",
      }, {
        title: 'Classificação dos eventos',
        command: '-eC',
        description: "Forma a ser utilizada para a classificação dos eventos: Por nome da atividade ('name') ou pelo formato especificado no log ('logspec').",
      }, {
        title: 'No folding',
        command: '-noCF',
        description: 'Evita que as restrições descobertas sejam vinculadas as atividades.',
      }, {
        title: 'Pós processamento',
        command: '-ppAT',
        description: `Tipo de pós-processamento a ser utilizado.
          Valores possîveis: 'none', 'hierarchy', 'hierarchyconflict', 'hierarchyconflictredundancy', 'hierarchyconflictredundancydouble'.
          Por padrão é: hierachy.
          Quanto mais restritivo for o método, maior será o processamento necessário.`,
      },
      ],
    };
  },
};
</script>

<style scoped>

</style>
