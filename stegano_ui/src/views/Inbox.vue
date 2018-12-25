<template>
  <div id="new-message">
    <el-container>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="24">
            <div><p>Received Steganos</p></div>
            <hr>
            <br>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="6">
            <div class="scrollmenu">
              <el-card v-for="msg in inboxMsgs" :key="msg.id" shadow="hover" style="margin-bottom: 5px">
                <div slot="header" class="clearfix">
                  <span><i><b>{{ msg.sent_by.username | capitalize}}</b></i></span>
                  <el-button style="float: right; padding: 3px 0" type="text" @click.stop="openedMsg = msg">Open</el-button>
                  <p class="text-xs" style="color: grey"><i>{{msg.sent_on | humanizeTime}}</i></p>
                </div>
                <div v-show="msg.expand">
                  test expand
                </div>
              </el-card>
            </div>
          </el-col>
          <el-col :span="18" v-if="inboxMsgs.length && openedMsg">
            <el-card>
              <div slot="header" class="clearfix">
                <span class="text-xs"><i>Click on the image to unhide the secret message</i></span>
                <p class="text-xs" style="color: grey"><i>{{openedMsg.sent_on | humanizeTime}} ( {{openedMsg.sent_on | calendarTime}} )</i></p>
                <p class="text-xs" style="color: grey">
                  <i>By {{ openedMsg.sent_by.username | capitalize}}</i>(<a :href="'mailto:'+openedMsg.sent_by.email">{{openedMsg.sent_by.email}}</a>)
                </p>
              </div>
              <div>
                <pre>{{openedMsg}}</pre>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>
<style></style>
<script>
export default {
  name: 'inbox',
  data () {
    return {
      inboxMsgs: [],
      openedMsg: null
    }
  },
  methods: {
    fetchInbox () {
      var url = '/api/v1/messages'
      this.$http.get(url).then(
        (reponse) => {
          this.inboxMsgs = reponse.data.results
        },
        (err) => {})
    }
  },
  created () {
    this.fetchInbox()
  }
}
</script>
