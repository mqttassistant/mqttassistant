<template>Node
  <b-card no-body>
    <b-tabs pills card>
        <b-tab v-for="tab,i in interfaces" :title="tab.name" :key="i">
            <b-container v-for="node,j in tab.nodes" :title="node.name" :key="j">
                <b-row>
                    <Switch v-if="node.type=='binary_sensor'" :name="node.name" :state-topic="node.topic_state" :command-topic="node.topic_command" :client="client"/>
                    <Sensor v-if="node.type=='sensor'" :name="node.name" :state-topic="node.topic_state" :client="client" />
                </b-row>
            </b-container>
        </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Switch from './Switch.vue'
import Sensor from './Sensor.vue'

import mqtt from  'mqtt';

export default {
  name: 'Nodes',
  data() {
    return {
      interfaces: [],
      client: {},
    }
  },
  components: {
   Switch,
   Sensor
  },
  mounted() {

    


    // Carico la configurazione e mi collego a mosquitto
    fetch("config.json")
    .then( response => response.json())
    .then( (config) =>  {
      this.client = mqtt.connect('mqtt://'+config.MQTT_HOST+':'+ config.MQTT_PORT, {
          username: config.MQTT_USERNAME,
          password: config.MQTT_PASSWORD
      })
    })
    .catch(error => {
      console.error("There was an error!", error);
    });
    
    // Carico la struttura dell'interfaccia
    /*fetch("interfaces.json")
    .then( response => response.json())
    .then( data =>  (this.interfaces = data))
    .catch(error => {
      console.error("There was an error!", error);
    });
    */
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
