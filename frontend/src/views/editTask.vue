<template>
  <div class="fillcontain">
    <HeaderTopMain></HeaderTopMain>
    <el-card>
      <el-form ref="form" :model="form" label-width="150px" :rules="testTaskRules">
        <el-form-item label="任务名称:" prop="taskname">
          <!-- <el-input v-model="form.taskname" class="input_width"></el-input>  目前不允许修改任务名称-->
          <span>{{form.taskname}}</span>
        </el-form-item>
        <el-form-item label="创建人:">
          <span>{{ form.username}}</span>
        </el-form-item>
        <el-form-item label="上传文件:" prop>
          <el-upload
            class="upload-demo"
            :action="UplaodUrl"
            :limit="1"
            :on-change="onChangeFile"
            :auto-upload="false"
          >
            <el-button size="small" type="primary">点击上传</el-button>
            <span slot="tip" class="el-upload__tip" style="margin-left:12px">只能上传zip包</span>
          </el-upload>
        </el-form-item>

        <el-form-item label="控制器:" prop="master">
          <el-select v-model="form.master" placeholder="请选择控制器">
            <el-option
              v-for="(item,index) in master"
              :key="index"
              :label="item.ip"
              :value="item.ip"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="客户端:" prop="slaves">
          <el-select v-model="form.slaves" placeholder="请选择客户端" :multiple="true">
            <el-option
              v-for="(item, index) in slaves"
              :key="index"
              :label="item.ip"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="被测服务器配置信息:" prop="gameserver">
          <el-input type="textarea" v-model="form.gameserver" class="input_width" :rows="4"></el-input>
        </el-form-item>
        <el-form-item label="自动停止:">
          <el-radio v-model="form.autostop" :label="true">是</el-radio>
          <el-radio v-model="form.autostop" :label="false">否</el-radio>
        </el-form-item>
        <el-form-item label="运行时长:" prop="runtime">
          <el-input
            v-model="form.runtime"
            class="input_width"
            placeholder="例子(300s, 20m, 3h, 1h30m)"
          ></el-input>
        </el-form-item>
        <el-form-item label="目标主机:" prop="testhost">
          <el-input v-model="form.testhost" class="input_width"></el-input>
        </el-form-item>
        <el-form-item label="并发用户数:" prop="usersize">
          <el-input v-model="form.usersize" class="input_width"></el-input>
        </el-form-item>
        <el-form-item label="每秒启动用户数:" prop="userspeed">
          <el-input v-model="form.userspeed" class="input_width"></el-input>
        </el-form-item>
        <el-form-item label="超时指标:">
          <el-input
            v-model="form.indextimes"
            class="input_width"
            placeholder="设置超时分析指标，例子:10,20,30 分别获取超过10ms，20ms，30ms的请求比例(必须设置3个)"
          ></el-input>
        </el-form-item>
        <el-form-item label="备注:">
          <el-input type="textarea" v-model="form.desc" class="input_width" :rows="5"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">保存</el-button>
          <el-button @click="onCancel('form')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import HeaderTopMain from "../components/HeaderTopMain";
import { mapState } from "vuex";
export default {
  components: {
    HeaderTopMain
  },
  data() {
    let master_arr = JSON.parse(localStorage.getItem("master"));
    let slaves_arr = JSON.parse(localStorage.getItem("slaves"));
    let str = '[{"ip":"无","id":"0"}]';
    let master_obj = master_arr != null ? master_arr : "1";
    let slaves_obj = slaves_arr != null ? slaves_arr : JSON.parse(str);
    let data = JSON.parse(
      window.decodeURIComponent(window.atob(this.$route.query.data))
    ); //对url的参数解密
    return {
      UplaodUrl: "/api/test_task/", //上传的地址, 会自动上传(该项目已被禁用,目前会和表单一起提交)
      master: master_obj,
      fd: new FormData(),
      slaves: slaves_obj,
      form: {
        username: data.user,
        taskname: data.task_name,
        master: data.master,
        slaves: JSON.parse(data.slaves),
        gameserver: "未提供服务器配置信息",
        autostop: data.autostop == "是" ? true : false,
        runtime: data.runtime,
        testhost: data.testhost,
        usersize: data.usersize,
        userspeed: data.userspeed,
        indextimes: data.indextimes,
        desc: data.desc
      },
      testTaskRules: {
        taskname: [
          { required: true, message: "请填写任务名称", trigger: "blur" }
        ],
        file: [{ required: true, message: "请上传zip包", trigger: "blur" }],
        master: [{ required: true, message: "请选择控制器" }],
        slaves: [
          { required: true, message: "请选择客户端", trigger: "change" }
        ],
        autostop: [
          { required: true, message: "请勾选是否自动停止", trigger: "blur" }
        ],
        runtime: [
          { required: true, message: "请填写运行时长", trigger: "blur" }
        ],
        usersize: [
          { required: true, message: "请填写用户数", trigger: "blur" }
        ],
        userspeed: [
          { required: true, message: "请填写并发数", trigger: "blur" }
        ]
      }
    };
  },

  methods: {
    onSubmit(refName) {
      this.$refs[refName].validate(async valid => {
        if (!valid) {
          this.$message.error("格式有误!");
          return;
        } else {
          this.fd.append("data", JSON.stringify(this.form));
          const res = await this.$axios.put("/api/test_task/", this.fd);
          if (res.status == 200) {
            this.$message.success("编辑成功");
            this.$router.push("/testTask");
          } else {
            this.$message.error("编辑失败");
          }
        }
      });
    },
    onCancel(refName) {
      this.$router.push("/testTask");
    },
    onChangeFile(file) {
      this.fd.append("file", file.raw);
    }
  }
};
</script>




<style lang="less" scoped>
.input_width {
  width: 30%;
}
</style>
