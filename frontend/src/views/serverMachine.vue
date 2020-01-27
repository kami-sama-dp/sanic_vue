<template>
  <div class="fillcontain" style="overflow:hidden">
    <HeaderTopMain></HeaderTopMain>
    <el-card style="margin-top:18px">
      <el-row :gutter="10">
        <el-col :span="7">
          <el-input placeholder="请输入内容">
            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </el-col>
        <!-- <el-col :span="2">
          <el-button type="primary">搜索</el-button>
        </el-col>-->
        <el-col :span="3">
          <el-button type="primary" @click="showaddDialog">添加服务器</el-button>
        </el-col>
      </el-row>
      <el-dialog
        :title="titleMap[dialogTitle]"
        :visible.sync="dialogFormVisible"
        :close-on-click-modal="false"
        @close="closeDialog('machineRef')"
      >
        <el-form :model="form" ref="machineRef" :rules="addMachineRules">
          <el-form-item label="服务器地址:" :label-width="formLabelWidth" prop="ip">
            <el-input v-model="form.ip" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="服务器端口:" :label-width="formLabelWidth" prop="port">
            <el-input v-model="form.port" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="核心数量:" :label-width="formLabelWidth" prop="coresize">
            <el-input v-model="form.coresize" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="控制器:" :label-width="formLabelWidth">
            <el-radio v-model="form.mtype" :label="true">是</el-radio>
            <el-radio v-model="form.mtype" :label="false">否</el-radio>
          </el-form-item>
          <el-form-item label="备注:" :label-width="formLabelWidth" prop="desc">
            <el-input type="textarea" :rows="5" v-model="form.desc" class="input_width"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelOff('machineRef')">取 消</el-button>
          <el-button type="primary" @click="addMachine('machineRef')">确 定</el-button>
        </div>
      </el-dialog>
      <el-table
        :data="serverMachine"
        style="margin-top:18px;font-size:12px;width: 100%"
        border
        stripe
        height="400"
      >
        <el-table-column label="#" prop="id" width="80%"></el-table-column>
        <el-table-column label="服务器地址" prop="ip"></el-table-column>
        <el-table-column label="服务器端口" prop="port"></el-table-column>
        <el-table-column label="核心数量" prop="coresize"></el-table-column>
        <el-table-column label="控制器" prop="mtype" width="90%"></el-table-column>
        <el-table-column label="备注" prop="desc"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope>
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="editShowDialog('machineRef')"
            ></el-button>
            <el-button type="danger" icon="el-icon-delete" size="mini"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页区域-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.curPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="queryInfo.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      ></el-pagination>
    </el-card>
  </div>
</template>

<script>
import HeaderTopMain from "../components/HeaderTopMain";
export default {
  components: {
    HeaderTopMain
  },
  inject: ["reload"],
  data() {
    //自定义校验规则
    var checkIp = (rule, value, callback) => {
      var regIp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
      if (regIp.test(value)) {
        return callback();
      } else {
        callback(new Error("请输入合法的ip"));
      }
    };
    var checkcoreSize = (rule, value, callback) => {
      var regcoreSize = /^\+?[1-9][0-9]*$/;
      if (regcoreSize.test(value)) {
        return callback();
      } else {
        callback(new Error("请输入大于0的整数"));
      }
    };
    return {
      dialogTitle: "",
      titleMap: {
        showaddDialog: "添加服务器",
        editShowDialog: "修改服务器"
      },
      serverMachine: [],
      form: {
        ip: "",
        port: "22",
        coresize: "",
        mtype: false,
        desc: ""
      },
      dialogFormVisible: false,
      formLabelWidth: "120px",
      queryInfo: {
        ip: "",
        curPage: 1,
        pageSize: 10
      },
      total: "",
      addMachineRules: {
        ip: [
          { required: true, message: "请输入地址", trigger: "blur" },
          { validator: checkIp }
        ],
        port: [{ required: true, message: "请输入端口", trigger: "blur" }],
        coresize: [
          { required: true, message: "请输入核心数量", trigger: "blur" },
          { validator: checkcoreSize }
        ]
      }
    };
  },
  created() {
    this.getMachineList();
  },
  methods: {
    closeDialog(refName) {
      this.$refs[refName].resetFields();

      this.dialogFormVisible = false;
    },
    showaddDialog() {
      this.dialogFormVisible = true;
      this.dialogTitle = "showaddDialog";
    },
    editShowDialog() {
      this.dialogFormVisible = true;
      this.dialogTitle = "editShowDialog";
    },
    async getMachineList() {
      try {
        const res = await this.$axios.get("/api/get_machine", {
          params: this.queryInfo
        });
        if (res.status == 200) {
          this.serverMachine = [];
          res.data.result.forEach(item => {
            const table_item = {
              id: item.id,
              ip: item.ip,
              port: item.port,
              coresize: item.coresize,
              mtype: item.mtype == true ? "是" : "否",
              desc: item.desc
            };
            this.total = res.data.total;
            this.serverMachine.push(table_item);
          });
        } else {
          throw new Error(res);
        }
      } catch (err) {
        console.log("获取务器列表数据失败!", err);
      }
    },
    //点击确定按钮,添加数据
    async addMachine(refName) {
      this.$refs[refName].validate(async valid => {
        if (!valid) return;
        else {
          let formData = JSON.stringify(this.form);
          await this.$axios.post("/api/add_machine", formData);
          this.reload(); // 刷新页面
          // this.getMachineList();  刷新页面的另一种处理方式

          this.dialogFormVisible = false;
        }
        this.$refs[refName].resetFields();
      });
    },
    // 取消按钮, 清空表单数据
    async cancelOff(refName) {
      this.$refs[refName].resetFields();
      this.dialogFormVisible = false;
    },
    // 监听pageSize改变的事件
    handleSizeChange(pageSize) {
      this.queryInfo.pageSize = pageSize;
      this.getMachineList();
    },
    //监听页码值改变的事件
    handleCurrentChange(curPage) {
      this.queryInfo.curPage = curPage;
      this.getMachineList();
    }
  }
};
</script>


<style lang="less" scoped>
.input_width {
  width: 50%;
}
</style>