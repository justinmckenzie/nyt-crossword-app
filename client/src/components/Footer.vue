<template>
  <footer>
    <p>{{ new Date().getFullYear() }} <span>&copy; All rights reserved</span></p>
    <p>Created By Justin McKenzie</p>
  </footer>
</template>

<style lang="scss">
  footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: $PRIMARY_500;
  }
</style>