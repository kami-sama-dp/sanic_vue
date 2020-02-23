<template>
  <div class="fillcontain">
    <HeaderTopMain></HeaderTopMain>
    <div>
      <h2>响应详细数据</h2>
      <el-table
        :data="requestRequest"
        style="margin-top:18px;font-size:12px;width: 100%"
        border
        stripe
        height="70%"
      >
        <el-table-column label="方法" prop="Method" width="120%"></el-table-column>
        <el-table-column label="请求" prop="Name" width="300%"></el-table-column>
        <el-table-column label="总数" prop="requests"></el-table-column>
        <el-table-column label="错误" prop="failures"></el-table-column>
        <el-table-column label="中值" prop="Median_response_time"></el-table-column>
        <el-table-column label="平均" prop="Average_response_time"></el-table-column>
        <el-table-column label="最小" prop="Min_response_time"></el-table-column>
        <el-table-column label="最大" prop="Max_response_time"></el-table-column>
        <el-table-column label="响应体" prop="Average_Content_Size"></el-table-column>
        <el-table-column label="rps" prop="rps"></el-table-column>
      </el-table>
    </div>
    <div>
      <h2 style="margin-top:15px">响应时间分布</h2>
      <el-table
        :data="requestDistribution"
        style="margin-top:18px;font-size:12px;width: 100%"
        border
        stripe
        height="100%"
      >
        <el-table-column label="请求方法" prop="Name" width="300%"></el-table-column>
        <el-table-column label="总数" prop="requests"></el-table-column>
        <el-table-column label="50%" prop="50%"></el-table-column>
        <el-table-column label="66%" prop="66%"></el-table-column>
        <el-table-column label="75%" prop="75%"></el-table-column>
        <el-table-column label="80%" prop="80%"></el-table-column>
        <el-table-column label="90%" prop="90%"></el-table-column>
        <el-table-column label="95%" prop="95%"></el-table-column>
        <el-table-column label="98%" prop="98%"></el-table-column>
        <el-table-column label="99%" prop="99%"></el-table-column>
        <el-table-column label="100%" prop="100%"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import HeaderTopMain from "../components/HeaderTopMain";
export default {
  components: {
    HeaderTopMain
  },
  data() {
    let data = JSON.parse(
      window.decodeURIComponent(window.atob(this.$route.query.data))
    );
    return {
      requestRequest: data.request_file,
      requestDistribution: data.distribution_file
    };
  },
  computed: {}
};
</script>

<style lang="less" scoped>
</style>