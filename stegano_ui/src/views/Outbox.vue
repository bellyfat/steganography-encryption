<template>
  <div id="new-message">
    <el-container>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="24">
            <div><p>Sent Steganos</p></div>
            <hr>
            <br>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <!-- Left side -->
          <el-col :span="6">
            <div class="scrollmenu">
              <el-card v-for="msg in outboxMsgs" :key="msg.id" shadow="hover" style="margin-bottom: 5px">
                <div slot="header" class="clearfix">
                  <span><i><b>{{ msg.sent_by.username | capitalize}}</b></i></span>
                  <p class="text-xs" style="color: grey"><i>{{msg.sent_on | humanizeTime}}</i></p>
                </div>
                <span class="text-xs"><i class="fa fa-paper-plane"></i>&nbsp;<i>Shared to : {{msg.share_to}}</i></span>
              </el-card>
            </div>
            <br>
            <div id="outbox-pagination" v-if="pagination.totalPages > 1">
              <el-pagination @size-change="fetchOutbox" @current-change="fetchOutbox" :current-page.sync="pagination.page" :page-sizes="[15,50,100]" :page-size.sync="pagination.perPage" layout="total, sizes, prev, pager, next, jumper" background :total="pagination.totaPages"/>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>
<style></style>
<script>
export default {
  name: 'outbox',
  data () {
    return {
      outboxMsgs: [],
      openedMsg: null,
      pagination: { page: 1, total: 0, totalPages: 0, perPage: 15 }
    }
  },
  methods: {
    fetchOutbox () {
      var page = this.pagination.page
      var perPage = this.pagination.perPage
      var url = '/api/v1/messages?msg_type=sent&page=' + page + '&perPage=' + perPage
      this.$http.get(url).then(
        (reponse) => {
          this.outboxMsgs = reponse.data.results
          this.pagination.total = response.data.total
          this.pagination.totalPages = response.data.total_pages
        },
        (err) => {
          if (err.response.status === 404) {
            this.outboxMsgs = []
            this.pagination = { page: 1, total: 0, totalPages: 0, perPage: 15 }
          }
        })
    }
  },
  created () {
    this.fetchOutbox()
  }
}
</script>
