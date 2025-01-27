<template>
  <main :class="$style.container" @contextmenu.prevent>
    <h1>Produtos</h1>
    <div :class="$style.buttonsContainer">
      <v-btn v-if="selectingProducts" prepend-icon="mdi-close" @click="stopSelectingProducts">Cancelar seleção</v-btn>
      <v-btn v-if="selectingProducts" prepend-icon="mdi-trash-can-outline" @click="deleteSelectedProducts">Deletar produtos selecionados</v-btn>
      <v-btn prepend-icon="mdi-plus" @click="openCreateProduct">Cadastrar produto</v-btn>
    </div>
    <ProductDetail
        :active="productDetailVisible"
        :product="selectedProduct"
        :isCreateProduct="isCreateProduct"
        @update:shouldUpdate="handleUpdate"
        @update:active="toggleProductDetail"
        @update:isCreateProduct="closeCreateProduct"
    />
    <ProductsTable
        :selectedProduct="selectedProduct"
        :selectingProducts="selectingProducts"
        :selected-products="selectedProducts"
        :shouldUpdate="shouldUpdate"
        @update:selectedProduct="updateSelectedProduct"
        @update:toggleDetail="toggleProductDetail"
        @update:toggleProductSelection="toggleProductSelection"
        @update:openContextMenu="openContextMenu"
        @update:selectedProducts="addSelectedProduct"
    />
    <ContextMenu
        :menu="menu"
        :isOpen="isContextMenuOpen"
        :isSelecting="selectingProducts"
        @update:isOpen="closeContextMenu"
        @update:selectMultiple="startSelectingProducts"
    />
  </main>
</template>


<script lang="ts">
import ProductsTable from '@/components/home/ProductsTable.vue'
import ProductDetail from "@/components/home/ProductDetail.vue";
import ContextMenu from "@/components/home/ContextMenu.vue";
import {deleteMultipleProducts} from "@/api/api.ts";

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
      selectedProducts: [],
      shouldUpdate: false,
      productDetailVisible: false,
      isCreateProduct: false,
      isContextMenuOpen: false,
      menu:{
        x: 0,
        y: 0,
      }
    }
  },
  components: {
    ContextMenu,
    ProductsTable,
    ProductDetail
  },
  methods: {
    updateSelectedProduct(product) {
      this.selectedProduct = product;
    },
    startSelectingProducts() {
      this.selectingProducts = true;
    },
    handleUpdate() {
      this.shouldUpdate = true;
      setTimeout(() => {
        this.shouldUpdate = false;
      }, 100);
    },
    stopSelectingProducts() {
      this.selectedProducts = [];
      this.selectingProducts = false;
    },
    toggleProductDetail(value) {
      if (this.selectingProduct) return;
      this.productDetailVisible = value;
    },
    toggleProductSelection() {
      this.selectingProduct = !this.selectingProduct;
    },
    closeCreateProduct() {
      this.isCreateProduct = false;
    },
    openCreateProduct() {
      this.selectedProduct = productModel;
      this.toggleProductDetail(true);
      this.isCreateProduct = true;
    },
    openContextMenu(event,id) {
      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;
      const offsetX = 170;
      const offsetY = 245;
      const clickX = event.clientX;
      const clickY = event.clientY;
      this.menu.x = clickX >= screenWidth - offsetX ? clickX - offsetX : clickX;
      this.menu.y = clickY >= screenHeight - offsetY ? clickY - offsetY : clickY;
      this.isContextMenuOpen = true;
    },
    closeContextMenu() {
      this.isContextMenuOpen = false;
    },
    addSelectedProduct(id) {
      if (this.selectedProducts.includes(id)) {
        this.selectedProducts = this.selectedProducts.filter((productId) => productId !== id);
        return;
      }
      this.selectedProducts.push(id);
    },
    deleteSelectedProducts(){
      deleteMultipleProducts(this.selectedProducts).then(() => {
        this.selectedProducts = [];
        this.handleUpdate();
      })
    }
  },
}
</script>

<style module>

.container{
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1200px;
}

.buttonsContainer{
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: end;
  gap: 10px;
  margin-bottom: 10px;
}

</style>