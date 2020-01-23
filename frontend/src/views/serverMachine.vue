<template>
  <div class="fillcontain">
    <HeaderTopMain></HeaderTopMain>
    <el-card style="margin-top:18px">
      <el-row :gutter="10">
        <el-col :span="7">
          <el-input placeholder="请输入内容">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
        <el-col :span="2">
          <el-button type="primary">搜索</el-button>
        </el-col>
        <el-col :span="3">
          <el-button type="danger">添加服务器</el-button>
        </el-col>
      </el-row>

      <el-table :data="serverMachine" style="margin-top:18px;font-size:12px" border stripe>
        <el-table-column type="index"></el-table-column>
        <el-table-column label="服务器地址" prop="ip"></el-table-column>
        <el-table-column label="服务器端口" prop="port"></el-table-column>
        <el-table-column label="用户名" prop="user"></el-table-column>
        <el-table-column label="核心数量" prop="coresize"></el-table-column>
        <el-table-column label="控制器" prop="mtype"></el-table-column>
        <el-table-column label="备注" prop="desc"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import HeaderTopMain from "../components/HeaderTopMain";
export default {
  components: {
    HeaderTopMain
  },
  data() {
    return {};
  },
  created() {
    this.initData();
  },
  methods: {
    initData() {}
  }
};
</script>


<style lang="less" scoped>
</style>