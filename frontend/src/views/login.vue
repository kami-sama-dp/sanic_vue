<template>
  <div class="login_page fillcontain">
    <transition name="form-fade" mode="in-out">
      <section class="form_contianer" v-show="showLogin">
        <div class="manage_tip">
          <p>管理系统</p>
        </div>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" placeholder="密码" v-model="loginForm.password"></el-input>
          </el-form-item>
          <el-form-item class>
            <!--  btns-->
            <el-button type="primary" @click="submitForm('loginFormRef')">登录</el-button>
            <el-button type="info" @click="resetForm('loginFormRef')">重置</el-button>
          </el-form-item>
        </el-form>
        <p class="tip" style="margin-top:-5px">温馨提示：</p>
        <p class="tip" style="margin-top:3px">未登录过的新用户，自动注册</p>
        <p class="tip" style="margin-top:3px">注册过的用户可凭账号密码登录</p>
      </section>
    </transition>
  </div>
</template>


<script>
export default {
  data: function() {
    return {
      loginForm: {
        username: "",
        password: ""
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      showLogin: false
    };
  },
  mounted: function() {
    this.showLogin = true;
    // if (!this.adminInfo.id) {
    //         this.getAdminData()
    //     }
  },
  methods: {
    //重置登录
    async resetForm(name) {
      this.$refs[name].resetFields();
      //console.log(this);
    },
    async submitForm(name) {
      this.$refs[name].validate(async valid => {
        if (valid) {
          this.$axios.default.auth = {
            username: this.loginForm.username,
            password: this.loginForm.password
          };

          const res = await this.$axios.post(
            "/api/login/",
            JSON.stringify(this.loginForm)
		  );
          if (res.status == 200) {
            this.$notify({
              title: "登录成功",
              type: "success",
			  offset: 80,
			  duration: 3000,
            });
            let token = res.data.token;
            this.$store.commit("set_token", token);
            this.$router.push("/serverMachine");
          }  
        } else return;
      });
    }
  }
};
</script>

<style lang="less" scoped>
@import "../style/mixin.less";
.login_page {
  background-color: #244e92;
}
.manage_tip {
  position: absolute;
  width: 100%;
  top: -60px;
  left: 0;
  p {
    font-size: 34px;
    color: #fff;
  }
}
.form_contianer {
  width: 320px;
  .ctp(320px, 210px);
  padding: 25px;
  border-radius: 5px;
  text-align: center;
  background-color: #fff;
  .submit_btn {
    width: 100%;
    font-size: 16px;
  }
}
.tip {
  font-size: 12px;
  color: red;
}
.form-fade-enter-active,
.form-fade-leave-active {
  transition: all 1s;
}
.form-fade-enter,
.form-fade-leave-active {
  transform: translate3d(0, -50px, 0);
  opacity: 0;
}
.btns {
  display: flex;
  justify-content: flex-end;
}
</style>