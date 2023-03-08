<template>
  <NavBar />
  <main id="app-container">
    <router-view />
  </main>
  <Footer />
</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  import Footer from '@/components/Footer.vue'

  export default {
    name: 'app',
    components: {
      NavBar,
      Footer,
    },
  }
</script>

<style lang="scss">
  #app-container {
    max-width: $BREAKPOINT_XXL;
    padding: 64px 48px;
    margin-right: auto;
    margin-left: auto;
    margin-top: 90px;
    height: 100%;

    @media (max-width: $BREAKPOINT_MD) {
      padding: 48px 32px;
    }

    @media (max-width: $BREAKPOINT_SM) {
      padding: 32px 16px;
    }
  }
</style>