<template>
  <network
    id="automaton"
    v-bind:options="options"
    v-bind:nodes="data.nodes"
    v-bind:edges="data.edges">
  </network>
</template>

<script>

import * as vue2vis from 'vue2vis';
import vis from 'vis';

export default {
  name: 'automaton',
  props: {
    automatonData: {
      required: true,
      type: String,
    },
  },
  components: {
    network: vue2vis.Network,
  },
  data() {
    return {
      data: {},
      options: {},
      type: 'automaton',
    };
  },

  created() {
    this.$nextTick(() => {
      const parsedData = vis.network.convertDot(this.automatonData);
      Object.keys(parsedData.nodes).forEach((key) => {

        if (parsedData.nodes[key].shape == "doublecircle") {
          parsedData.nodes[key].color = "red";
        }

        if (parsedData.nodes[key].id == "initial") {
          parsedData.nodes[key].color = "green";
          parsedData.nodes[key].shape = "circle";
        }

      });
      this.data = {
        nodes: parsedData.nodes,
        edges: parsedData.edges,
      };

      const opt = parsedData.options;
      opt.height = '500px'; // TODO: fix static height, start zoom
      opt.width = '100%';

      this.options = opt;
    });
  },

  watch: {
    automatonData() {
      const parsedData = vis.network.convertDot(this.automatonData);
      Object.keys(parsedData.nodes).forEach((key) => {

        if (parsedData.nodes[key].shape == "doublecircle") {
          parsedData.nodes[key].color = "red";
        }

        if (parsedData.nodes[key].id == "initial") {
          parsedData.nodes[key].color = "green";
          parsedData.nodes[key].shape = "circle";
        }

      });
      this.data = {
        nodes: parsedData.nodes,
        edges: parsedData.edges,
      };

      const opt = parsedData.options;
      opt.height = '100%';
      opt.width = '100%';

      this.options = opt;
    },
  },
};
</script>

<style>

#automaton {
  height: -webkit-fill-available;
}

</style>
