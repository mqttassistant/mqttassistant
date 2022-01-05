<template>
  <div>
        <p>Login</p>
        <p>Username: <input v-model="username"></p>
        <p>Password: <input v-model="password"></p>
        <button @click="login()" class="btn btn-large btn-primary">Entra</button>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data() {
      return {username:'', password:''}
  },
  methods: {
    
    login() {
      fetch(process.env.VUE_APP_BASE_URL+'/login', {
          'method': 'POST',
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({ username: this.username, password: this.password })
      });
    }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
