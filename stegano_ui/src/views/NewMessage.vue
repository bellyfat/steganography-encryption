<template>
  <div id="new-message">
    <el-container>
      <el-main>
        <el-row :gutter="10">
          <el-col :xs="24">
            <div><p>Send a Stegano</p></div>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :xs="20">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span class="text-xl"><strong>Sreenadh</strong></span><br>
                <span class="text-xs">4 hours ago</span>
                <el-button style="float: right; padding: 3px 0" type="text">Close</el-button>
              </div>
              <div v-for="o in 4" :key="o" class="text item">
                {{'List item ' + o }}
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>
<style></style>
<script></script>
