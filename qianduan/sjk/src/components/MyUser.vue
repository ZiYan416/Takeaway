<template>
    <div>
        <div class="header">
            <!-- &nbsp;&nbsp;  -->
            <a class="logo"><i class="icon iconfont icon-food"></i>外卖管理系统</a>
            <nav class="navbar">
                <p>数据库小组作业 <br>
                    成员：宋子杰、刘睿、吕瀚林
                </p>
            </nav>
        </div>
        <div class="body">
            <!-- 左侧导航栏 -->
            <div class="liner">
                <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff"
                    active-text-color="#ffd04b" @select="handleselect">
                    <el-menu-item index="1">
                        <i class="el-icon-food"></i>
                        <span slot="title">首页</span>
                    </el-menu-item>

                    <el-submenu index="2">
                        <template  slot="title">
                            <i class="el-icon-menu"></i>
                            <span>逛店铺</span>
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="2">店铺列表</el-menu-item>
                            <el-menu-item index="10">店铺详情</el-menu-item>
                            <el-menu-item index="9">搜索店铺</el-menu-item>
                        </el-menu-item-group>
                    </el-submenu>

                    <el-submenu index="3">
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
                            <i class="el-icon-s-custom"></i>
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

                <div id="shoplist" v-show="active == 2">
                    <shoplist></shoplist>
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

                <div id="searchshop" v-show="active == 9">
                    <searchshop></searchshop>
                </div>

                <div id="searchshop" v-show="active == 10">
                    <shopdetails></shopdetails>
                </div>
            </div>
        </div>
        <el-dialog title="确认退出" :visible.sync="logoutDialogVisible" width="30%" @close="logoutDialogVisible = false">
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
import shoplist from '@/components/UserShop/ShopList.vue'
import userfinished from '@/components/UserOrder/UserFinished.vue'
import usersending from '@/components/UserOrder/UserSending.vue'
import userunsend from '@/components/UserOrder/UserUnsend.vue'
import indimsg from '@/components/UserMsg/IndiMsg.vue'
import changepwd from '@/components/UserMsg/ChPwd.vue'
import searchshop from '@/components/UserShop/SearchShop.vue'
import shopdetails from '@/components/UserShop/ShopDetails.vue'


export default {
    components: {
        usershop: usershop,
        shoplist: shoplist,
        userfinished: userfinished,
        usersending: usersending,
        userunsend: userunsend,
        indimsg: indimsg,
        changepwd: changepwd,
        searchshop: searchshop,
        shopdetails: shopdetails,
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
    },
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10vh;
    /* text-align: center; */
    display: flex;
    justify-content: space-between;
    align-items: center;
    line-height: 10vh;
    font-size: 28px;
    letter-spacing: 1px;
    font-weight: 800;
    background-color: white;
    /* padding-left: 100px; */
}

.logo {
    margin-left: 2%;
}

.navbar {
    margin-right: 2%;
    font-size: 16px;
    font-weight: 300;
    line-height: 16px;
    display: block;
}

.body {
    width: 100%;
    height: 90vh;
    display: flex;
    justify-content: space-around;
}

.liner {
    width: 15%;
    height: 100%;
    background-color: #545c64;
}

.main {
    background: url("../assets/img/bg02.png");
    width: 85%;
    background-size: 100% 100%;
}
</style>