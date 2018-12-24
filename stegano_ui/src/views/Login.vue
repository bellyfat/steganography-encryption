<template>
  <div id="login-wrapper">
    <el-container>
      <el-header class="hidden-sm-and-down"/>
      <el-main>
        <el-row
          type="flex"
          justify="center">
          <el-col :md="12">
            <el-row>
              <el-col :md="12">
                <hr class="hidden-md-and-up">
                <el-form
                  ref="loginform"
                  :model="loginForm"
                  @submit.native.prevent="doLogin()">
                  <el-form-item>
                    <el-input
                      required
                      v-model="loginFormData.username"
                      placeholder="Username"
                      prefix-icon="fa fa-user"/>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                      type="password"
                      required
                      v-model="loginFormData.password"
                      placeholder="Username"
                      prefix-icon="fa fa-lock"/>
                  </el-form-item>
                  <el-form-item v-if="loginFormData.reqErr">
                    <el-alert
                      title="Login Error"
                      type="error"
                      :description="loginFormData.reqErr"
                      :closable="false"
                      show-icon/>

                  </el-form-item>
                  <el-form-item>
                    <el-button
                      type="success"
                      native-type="submit"
                      size="medium">Login</el-button>
                    <el-button
                      type="info"
                      native-type="reset"
                      @click="$refs.loginForm.reset();"
                      size="medium">Cancel</el-button>
                  </el-form-item>
                  <el-form-item>
                    <div class="text-smaller">New to SteganoProject? Please <el-button
                      type="text"
                      @click.native.prevent="$router.push('/signup');"
                      icon="fa fa-heart">&nbsp;Signup.</el-button></div>
                  </el-form-item>
                </el-form>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </el-main>
      <el-footer/>
    </el-container>
  </div>
</template>
<script>
export default {
  name: 'Login',
  data () {
    return {
      loginForm: null,
      loginFormData: { username: '', password: '', reqErr: null }
    }
  },
  methods: {
    doLogin () {
      console.log(this.loginFormData)
      var requestOptions = {
        method: 'POST',
        headers: { 'Content-type': 'application/json' }
      }
      var user = {
        username: this.loginFormData.username,
        password: this.loginFormData.password
      }
      this.$auth.login(user, requestOptions).then((response) => {
        if (response.status === 200) {
          this.loading = false
          window.location = '/'
        }
      }, (err) => {
        if (err.response.status === 404) {
          this.loading = false
          this.loginFormData.reqErr = 'Sorry, could not find that username'
        }
        if (err.response.status === 400) {
          this.loading = false
          this.loginFormData.reqErr = err.response.data.msg
        }
      })
    }
  },
  created () {
    if (this.$auth.isAuthenticated()) {
      this.$router.push('/')
    }
  }
}
</script>
<style>
#login-wrapper{
  font-family: "Arial";
  // background-color:#7d4e57;
}
</style>
