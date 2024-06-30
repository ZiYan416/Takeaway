<template>
    <div>
        <div class="header">
            已发货订单
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table" border>
                <el-table-column prop="order_id" label="订单编号" width="100" align="center">
                </el-table-column>
                <el-table-column prop="shop_name" label="店铺" width="160" align="center">
                </el-table-column>
                <el-table-column prop="order_money" label="订单单价" width="80" align="center">
                </el-table-column>
                <el-table-column prop="quantity" label="订单数量" width="80" align="center">
                </el-table-column>
                <el-table-column prop="total_price" label="订单总价" width="80" align="center">
                </el-table-column>
                <el-table-column prop="cons_phone" label="订餐人电话" width="140" align="center">
                </el-table-column>
                <el-table-column prop="cons_name" label="订餐人姓名" width="130" align="center">
                </el-table-column>
                <el-table-column prop="cons_addre" label="取餐地址" width="180" align="center">
                </el-table-column>
                <el-table-column prop="disp_id" label="送餐员编号" width="120" align="center">
                </el-table-column>
                <el-table-column prop="deliver_time" label="预计送餐时间" width="110" align="center">
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata()
    },
    data() {
        return {
            tableData: [],
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/sending").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = this.summarizeOrders(res.data.tabledata);
                }
            })
        },
        summarizeOrders(orders) {
            const summary = {};
            orders.forEach(order => {
                const key = `${order.shop_name}-${order.order_money}-${order.cons_phone}-${order.cons_name}-${order.cons_addre}-${order.disp_id}-${order.deliver_time}`;
                if (!summary[key]) {
                    summary[key] = {
                        ...order,
                        order_ids: [order.order_id],
                        total_price: order.order_money,
                        quantity: 1
                    };
                } else {
                    summary[key].order_ids.push(order.order_id);
                    summary[key].total_price += order.order_money;
                    summary[key].quantity += 1;
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
    width: 84%;
    margin: auto;
    margin-top: 30px;
}
</style>
