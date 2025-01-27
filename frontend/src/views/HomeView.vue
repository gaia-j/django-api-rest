<script lang="ts">
import ProductsTable from '@/components/home/ProductsTable.vue'
import ProductDetail from "@/components/home/ProductDetail.vue";
import {createProduct} from "../api/api.ts";

let productModel = {
  id: 0,
  name: "",
  description: "",
  price: 0,
  image: "",
};

export default {
  data(){
    return {
      selectingProducts: false,
      selectedProduct: productModel,
      productDetailVisible: false,
      createProduct: false,
    }
  },
  components: {
    ProductsTable,
    ProductDetail
  },
  methods: {
    createProduct,
    updateSelectedProduct(product) {
      this.selectedProduct = product;
    },
    toggleProductDetail(value) {
      if (this.selectingProduct) return;
      this.productDetailVisible = value;
    },
    toggleProductSelection() {
      this.selectingProduct = !this.selectingProduct;
    },
    closeCreateProduct() {
      this.createProduct = false;
    },
    openCreateProduct() {
      this.selectedProduct = productModel;
      this.toggleProductDetail(true);
      this.createProduct = true;
    },
  },
}
</script>

<template>
  <main :class="$style.container" @contextmenu.prevent>
    <h1>Home</h1>
    <button @click="openCreateProduct">Create Product</button>
    <h1>{{createProduct}}</h1>
    <ProductDetail
        :active="productDetailVisible"
        :product="selectedProduct"
        :isCreateProduct="createProduct"
        @update:active="toggleProductDetail"
        @update:isCreateProduct="closeCreateProduct"
    />
    <ProductsTable
        :selectedProduct="selectedProduct"
        :selectingProducts="selectingProducts"
        @update:selectedProduct="updateSelectedProduct"
        @update:toggleDetail="toggleProductDetail"
        @update:toggleProductSelection="toggleProductSelection"
    />
  </main>
</template>


<style module>

.container{
  min-width: 100%;
}

</style>