<template>
  <div
  id="app"
  v-if="!$route.meta.public">
  <!-- Main pages -->
  <el-container>
    <el-aside>
      <el-menu router default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" background-color="#fff" text-color="#0f0f0f" active-text-color="#b35465">
        <el-menu-item index="new">
          <span>Stegano</span>
        </el-menu-item>
        <el-menu-item index="new">
          <i class="el-icon-d-arrow-right"></i>
          <span>Send</span>
        </el-menu-item>
        <el-menu-item index="inbox">
          <i class="el-icon-message"></i>
          <span>Inbox</span>
        </el-menu-item>
        <el-menu-item index="outbox">
          <i class="el-icon-circle-check"></i>
          <span>Sent</span>
        </el-menu-item>
      </el-menu>

    </el-aside>
    <el-main>
      <router-view/>
    </el-main>
  </el-container>
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
.text-xl {
  font-size: 18px;
}
</style>
