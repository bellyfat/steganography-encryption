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
                  ref="signupForm"
                  :model="signupForm"
                  @submit.native.prevent="doSignup()">
                  <el-form-item>
                    <el-input
                      required
                      v-model="signupFormData.username"
                      placeholder="Username"
                      prefix-icon="fa fa-user"/>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                      required
                      type='email'
                      v-model="signupFormData.email"
                      placeholder="Email Address"
                      prefix-icon="fa fa-envelope"/>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                      type="password"
                      required
                      v-model="signupFormData.passwd_digest"
                      placeholder="Password"
                      prefix-icon="fa fa-lock"/>
                  </el-form-item>
                  <el-form-item v-if="signupFormData.reqErr">
                    <el-alert
                      title="Signup Error"
                      type="error"
                      :description="signupFormData.reqErr"
                      :closable="false"
                      show-icon/>

                  </el-form-item>
                  <el-form-item>
                    <el-button
                      type="danger"
                      native-type="submit"
                      size="medium">Signup</el-button>
                    <el-button
                      type="info"
                      native-type="reset"
                      size="medium">Cancel</el-button>
                  </el-form-item>
                  <el-form-item>
                    <div class="text-smaller">Familiar to SteganoProject? Please <el-button
                      type="text"
                      @click.native.prevent="$router.push('/login');"
                      icon="fa fa-heart">&nbsp;Login.</el-button></div>
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
  name: 'Signup',
  data () {
    return {
      signupForm: null,
      signupFormData: {
        username: '',
        email: '',
        passwd_digest: '',
        gender: null,
        reqErr: null
      }
    }
  },
  methods: {
    doSignup () {
      this.$http.post('/auth/signup', this.signupFormData).then((response) => {
        if (response.status === 200) {
          this.loading = false
          this.$router.push('/login')
        }
      }, (err) => {
        if (err.response.status === 404) {
          this.loading = false
          this.signupFormData.reqErr = 'Sorry, could not find that username'
        } else {
          this.loading = false
          this.signupFormData.reqErr = err.response.status + ': ' + err.response.data.msg
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
