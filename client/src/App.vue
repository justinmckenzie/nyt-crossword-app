<template>
  <div id="app">
    <div>
      <NavBar />
      <div id="app-container">
        <router-view />
      </div>
      <Footer />
    </div>
  </div>
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