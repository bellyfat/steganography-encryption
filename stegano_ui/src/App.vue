<template>
  <div
    id="app"
    v-if="!$route.meta.public">
    <!-- Main pages -->
    <router-view/>
  </div>
  <div
    id="app"
    v-else
    style="height='100%'">
    <!-- Login, Signup, About pages -->
    <router-view/>
  </div>
</template>

<script>
import Login from './views/Login.vue'

export default {
  name: 'App',
  components: {
    Login
  }
}
</script>
<style>
.text-xs {
  font-size: 12px;
}
.text-sm {
  font-size: 13px;
}
.text-md {
  font-size: 14px;
}
.text-lg {
  font-size: 16px;
}
</style>
