<template>
    <div>
        <div class="header">
            <!-- &nbsp;&nbsp;  -->
            <a class="logo"><i class="icon iconfont icon-manager"></i>外卖管理系统——后台管理</a>
            <nav class="navbar"><p>数据库小组作业 <br>
                成员：宋子杰、刘睿、吕瀚林
            </p></nav>
        </div>
        <div class="body">
            <div class="liner">
                <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff"
                    active-text-color="#ffd04b" @select="handleselect">

                    <el-menu-item index="1">
                        <i class="el-icon-s-shop"></i>
                        <span slot="title">店铺管理</span>
                    </el-menu-item>

                    <!-- <el-menu-item index="2">
                        <i class="el-icon-s-custom"></i>
                        <span slot="title">服务员管理</span>
                    </el-menu-item> -->

                    <el-menu-item index="3">
                        <i class="el-icon-s-check"></i>
                        <span slot="title">送餐员管理</span>
                    </el-menu-item>


                    <el-submenu>
                        <template slot="title">
                            <i class="el-icon-s-promotion"></i>
                            <span>物流管理</span>
                        </template>
                        <el-menu-item-group>

                            <el-menu-item index="4">已完成</el-menu-item>
                            <el-menu-item index="5">进行中</el-menu-item>
                        </el-menu-item-group>

                    </el-submenu>


                    <el-submenu index="100">
                        <template slot="title">
                            <i class="el-icon-s-order"></i>
                            <span>订单管理</span>
                        </template>
                        <el-menu-item-group>

                            <el-menu-item index="6">已完成订单</el-menu-item>
                            <el-menu-item index="7">已发货订单</el-menu-item>
                            <el-menu-item index="8">未发货订单</el-menu-item>
                        </el-menu-item-group>

                    </el-submenu>
                    <el-menu-item index="2">
                        <i class="el-icon-s-custom"></i>
                        <span slot="title">退出管理员后台</span>
                    </el-menu-item>

                </el-menu>
            </div>
            <div class="main">
                <div id="manageshop" v-show="active == 1">
                    <manageshop></manageshop>
                </div>

                <!-- <div id="manageserver" v-show="active == 2">
                    <manageserver></manageserver>
                </div> -->

                <div id="managedispatcher" v-show="active == 3">
                    <managedispatcher></managedispatcher>
                </div>


                <div id="wuliuended" v-show="active == 4">
                    <wuliuended></wuliuended>
                </div>

                <div id="wuliuunended" v-show="active == 5">
                    <wuliuunended></wuliuunended>
                </div>
                <div id="ordersended" v-show="active == 6">
                    <ordersended></ordersended>
                </div>
                <div id="ordersending" v-show="active == 7">
                    <ordersending></ordersending>
                </div>

                <div id="orderunsend" v-show="active == 8">
                    <orderunsend></orderunsend>
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
    </div>
</template>

<script>
import manageshop from '@/components/ManageShop.vue'
// import manageserver from '@/components/ManageServer.vue'
import managedispatcher from '@/components/ManageDispatcher.vue'
import wuliuended from '@/components/ManageWuliu/WuliuEnded.vue'
import wuliuunended from '@/components/ManageWuliu/WuliuUnended.vue'
import ordersended from '@/components/ManageOrder/BeSended.vue'
import ordersending from '@/components/ManageOrder/BeSending.vue'
import orderunsend from '@/components/ManageOrder/UnSend.vue'
export default {
    components: {
        manageshop: manageshop,
        // manageserver: manageserver,
        managedispatcher: managedispatcher,
        wuliuended: wuliuended,
        wuliuunended: wuliuunended,
        ordersended: ordersended,
        ordersending: ordersending,
        orderunsend: orderunsend
    },
    data() {
        return {
            active: 1,
            logoutDialogVisible: false, // 控制退出登录确认弹窗的显示
        }
    },
    methods: {
        handleselect(index) {
            if (index == 2) {
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
    background:url("../assets/img/bg02.png");
    width: 85%;
    background-size:100% 100%;
}
</style>