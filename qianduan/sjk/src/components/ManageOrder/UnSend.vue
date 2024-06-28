<template>
    <div>
        <div class="header">
            未发货订单
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table" border>
                <el-table-column prop="order_id" label="订单编号" width="80" align="center">
                </el-table-column>
                <el-table-column prop="shop_name" label="店铺" width="100" align="center">
                </el-table-column>
                <el-table-column prop="price" label="订单价格" width="80" align="center">
                </el-table-column>
                <el-table-column prop="create_time" label="下单时间" width="200" align="center">
                </el-table-column>
                <!-- <el-table-column prop="orderway" label="订餐方式" width="100" align="center">
                </el-table-column> -->
                <el-table-column prop="cons_phone" label="订餐人电话" width="200" align="center">
                </el-table-column>
                <el-table-column prop="cons_name" label="订餐人姓名" width="100" align="center">
                </el-table-column>
                <el-table-column prop="cons_addre" label="取餐地址" width="200" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="派发订单" width="127" align="center">
                    <template slot-scope="scope">
                        <el-button size="small" type="success" @click="show_dialog(scope.row)">派发此订单
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="派发订单" :visible.sync="dialog" width="30%">
                <el-form ref="form" :model="form" label-width="120px">

                    <el-form-item label="选择送餐员：" prop="">
                        <el-select v-model="form.dispatcher_id" placeholder="请选择送餐员编号">

                            <el-option v-for="(item, index)  in disp_range" :key="index" :label="item.disp_id"
                                :value="item.disp_id"></el-option>
                        </el-select>

                    </el-form-item>
                    <el-form-item label="预计送货时间（分钟）：">
                        <el-input v-model="form.deliver_time"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="add()">
                        确定派发
                    </el-button>
                </div>
            </el-dialog>

        </div>
    </div>
</template>

<script>
import { EventBus } from '@/eventBus'; // 引入事件总线
export default {
    created() {
        this.getdata()
    },
    data() {
        return {
            tableData: [],
            dialog: false,
            form: {
                dispatcher_id: '',
                order_id: '',
                deliver_time: '',
            },
            disp_range: [],
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/unsend").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = this.summarizeOrders(res.data.tabledata);
                    this.disp_range = res.data.disp_range;
                }
            })
        },
        summarizeOrders(orders) {
            const summary = {};
            orders.forEach(order => {
                const key = `${order.shop_name}-${order.price}-${order.cons_phone}-${order.cons_name}-${order.cons_addre}-${order.create_time}`;
                if (!summary[key]) {
                    summary[key] = {
                        ...order,
                        order_ids: [order.order_id],
                        total_price: order.price
                    };
                } else {
                    summary[key].order_ids.push(order.order_id);
                    summary[key].total_price += order.price;
                }
            });
            return Object.values(summary).map(order => {
                if (order.order_ids.length === 1) {
                    order.order_id = order.order_ids[0].toString();  // 单独订单显示单个ID
                } else {
                    order.order_id = `${order.order_ids[0]}-${order.order_ids[order.order_ids.length - 1]}`;  // 多个订单显示范围
                }
                order.price = order.total_price; // 显示总价格
                return order;
            });
        },
        show_dialog(row) {
            // 将 order_id 字符串转换为数组
            const order_id_range = row.order_id.split('-').map(id => parseInt(id, 10));
            const order_ids = [];
            for (let i = order_id_range[0]; i <= order_id_range[order_id_range.length - 1]; i++) {
                order_ids.push(i);
            }
            this.form.order_ids = order_ids;
            this.dialog = true;
        },
        add() {
            const formData = {
                ...this.form
            };
            this.$axios.post("/api/manager/unsend", formData).then((res) => {
                if (res.data.status === 200) {
                    this.$message({
                        message: res.data.msg,
                        type: "success"
                    });
                    this.dialog = false;
                    this.getdata(); // 刷新表格数据

                    // 派发成功后，发送事件通知WuliuUnended组件更新
                    EventBus.$emit('orderSending');
                } else {
                    this.$message({
                        message: res.data.msg,
                        type: "error"
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
    width: 91%;
    margin: auto;
    margin-top: 30px;
}
</style>