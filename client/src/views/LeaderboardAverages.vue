<template>
  <section>
    <h2>Leader Board Averages - Mini Only</h2>
    <p class="subtitle">(Data pulled from the last 31 days)</p>
    <template v-if="isLoading">
      <div class="loading-container">
        <FontAwesomeIcon class="loading-spinner" icon="fa-solid fa-spinner" />
        <p>Crunching the numbers...</p>
      </div>
    </template>
    <template v-else>
      <ul class="averages-results">
        <li
          v-for="person in data"
          :key="person.name"
        >
          <div class="result-container">
            <p class="name">{{ person.name }}</p>
            <span class="average">{{ new Date(person.data.average * 1000).toISOString().substring(14, 19) }}</span>
            <div class="result-metadata">
              <p>Puzzles Completed: {{ person.data.completed }}</p>
              <p>In Progress: {{ person.data.in_progress }}</p>
              <p>Not Started: {{ person.data.not_started }}</p>
            </div>
          </div>
        </li>
      </ul>
    </template>
  </section>
</template>

<script>
  export default {
    name: 'Leaderboard',
    data() {
      return {
        data: [],
        isLoading: false,
      };
    },
    created: function () {
      this.fetchData();
    },
    methods: {
      fetchData: async function () {
        this.isLoading = true;
        const req = await fetch(`http://localhost:5000/leaderboard-averages`);
        const { data } = await req.json();
        this.isLoading = false;
        return this.data = this.sortLeaderboard(data);
      },
      sortLeaderboard: function (data) {
        console.log('data', data);
        const lbData = data;
        return lbData.sort((a, b) => {
          if (a['data'].average === 0) return 1;
          if (b['data'].average === 0) return -1;
          return a['data'].average - b['data'].average;
        });
      }
    },
};
</script>

<style scoped lang="scss">
  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;

    h2 {
      font-size: 32px;
    }

    .subtitle {
      margin-top: 16px;
    }

    ul {
      list-style-type: none;
    }

    .averages-results {
      display: flex;
      margin-top: 24px;
      .result-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        border: 1px solid $PRIMARY_100;
        box-shadow: 0px 4px 10px -4px rgba(0, 30, 43, 0.3);
        border-radius: 24px;
        padding: 32px;
        margin: 0 16px;

        .name {
          font-size: 20px;
        }

        .average {
          font-size: 48px;
          font-family: 'Montserrat-Bold';
          color: $PRIMARY_600;
          margin: 16px 0;
        }

        .result-metadata {
          p {
            font-size: 12px;
            margin: 6px 0;
            color: $GRAYSCALE_600;
          }
        }
      }
    }

    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;

      svg {
        height: 32px;
        width: 32px;
        margin-bottom: 24px;
        animation-name: spin;
        animation-duration: 2000ms;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
      }
    }
  }

  @keyframes spin {
    from {transform:rotate(0deg);}
    to {transform:rotate(360deg);}
  }
</style>