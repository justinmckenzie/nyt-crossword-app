<template v-show="error.status || loading.status">
  <div v-show="error.status" class="error">
    <FontAwesomeIcon icon="fa-solid fa-circle-exclamation" />
    <p>{{ error.message }}</p>
  </div>
  <div v-show="loading.status" class="loading">
    <FontAwesomeIcon class="loading-spinner" icon="fa-solid fa-spinner" />
    <p>{{ loading.message }}</p>
  </div>
</template>

<script>
export default {
  name: "Overlay",
  // TODO: prop validation
  props: ["error", "loading"],
};
</script>

<style scoped lang="scss">
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;

  svg {
    height: 24px;
    width: 24px;
    margin-bottom: 16px;
  }

  p {
    text-align: center;
  }

  &.loading {
    svg {
      margin-bottom: 24px;
      animation-name: spin;
      animation-duration: 2000ms;
      animation-iteration-count: infinite;
      animation-timing-function: linear;
    }
  }

  @media (min-width: $BREAKPOINT_SM) {
    svg {
      height: 32px;
      width: 32px;
      margin-bottom: 24px;
    }
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
