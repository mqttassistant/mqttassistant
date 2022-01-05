<template>
  <b-col>{{name}}</b-col>
  <b-col>
      <b-badge pill variant="primary">{{state}}</b-badge>
  </b-col>
</template>

<script>

export default {
  name: 'Sensor',
  props: {
      stateTopic: String,
      name: String,
      client: Object
  },
  data() {
      return {
        state: '',
    }
  },
  mounted() {
    this.client.subscribe(this.stateTopic);
    this.client.on('message',  (topic, message) => {
        if(topic == this.stateTopic) this.state = message.toString();
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
