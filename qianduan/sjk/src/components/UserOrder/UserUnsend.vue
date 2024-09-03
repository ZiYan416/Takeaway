<template>
    <div>
        <div class="header">
            未发货订单
        </div>
        <div class="body">
            <el-table :data="tabledata" style="width: 100%" class="table" border>
                <el-table-column prop="shop_name" label="店铺" min-width="20%" align="center">
                </el-table-column>
                <el-table-column prop="price" label="订单单价" min-width="13%" align="center">
                </el-table-column>
                <el-table-column prop="quantity" label="订单数量" min-width="13%" align="center">
                </el-table-column>
                <el-table-column prop="total_price" label="订单总价" min-width="13%" align="center">
                </el-table-column>
                <el-table-column prop="create_time" label="下单时间" min-width="25%" align="center">
                </el-table-column>
                <el-table-column prop="cons_name" label="订餐人姓名" min-width="15%" align="center">
                </el-table-column>
                <el-table-column prop="cons_addre" label="取餐地址" min-width="40%" align="center">
                </el-table-column>
                <el-table-column prop="operate" label="操作" min-width="40%" align="center">
                    <template slot-scope="scope">
                        <el-button size="small" type="success" @click="showdia_ch(scope.row)">修改订单
                        </el-button>
                        <el-button size="small" type="danger" @click="showdia_dl(scope.row)">取消订单
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-dialog title="修改订单" :visible.sync="dialog_chnage" width="30%">
                <el-form ref="form" :model="form_change" label-width="100px">
                    <el-form-item label="选择订单：">
                        <el-checkbox-group v-model="form_change.order_ids">
                            <el-checkbox v-for="id in form_change.all_order_ids" :label="id" :key="id">{{ id }}</el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                    <el-form-item label="订餐人姓名：">
                        <el-input v-model="form_change.cons_name"></el-input>
                    </el-form-item>
                    <el-form-item label="取餐地址：">
                        <el-input v-model="form_change.cons_addre"></el-input>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="change">
                        确认修改
                    </el-button>
                </div>
            </el-dialog>

            <el-dialog title="取消订单" :visible.sync="dialog_delete" width="30%">
                <el-form ref="form_delete" :model="form_delete" label-width="100px">
                    <el-form-item label="选择订单：">
                        <el-checkbox-group v-model="form_delete.order_ids">
                            <el-checkbox v-for="id in form_delete.all_order_ids" :label="id" :key="id">{{ id }}</el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;">
                    <el-button type="primary" @click="order_delete">
                        确定
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
        this.getdata();
        EventBus.$on('orderadded', this.getdata); // 监听订单收货事件
    },
    data() {
        return {
            tabledata: [],
            dialog_chnage: false,
            dialog_delete: false,
            form_change: {
                order_ids: [],
                all_order_ids: [],
                cons_addre: '',
                cons_name: '',
            },
            form_delete: {
                order_ids: [],
                all_order_ids: [],
            },
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/user/unsend").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tabledata = this.summarizeOrders(res.data.tabledata);
                }
            })
        },
        summarizeOrders(orders) {
            const summary = {};
            orders.forEach(order => {
                const key = `${order.shop_name}-${order.price}-${order.cons_name}-${order.cons_addre}-${order.create_time}`;
                if (!summary[key]) {
                    summary[key] = {
                        ...order,
                        order_ids: [order.order_id],
                        total_price: order.price,
                        quantity: 1
                    };
                } else {
                    summary[key].order_ids.push(order.order_id);
                    summary[key].total_price += order.price;
                    summary[key].quantity += 1;
                }
            });
            return Object.values(summary).map(order => {
                if (order.order_ids.length === 1) {
                    order.order_id = order.order_ids[0].toString();  // 单独订单显示单个ID
                } else {
                    order.order_id = `${order.order_ids[0]}-${order.order_ids[order.order_ids.length - 1]}`;  // 多个订单显示范围
                }
                order.all_order_ids = order.order_ids; // 保存所有订单ID
                return order;
            });
        },
        showdia_ch(row) {
            this.form_change.order_ids = [...row.order_ids];
            this.form_change.all_order_ids = row.all_order_ids;
            this.form_change.cons_name = row.cons_name;
            this.form_change.cons_addre = row.cons_addre;
            this.dialog_chnage = true;
        },
        change() {
            this.$axios.post("/api/user/unsend", this.form_change).then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.$message({
                        message: res.data.msg,
                        type: "success"
                    });
                    this.getdata();
                    this.dialog_chnage = false;
                }
            })
        },
        showdia_dl(row) {
            this.form_delete.order_ids = [...row.order_ids];
            this.form_delete.all_order_ids = row.all_order_ids;
            this.dialog_delete = true;
        },
        order_delete() {
            this.$axios.delete("/api/user/unsend", { data: { delete_ids: this.form_delete.order_ids } }).then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.$message({
                        message: res.data.msg,
                        type: "success"
                    });
                    this.getdata();
                    this.dialog_delete = false;
                }
            })
        }
    },
    beforeDestroy() {
        EventBus.$off('orderadded', this.getdata); // 组件销毁前取消事件监听
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

.table {
    /* margin-left: 50px; */
}
</style>
