<template>
    <div>
        <div class="header">
            个人信息
        </div>
        <div class="body">
            <el-form ref="form" :model="form" label-width="20%" id="selectForm">
                <el-form-item label="用户名：" prop="user_name">
                    <span>{{ form.user_name }}</span>
                </el-form-item>
                <el-form-item label="真实姓名：" prop="real_name">
                    <span>{{ form.real_name }}</span>
                </el-form-item>
                <el-form-item label="年龄：" prop="age">
                    <span>{{ form.age }}</span>
                </el-form-item>
                <el-form-item label="性别：" prop="sex">
                    <span>{{ form.sex }}</span>
                </el-form-item>
                <el-form-item label="电话：" prop="phone">
                    <span>{{ form.phone }}</span>
                </el-form-item>
                <el-form-item label="邮箱：" prop="mail">
                    <span>{{ form.mail }}</span>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="editUserInfo">修改个人信息</el-button>
                </el-form-item>
            </el-form>
        </div>

        <el-dialog
            title="修改个人信息"
            :visible.sync="editInfoDialogVisible"
            width="50%">
            <el-form :model="form" label-width="20%">
                <el-form-item label="用户名：" prop="user_name">
                    <el-input v-model="form.user_name"></el-input>
                </el-form-item>
                <el-form-item label="真实姓名：" prop="real_name">
                    <el-input v-model="form.real_name"></el-input>
                </el-form-item>
                <el-form-item label="年龄：" prop="age">
                    <el-input v-model="form.age"></el-input>
                </el-form-item>
                <el-form-item label="性别：" prop="sex">
                    <el-input v-model="form.sex"></el-input>
                </el-form-item>
                <el-form-item label="电话：" prop="phone">
                    <el-input v-model="form.phone"></el-input>
                </el-form-item>
                <el-form-item label="邮箱：" prop="mail">
                    <el-input v-model="form.mail"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editInfoDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveUserInfo">保存</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata()
    },
    data() {
        return {
            form: {
                real_name: '',
                sex: '',
                age: '',
                mail: '',
                phone: '',
                user_name: '',
            },
            editInfoDialogVisible: false, // 控制修改个人信息弹窗的显示
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/user/usermsg").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.form.age = res.data.data.age;
                    this.form.mail = res.data.data.mail;
                    this.form.phone = res.data.data.phone;
                    this.form.real_name = res.data.data.real_name;
                    this.form.sex = res.data.data.sex;
                    this.form.user_name = res.data.data.user_name;
                }
            })
        },
        editUserInfo() {
            // 显示修改个人信息弹窗
            this.editInfoDialogVisible = true;
        },
        saveUserInfo() {
            // 发送请求到服务器更新用户信息
            this.$axios.post("/api/user/updateUserInfo", this.form).then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.$message.success("个人信息更新成功");
                    this.editInfoDialogVisible = false; // 关闭弹窗
                    this.getdata(); // 重新获取数据
                } else {
                    this.$message.error("个人信息更新失败");
                }
            });
        }
    },
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

.body {
    width: 40%;
    margin-top: 30px;
    margin: auto;
}

#selectForm >>> .el-form-item__label {
    font-size: 18px;
}

span {
    font-size: 18px;
}
</style>
