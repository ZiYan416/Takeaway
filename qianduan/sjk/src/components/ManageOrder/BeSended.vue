<template>
    <div>
        <div class="header">
            已完成订单
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table" border>
                <el-table-column prop="order_id" label="订单编号" width="80" align="center">
                </el-table-column>
                <el-table-column prop="shop_name" label="店铺" width="120" align="center">
                </el-table-column>
                <el-table-column prop="order_money" label="订单单价" width="80" align="center">
                </el-table-column>
                <el-table-column prop="quantity" label="订单数量" width="80" align="center">
                </el-table-column>
                <el-table-column prop="total_price" label="订单总价" width="80" align="center">
                </el-table-column>
                <el-table-column prop="cons_phone" label="订餐人电话" width="130" align="center">
                </el-table-column>
                <el-table-column prop="cons_name" label="订餐人姓名" width="100" align="center">
                </el-table-column>
                <el-table-column prop="cons_addre" label="取餐地址" width="140" align="center">
                </el-table-column>
                <el-table-column prop="disp_id" label="送餐员编号" width="120" align="center">
                </el-table-column>
                <el-table-column prop="deliver_time" label="实际送餐时间" width="120" align="center">
                </el-table-column>
                <el-table-column label="操作" width="140" align="center">
                    <template slot-scope="scope">
                        <el-button type="danger" size="mini" @click="confirmDelete(scope.row)">删除订单</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 删除确认弹窗 -->
            <el-dialog
                title="确认删除"
                :visible.sync="deleteDialogVisible"
                width="30%"
                @close="deleteDialogVisible = false">
                <el-checkbox-group v-model="selectedOrderIds">
                    <el-checkbox v-for="id in currentOrderIds" :label="id" :key="id">{{ id }}</el-checkbox>
                </el-checkbox-group>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="deleteDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="deleteOrder">确认</el-button>
                </span>
            </el-dialog>

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
            deleteDialogVisible: false,
            currentOrderIds: [], // 当前要删除的订单ID数组
            selectedOrderIds: [] // 被选中的要删除的订单ID数组
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/sended").then((res) => {
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
        },
        confirmDelete(row) {
            this.currentOrderIds = row.order_ids;
            this.selectedOrderIds = [...this.currentOrderIds]; // 默认全选
            this.deleteDialogVisible = true;
        },
        deleteOrder() {
            this.$axios.delete(`/api/manager/sended`, { data: { order_ids: this.selectedOrderIds } }).then((res) => {
                if (res.data.status == 200) {
                    this.$message({
                        type: 'success',
                        message: '删除成功!'
                    });
                    this.getdata(); // 重新获取数据，更新表格
                    this.deleteDialogVisible = false; // 关闭弹窗
                } else {
                    this.$message({
                        type: 'error',
                        message: '删除失败!'
                    });
                }
            })
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
    width: 85%;
    margin: auto;
    margin-top: 30px;
}
</style>
