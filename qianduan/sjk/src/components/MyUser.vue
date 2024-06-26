<template>
    <div>
        <div class="header">
            &nbsp;&nbsp; 外卖管理系统
        </div>
        <div class="body">
            <!-- 左侧导航栏 -->
            <div class="liner">
                <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff"
                    active-text-color="#ffd04b" @select="handleselect">
                    <!-- <el-submenu index="1">
                        <template slot="title">
                            <i class="el-icon-location"></i>
                            <span>导航一</span>
                        </template>
                        <el-menu-item-group>
                            <template slot="title">分组一</template>
                            <el-menu-item index="1-1">选项1</el-menu-item>
                            <el-menu-item index="1-2">选项2</el-menu-item>
                        </el-menu-item-group>
                        <el-menu-item-group title="分组2">
                            <el-menu-item index="1-3">选项3</el-menu-item>
                        </el-menu-item-group>
                        <el-submenu index="1-4">
                            <template slot="title">选项4</template>
                            <el-menu-item index="1-4-1">选项1</el-menu-item>
                        </el-submenu>
                    </el-submenu> -->
                    <el-menu-item index="1">
                        <i class="el-icon-menu"></i>
                        <span slot="title">逛店铺</span>
                    </el-menu-item>

                    <el-submenu index="2">
                        <template slot="title">
                            <i class="el-icon-setting"></i>
                            <span>个人订单</span>
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="3">已完成订单</el-menu-item>
                            <el-menu-item index="4">已发货订单</el-menu-item>
                            <el-menu-item index="5">未发货订单</el-menu-item>
                        </el-menu-item-group>

                    </el-submenu>

                    <el-submenu>
                        <template slot="title">
                            <i class="el-icon-s-home"></i>
                            <span>个人中心</span>
                        </template>
                        <el-menu-item-group>

                            <el-menu-item index="6">个人信息</el-menu-item>
                            <el-menu-item index="7">修改密码</el-menu-item>
                            <el-menu-item index="8">退出登录</el-menu-item>
                        </el-menu-item-group>

                    </el-submenu>

                </el-menu>
            </div>
            <div class="main">
                <div id="usershop" v-show="active == 1">
                    <usershop></usershop>
                </div>

                <div id="userfinished" v-show="active == 3">
                    <userfinished></userfinished>
                </div>

                <div id="usersending" v-show="active == 4">
                    <usersending></usersending>
                </div>

                <div id="userunsend" v-show="active == 5">
                    <userunsend></userunsend>
                </div>

                <div id="indimag" v-show="active == 6">
                    <indimsg></indimsg>
                </div>

                <div id="changepwd" v-show="active == 7">
                    <changepwd></changepwd>
                </div>

            </div>
        </div>
        <el-dialog
            title="确认退出"
            :visible.sync="logoutDialogVisible"
            width="30%"
            @close="logoutDialogVisible = false">
            <span>你确定要退出登录吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="logoutDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmLogout">确认</el-button>
            </span>
        </el-dialog>
         <!-- 修改个人信息弹窗
         <el-dialog
            title="修改个人信息"
            :visible.sync="editInfoDialogVisible"
            width="50%">
            <el-form :model="userInfo">
                <el-form-item label="用户名">
                    <el-input v-model="userInfo.username"></el-input>
                </el-form-item>
                <el-form-item label="电子邮件">
                    <el-input v-model="userInfo.email"></el-input>
                </el-form-item>
                <el-form-item label="电话号码">
                    <el-input v-model="userInfo.phone"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editInfoDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveUserInfo">保存</el-button>
            </span>
        </el-dialog> -->
    </div>
</template>

<script>
import usershop from '@/components/UserShop.vue'
import userfinished from '@/components/UserOrder/UserFinished.vue'
import usersending from '@/components/UserOrder/UserSending.vue'
import userunsend from '@/components/UserOrder/UserUnsend.vue'
import indimsg from '@/components/UserMsg/IndiMsg.vue'
import changepwd from '@/components/UserMsg/ChPwd.vue'
export default {
    components: {
        usershop: usershop,
        userfinished: userfinished,
        usersending: usersending,
        userunsend: userunsend,
        indimsg: indimsg,
        changepwd: changepwd,
    },
    data() {
        return {
            active: 1,
            logoutDialogVisible: false, // 控制退出登录确认弹窗的显示
            // editInfoDialogVisible: false, // 控制修改个人信息弹窗的显示
            // userInfo: {
            //     username: '',
            //     email: '',
            //     phone: '',
            // }
        };
    },
    methods: {
        handleselect(index) {
            if (index == 8) {
                this.logoutDialogVisible = true; // 显示退出登录确认弹窗
            } else {
                this.active = index;
            }
        },
        confirmLogout() {
            // 实现退出登录逻辑，比如清除本地存储中的用户信息并重定向到登录页面
            localStorage.removeItem('userToken'); // 假设你用localStorage存储用户令牌
            this.$router.push('/login'); // 假设你用vue-router重定向到登录页面
            this.logoutDialogVisible = false; // 关闭弹窗
        },
        // editUserInfo() {
        //     // 显示修改个人信息弹窗
        //     this.editInfoDialogVisible = true;
        // },
        // saveUserInfo() {
        //     // 保存用户信息的逻辑，比如发送请求到服务器更新用户信息
        //     console.log(this.userInfo);
        //     this.editInfoDialogVisible = false; // 关闭弹窗
        // },
    } ,
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10vh;
    /* text-align: center; */
    line-height: 10vh;
    font-size: 25px;
    font-weight: 800;
    background-color: #e3e3e3;
    /* padding-left: 100px; */
}

.body {
    width: 100%;
    height: 648px;
    display: flex;
    justify-content: space-around;
}

.liner {
    width: 15%;
    height: 100%;
    background-color: #545c64;
}

.main {
    width: 85%;
}
</style>