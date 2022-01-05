<template>
    <b-col>{{name}}</b-col> 
    <b-col>
        <span v-if="!commandTopic" class="badge bg-primary">{{state == false ? 'OFF' : 'ON'}}</span>
        <b-form-checkbox switch size="lg" v-if="commandTopic"  @click="onoff" v-model="state" ></b-form-checkbox>
    </b-col>
</template>

<script>

export default {
  name: 'Switch',
  props: {
      stateTopic: String,
      commandTopic: String,
      name: String,
      client: Object
  },
  data() {
      return {
        state: false,
    }
  },
  mounted() {   
    this.client.subscribe(this.stateTopic);
    this.client.on('message',  (topic, message) => {
        if(topic == this.stateTopic) this.state = message.toString() === 'ON';
    });
  },
  methods: {
    onoff() {   
      this.client.publish(this.commandTopic, this.state === true ? 'OFF' : 'ON');
    }
  }
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
