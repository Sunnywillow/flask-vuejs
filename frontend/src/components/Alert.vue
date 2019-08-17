<template>
    <div class="alert" role="alert" v-blind:class=" 'alert-' + variant">
      {{ message }}
    </div>
</template>

<script>
    export default {
      props: ['variant', 'message']
    }
</script>

<style scoped>

</style>
