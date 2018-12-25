<template>
  <div id="new-message">
    <el-container>
      <el-main>
        <el-row :gutter="10">
          <el-col :span="24">
            <div><p>Send a Stegano</p></div>
          </el-col>
        </el-row>
        <hr style="color: grey">
        <el-row :gutter="20" type="flex" justify="center" v-if="uploadNew">
          <el-col :span="12" :offset="6">
            <span>
              <img src="../assets/upload-icon.png" style="cursor: pointer;" @click="uploadNew=false"/>
            </span>
          </el-col>
        </el-row>
        <el-row :gutter="20" type="flex" justify="center" v-else>
          <el-col :span="18">
            <el-row :gutter="5">
              <el-col :span="8" :xs="24">
                <br>
                <el-upload drag action="" accept="" :limit="1" :on-preview="handlePreview" :on-remove="handleRemove" :http-request="handleUpload" list-type="picture" :file-list="fileList">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
                  <div class="el-upload__tip" slot="tip">Works with PNG/BMP files</div>
                </el-upload>
              </el-col>
              <el-col :span="16" :xs="24">
                <el-form label-position="top" :model="messageForm" @submit.native.prevent="uploadStegano">
                  <el-form-item label="Message">
                    <el-input required v-model="messageForm.msg_payload" placeholder="Enter the message to be encrypted"></el-input>
                  </el-form-item>
                  <el-form-item label="Encryption Key">
                    <el-input required v-model="messageForm.msg_enc_key" placeholder="Enter the encryption key"></el-input>
                  </el-form-item>
                  <el-form-item label="Recepient Mail">
                    <el-input required v-model="messageForm.share_to" type="email" placeholder="Enter the recepient email address"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="success" native-type="submit" size="medium">Send</el-button>
                  </el-form-item>
                </el-form>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>
<style></style>
<script>
export default {
  name: 'newmessage',
  data () {
    return {
      uploadNew: false,
      fileList: [],
      messageForm: {
        msg_payload: '',
        msg_enc_key: '',
        share_to: '',
        img_file: ''
      }
    }
  },
  methods: {
    handleUpload (payload) { this.messageForm.img_file = payload.file; console.log(this.messageForm) },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    uploadStegano () {
      if (this.messageForm.img_file) {
        var url = '/api/v1/messages'
        var data = new FormData()
        data.append('file', this.messageForm.img_file)
        data.append('msg_payload', this.messageForm.msg_payload)
        data.append('msg_enc_key', this.messageForm.msg_enc_key)
        data.append('share_to', this.messageForm.share_to)
        this.$http.post(url, data, { headers: { 'Content-Type': 'multipart/form-data' } }).then((response) => {}, (err) => {})
      }
    }
  }
}
</script>
