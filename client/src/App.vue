<template>
  <NavBar />
  <main id="app-container">
    <router-view />
  </main>
  <Footer />
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "app",
  components: {
    NavBar,
    Footer,
  },
};
</script>

<style scoped lang="scss">
#app-container {
  max-width: $BREAKPOINT_XXL;
  padding: 32px 16px;
  align-self: center;
  display: flex;
  flex-direction: column;
  width: 100%;
  flex: 1;

  @media (min-width: $BREAKPOINT_SM) {
    padding: 48px 32px;
  }

  @media (min-width: $BREAKPOINT_MD) {
    padding: 64px 48px;
  }
}
</style>
