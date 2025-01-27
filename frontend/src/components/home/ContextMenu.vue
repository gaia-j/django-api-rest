<template>
  <div class="d-flex justify-space-around">
    <div
        v-if="isOpenInternal"
        :class="$style.overlay"
        @click="closeMenu"
    />
    <v-menu
        v-model="isOpenInternal"
        :class="$style.contextMenu"
        :style="{ top: `${menu.y}px`, left: `${menu.x}px` }"
    >
      <v-list>
        <v-list-item value="select" prepend-icon="mdi-format-list-checks" @click="selectMultiple">
          <v-list-item-title>Selecionar vários</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
export default {
  props: {
    menu: {
      type: Object,
      required: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    isSelecting: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    closeMenu() {
      this.$emit('update:isOpen', false)
    },
    selectMultiple() {
      this.$emit('update:selectMultiple')
    },
  },
  computed: {
    isOpenInternal: {
      get() {
        return this.isOpen
      },
      set(value) {
        this.$emit('update:isOpen', value)
      },
    },
  },
}
</script>

<style module>
.contextMenu{
  position: absolute;
  z-index: 1000;
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  z-index: 999;
}
</style>