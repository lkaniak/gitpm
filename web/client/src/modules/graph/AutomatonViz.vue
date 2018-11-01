<template>
  <div id="app-automaton">
  </div>
</template>

<script>

import Viz from 'viz.js';
import { Module, render } from 'viz.js/full.render.js';

export default {
  name: 'automatonViz',
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
      type: 'automatonViz',
    };
  },

  created() {
    let viz = new Viz({ Module, render });
    const vm = this;
    viz.renderSVGElement(this.automatonData)
      .then((element) => {
        console.log('element created: ', element);
        vm.graph = JSON.stringify(element);
        document.querySelector('#app-automaton').appendChild(element);
      })
      .catch((error) => {
        console.log('error: ', error);
        // Create a new Viz instance (@see Caveats page for more info)
        viz = new Viz({ Module, render });

        // Possibly display the error
        console.error(error);
      });
  },

  watch: {
    automatonData() {
      let viz = new Viz({ Module, render });
      const vm = this;

      viz.renderSVGElement(this.automatonData)
        .then((element) => {
          console.log('element monted: ', element);
          vm.graph = element;
          document.querySelector('#app-automaton').appendChild(element);
        })
        .catch((error) => {
          console.log('error: ', error);
          // Create a new Viz instance (@see Caveats page for more info)
          viz = new Viz({ Module, render });

          // Possibly display the error
          console.error(error);
        });
    },
  },
};
</script>

<style>

#automaton {
  height: -webkit-fill-available;
}

</style>
