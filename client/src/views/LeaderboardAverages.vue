<template>
  <section>
    <h2>Leader Board Averages - Mini Only</h2>
    <p class="subtitle">(Data pulled from the last 31 days)</p>
    <ul class="averages-results">
      <Overlays :error="{ status: error, message: errorMsg }" :loading="{ status: loading, message: 'Crunching the numbers...' }" />
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
  </section>
</template>

<script>
  import fetcher from '../utils/fetcher';
  import Overlays from '@/components/Overlays.vue';

  export default {
    name: 'Leaderboard',
    data() {
      return {
        data: [],
        loading: false,
        error: false,
        errorMsg: '',
      };
    },
    created: function () {
      this.fetchData();
    },
    methods: {
      fetchData: async function () {
        // clear existing error if present
        if (this.errorMsg) {
          this.errorMsg = '';
        }
        this.loading = true;
        const { data, message, status } = await fetcher('/leaderboard-averages');
        this.loading = false;

        // TODO: constants
        if (status !== 'success') {
          this.error = true;
          this.errorMsg = message;
          return this.data = [];
        }

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
    components: { Overlays },
 };
</script>

<style scoped lang="scss">
  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;

    h2 {
      font-size: 24px;
      text-align: center;
    }

    .subtitle {
      margin-top: 16px;
    }

    ul {
      list-style-type: none;
    }

    .averages-results {
      display: flex;
      flex-direction: column;
      margin-top: 16px;
      flex: 1;

      .result-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        border: 1px solid $PRIMARY_100;
        box-shadow: 0px 4px 10px -4px rgba(0, 30, 43, 0.3);
        border-radius: 24px;
        padding: 32px;
        margin-top: 16px;

        .name {
          font-size: 16px;
        }

        .average {
          font-size: 32px;
          font-family: 'Montserrat-Bold';
          color: $PRIMARY_600;
          margin: 8px 0;
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

    @media (min-width: $BREAKPOINT_MD) {
      h2 {
        font-size: 32px;
      }

      .averages-results {
        flex-direction: row;
        margin-top: 24px;

        .result-container {
          margin: 0 16px;

          .name {
            font-size: 20px;
          }

          .average {
            font-size: 48px;
            margin: 16px 0;
          }
        }
      }
    }
  }
</style>