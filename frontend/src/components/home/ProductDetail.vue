
<template>
  <v-dialog v-model="activeInternal" max-width="500">
    <v-card>
      <v-card-title v-if="!isCreateProduct">{{ `${product.id} - ${product.name}` }}</v-card-title>
      <v-card-title v-else>Criar Produto</v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col
              cols="12"
              md="6"
              sm="6"
          >
            <v-text-field
                label="Nome"
                required
                :model-value="updateProductData?.name"
                @update:model-value="updateField('name', $event)"
            />
          </v-col>
          <v-col
              cols="12"
              md="6"
              sm="6"
          >
            <v-text-field
                label="Preço"
                required
                type="number"
                prefix="R$"
                :model-value="updateProductData?.price"
                @update:model-value="updateField('price', $event)"

            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
              cols="12"
              md="12"
              sm="12"
          >
            <v-textarea
                label="Descrição"
                required
                :model-value="updateProductData?.description"
                @update:model-value="updateField('description', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-file-input
              label="Enviar imagem"
              show-size
              accept="image/*"
              @update:model-value="updateImage"
          />
        </v-row>
        <v-row>
          <v-img
              :class="$style.productImage"
              :src="previewUrl || `http://localhost:8000/${updateProductData.image}`"
          />
        </v-row>
      </v-card-text>

      <v-card-actions>

        <v-btn v-if="!isCreateProduct" text="Atualizar" prepend-icon="mdi-check-circle" @click="createUpdateProduct"/>
        <v-btn v-else text="Criar" prepend-icon="mdi-plus" @click="createUpdateProduct"/>

        <v-spacer v-if="!isCreateProduct"/>
        <v-btn v-if="!isCreateProduct" text="Excluir" prepend-icon="mdi-trash-can-outline" @click="deleteProductF"/>
        <v-spacer/>

        <v-btn prepend-icon="mdi-close" text="Cancelar" @click="closeDialog"/>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>



<script>
import {createProduct, deleteProduct, updateProduct} from "@/api/api.ts";

export default {
  props: {
    product: {
      type: Object,
      required: true,
    },
    active: {
      type: Boolean,
      default: true,
    },
    isCreateProduct:{
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      updateProductData: { ...this.product },
      selectedImage: null,
      previewUrl: null,
    };
  },
  watch: {
    product: {
      handler(value) {
        this.updateProductData = { ...value };
      },
      deep: true,
    },
  },
  computed: {
    activeInternal: {
      get() {
        return this.active;
      },
      set(value) {
        this.updateProductData = { ...this.product };
        this.$emit("update:isCreateProduct", false);
        this.$emit("update:active", value);
      },
    },
  },
  methods: {
    deleteProduct,
    updateField(field, value) {
      this.updateProductData[field] = value;
    },
    async createUpdateProduct() {
      if (this.isCreateProduct){
        await createProduct({
          name: this.updateProductData.name,
          price: this.updateProductData.price,
          description: this.updateProductData.description,
          image: this.selectedImage,
        }).then(() => {
          this.$emit("update:active", false);
          this.$emit("update:isCreateProduct", false);
          this.$emit("update:shouldUpdate");
          URL.revokeObjectURL(this.previewUrl);
          this.previewUrl = null;
        })
        return
      }
      await updateProduct(this.updateProductData.id, {
        name: this.updateProductData.name,
        price: this.updateProductData.price,
        description: this.updateProductData.description,
        image: this.selectedImage,
      }).then(() => {
        this.$emit("update:active", false);
        this.$emit("update:shouldUpdate", true);
        URL.revokeObjectURL(this.previewUrl);
        this.previewUrl = null;
      });

    },
    updateImage(file) {
      if (!file) return;
      this.selectedImage = file;
      this.previewUrl = URL.createObjectURL(file);
    },
    async deleteProductF() {
      await this.deleteProduct(this.product.id).then(() => {
        this.$emit("update:active", false);
      });
    },
    closeDialog() {
      URL.revokeObjectURL(this.previewUrl);
      this.previewUrl = null;
      this.updateProductData = { ...this.product };
      this.$emit("update:isCreateProduct", false);
      this.$emit("update:active", false);
    },
  },
};
</script>


<style module>
.productImage{
  display: block;
  border-radius: 10px;
  margin: 10px auto;
}

.productImage img {
  max-width: 500px;

}
</style>