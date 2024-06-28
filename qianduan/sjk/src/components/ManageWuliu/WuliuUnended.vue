<template>
    <div>
        <div class="header">
            进行中物流
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table">
                <el-table-column prop="order_id" label="订单编号" width="200" align="center">
                </el-table-column>
                <el-table-column prop="cons_phone" label="顾客电话" width="200" align="center">
                </el-table-column>
                <el-table-column prop="disp_id" label="送餐员编号" width="200" align="center">
                </el-table-column>
                <el-table-column prop="deliver_time" label="预计送餐时间" width="200" align="center">
                </el-table-column>
                <el-table-column label="操作" width="120" align="center">
                    <template slot-scope="scope">
                        <el-button type="success" size="small" @click="confirmReceipt(scope.row)">确认收货</el-button>
                    </template>
                </el-table-column>
            </el-table>


        </div>
    </div>
</template>

<script>
import { EventBus } from '@/eventBus'; // 引入事件总线
export default {
    created() {
        this.getdata();
        EventBus.$on('orderSending', this.getdata); // 监听派发订单事件
    },
    data() {
        return {
            tableData: [],

        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/wuliu?id=0").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        },

        confirmReceipt(row) {
            this.$prompt('请输入实际送餐时间 (分钟)', '确认收货', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputPattern: /^[1-9]\d*分钟$/,
                inputErrorMessage: '请输入有效的分钟数'
            }).then(({ value }) => {
                this.$axios.post("/api/user/confirm-receipt", {
                    order_id: row.order_id,
                    actual_deliver_time: value
                }).then((res) => {
                    if (res.data.status == 200) {
                        this.$message.success('确认收货成功');
                        this.getdata(); // 刷新表格数据

                        // 收货成功后，发送事件通知WuliuEnded组件更新
                        EventBus.$emit('orderSended');
                    } else if (res.data.status == 400) {
                        this.$message.error('订单ID缺失');
                    } else if (res.data.status == 404) {
                        this.$message.error('订单不存在');
                    } else if (res.data.status == 500) {
                        this.$message.error('数据库错误');
                    } else {
                        this.$message.error('确认收货失败');
                    }
                });
            }).catch(() => {
                this.$message.info('已取消确认');
            });
        }
    },
    beforeDestroy() {
        EventBus.$off('orderDispatched', this.getdata); // 组件销毁前取消事件监听
    }
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

    width: 68%;
    margin: auto;
    margin-top: 30px;
}
</style>