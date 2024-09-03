<template>
    <div>
        <div class="header">
            店铺列表
        </div>
        <div class="body">
            <el-table :data="shopList" style="width: 100%" class="table" border>
                <el-table-column prop="name" label="店铺名称" min-width="20%" align="center">
                </el-table-column>
                <el-table-column prop="rating" label="评分" min-width="30%" align="center">
                </el-table-column>
                <el-table-column prop="address" label="地址" min-width="30%" align="center">
                </el-table-column>
                <el-table-column label="操作" min-width="20%" align="center">
                    <template v-slot="scope">
                        <el-button type="primary" @click="viewShopDetails(scope.row.id)">查看详情</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.fetchShopList();
    },
    data() {
        return {
            shopList: [],
        }
    },
    methods: {
        fetchShopList() {
            this.$axios.get("/api/shops").then((res) => {
                if (res.data.status === 200) {
                    this.shopList = res.data.shops;
                }
            }).catch((error) => {
                console.error("无法获取店铺列表", error);
            });
        },
        viewShopDetails(shopId) {
            this.$router.push(`/shop-details/${shopId}`);
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
    width: 75%;
    margin: auto;
    margin-top: 30px;
}
</style>
