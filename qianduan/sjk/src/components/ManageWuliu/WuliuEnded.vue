<template>
    <div>
        <div class="header">
            已完成物流
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table">
                <el-table-column prop="order_id" label="订单编号" width="200" align="center">
                </el-table-column>
                <el-table-column prop="cons_phone" label="顾客电话" width="200" align="center">
                </el-table-column>
                <el-table-column prop="disp_id" label="送餐员编号" width="200" align="center">
                </el-table-column>
                <el-table-column prop="deliver_time" label="送餐时间" width="200" align="center">
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
import { EventBus } from '@/eventBus'; // 引入事件总线
export default {
    created() {
        this.getdata()
        EventBus.$on('orderSended', this.getdata); // 监听订单收货事件
    },
    data() {
        return {
            tableData: [],
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/wuliu?id=1").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = this.summarizeOrders(res.data.tabledata);
                }
            })
        },
        summarizeOrders(orders) {
            const summary = {};
            orders.forEach(order => {
                const key = `${order.cons_phone}-${order.disp_id}-${order.deliver_time}`;
                if (!summary[key]) {
                    summary[key] = {
                        ...order,
                        order_ids: [order.order_id]
                    };
                } else {
                    summary[key].order_ids.push(order.order_id);
                }
            });
            return Object.values(summary).map(order => {
                if (order.order_ids.length === 1) {
                    order.order_id = order.order_ids[0].toString();  // 单独订单显示单个ID
                } else {
                    order.order_id = `${order.order_ids[0]}-${order.order_ids[order.order_ids.length - 1]}`;  // 多个订单显示范围
                }
                return order;
            });
        }
    },
    beforeDestroy() {
        EventBus.$off('orderSended', this.getdata); // 组件销毁前取消事件监听
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
    width: 62%;
    margin: auto;
    margin-top: 30px;
}
</style>
