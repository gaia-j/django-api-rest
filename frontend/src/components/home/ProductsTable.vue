
<template>
  <v-data-table-server
      fixed-header
      item-value="id"
      v-model="selectedProductsInternal"
      v-model:items-per-page="itemsPerPage"
      :class="$style.productTable"
      :show-select="selectingProducts"
      :headers="headers"
      :items="products"
      :items-length="totalItems"
      :loading="loading"
      :search="search"
      :row-props="{ class: $style.productRow }"
      @click:row="rowClick"
      @contextmenu:row="handleRightClick"
      @update:options="loadItems"
  >
    <template v-slot:item.price="{ item }">
      {{ formatPrice(item.price) }}
    </template>
    <template v-slot:footer.prepend>
      <v-text-field v-model="search" class="ma-2" density="compact" placeholder="Buscar produto..." hide-details></v-text-field>
    </template>
  </v-data-table-server>
</template>


<script>
import {getProducts} from "@/api/api.ts";

export default {
  props: {
    selectedProduct: {
      type: Object,
      required: true,
    },
    selectingProducts: {
      type: Boolean,
      required: true,
    },
    selectedProducts: {
      type: Array,
      required: true,
    },
    shouldUpdate: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      itemsPerPage: 10,
      products: [],
      totalItems: 0,
      loading: true,
      filterQuery: '',
      search:'',
      headers: [
        { title: 'Id', key: 'id', align: 'center'},
        { title: 'Nome', key: 'name', align: 'end' },
        { title: 'Preço', key: 'price', align: 'end' },
      ],
    }
  },
  methods:{
    handleRightClick(e, item){
      this.$emit('update:openContextMenu', e, item.item.id)
    },
    rowClick(e, item){
      if (this.selectingProducts){
        this.$emit('update:selectedProducts', item.item.id );
        return
      }
      this.$emit('update:selectedProduct', item.item );
      this.$emit('update:toggleDetail',true)
    },
    async loadItems(event) {
      this.loading = true;
      let sortBy = '';
      if (event) {
        sortBy = JSON.stringify(event.sortBy)
        this.filterQuery = `?page=${event.page}&itemsPerPage=${event.itemsPerPage}&search=${this.search}&sortBy=${sortBy}`
      }
      await getProducts(this.filterQuery).then((response) => {
        let res = response.data;
        res.results.forEach((product) => {
          product.price = product.price/100;
        });
        this.products = res.results;
        this.totalItems = res.count;
        this.loading = false;
      })
    },
    formatPrice(price) {
      return `R$ ${price.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    },
  },
  computed: {
    selectedProductsInternal: {
      get() {
        return this.selectedProducts;
      },
      set(value) {
        console.log(this.selectedProductsInternal)
      },
    },
  },
  watch: {
    selectedProducts: {
      handler(newValue) {
        this.selectedProductsInternal = newValue;
      },
      deep: true,
    },
    shouldUpdate(value) {
      if (value) this.loadItems(null);
    }
  },
  async mounted() {
    await getProducts().then((response) => {
      let res = response.data;
      res.results.forEach((product) => {
        product.price = product.price/100;
      });
      this.products = res.results;
      this.totalItems = res.count;
      this.loading = false;
    })
  },
}
</script>


<style module>
.productRow{
  border-bottom: 1px solid rgba(221, 221, 221, 0.34);
  transition: background-color 0.2s;
  &:hover{
    background-color: rgba(59, 16, 99, 0.55);
  }
}

td{
  padding: 8px;
  text-align: center;
}

.productTable{
  width: 100%;
  height: 600px;
  border-collapse: collapse;
  border-radius: 10px;
}

</style>