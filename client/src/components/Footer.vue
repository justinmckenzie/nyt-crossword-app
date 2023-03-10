<template>
  <footer>
    <p>{{ new Date().getFullYear() }} <span>&copy; By Justin McKenzie</span></p>
    <a href="https://github.com/justinmckenzie/nyt-crossword-stats">
      <FontAwesomeIcon icon="fa-brands fa-github" />
    </a>
  </footer>
</template>

<style lang="scss">
footer {
  margin-top: auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: $PRIMARY_500;
  padding: 16px 24px;

  p {
    text-align: center;
    font-size: 14px;
  }

  a {
    color: inherit;
    text-decoration: none;

    svg {
      margin-top: 16px;

      path {
        fill: $WHITE;
      }
    }
  }

  @media (min-width: $BREAKPOINT_SM) {
    padding: 24px 32px;
    flex-direction: row;
    justify-content: space-between;

    p {
      font-size: 16px;
    }

    a {
      svg {
        margin: 0;
        height: 24px !important;
      }
    }
  }
}
</style>
