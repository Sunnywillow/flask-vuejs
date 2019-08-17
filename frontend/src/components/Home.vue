<template>
    <div class="container">
      <alert
        v-for="(alert, index) in alerts" :key="index"
        v-if="alert.showAlert"
        v-bind:variant="alert.alertVariant"
        v-bind:message="alert.alertMessage">
      </alert>
    </div>
</template>

<script>
  import Alert from './Alert'
    export default {
        name: "Home", //this is the name of the component
        components: {
          alert: Alert
        },
      data () {
          return {
            alerts: [
              {
                showAlert: ture,
                alertVariant: 'danger',
                alertMessage: 0
              },
              {
                showAlert: ture,
                alertVariant: 'info',
                alertMessage: 1
              },
              {
                showAlert: true,
                alertVariant: 'dark',
                alertMessage: 2
              }
            ]
          }
      }
    }
</script>

<style scoped>

</style>
