
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
  },
  data() {
    return {
      itemsPerPage: 10,
      products: [],
      selectedItems: [],
      totalItems: 0,
      loading: true,
      search:'',
      headers: [
        { title: 'Id', key: 'id', align: 'center'},
        { title: 'Nome', key: 'name', align: 'end' },
        { title: 'Preço', key: 'price', align: 'end' },
      ],
    }
  },
  watch: {
    search (e) {
      this.search = e
    },
  },
  methods:{
    rowClick(e, item){
      if (this.selectingProducts){
        const currentItem = item.item.id
        this.selectedItems.includes(currentItem) ?
            this.selectedItems.splice(this.selectedItems.indexOf(currentItem), 1) :
            this.selectedItems.push(currentItem);
        return
      }
      this.$emit('update:selectedProduct', item.item );
      this.$emit('update:toggleDetail',true)
    },
    async loadItems(event) {
      console.log(event)
      this.loading = true;
      await getProducts().then((response) => {
        this.products = response.data;
        this.loading = false;
        this.totalItems = this.products.length;
      }).catch((error) => {
        console.log(error);
      });
    },
  },
  async mounted() {
    await getProducts().then((response) => {
      this.products = response.data;
      this.totalItems = this.products.length;
      this.loading = false;
    }).catch((error) => {
      console.log(error);
    });
  },


}

</script>

<template>
  <h2>{{search}}</h2>
  <h2>{{selectedItems}}</h2>
  <v-data-table-server
      height="900px"
      fixed-header
      item-value="id"
      v-model="selectedItems"
      v-model:items-per-page="itemsPerPage"
      :class="$style.productTable"
      :show-select="selectingProducts"
      :headers="headers"
      :items="products"
      :items-length="totalItems"
      :loading="loading"
      :row-props="{ class: $style.productRow }"
      @click:row="rowClick"
      @update:options="loadItems"
  >
    <template v-slot:tfoot>
      <tr>
        <td/>
        <td>
          <v-text-field v-model="search" class="ma-2" density="compact" placeholder="Search name..." hide-details></v-text-field>
        </td>
      </tr>
    </template>
  </v-data-table-server>
</template>
<script setup lang="ts">
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
  border-collapse: collapse;
  border-radius: 10px;
}

</style>