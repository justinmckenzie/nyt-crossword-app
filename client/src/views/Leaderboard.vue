<template>
  <section>
    <h2>Leader Board</h2>
    <DatePicker
      v-model="selectedDate"
      :max-date='new Date()'
      @dayclick="fetchData($event.id)"
      :popover="{ visibility: 'click' }"
      id="date-selector-container"
    >
      <template v-slot="{ inputValue, inputEvents }">
        <label for="date-input">
          Show Results For:
          <input
            id="date-input"
            :value="inputValue"
            v-on="inputEvents"
          />
          <FontAwesomeIcon icon="fa-solid fa-calendar-days" />
        </label>
      </template>
    </DatePicker>
    <ul id="leaderboard-options">
      <li v-for="option in leaderboardOptions" :key="option.id">
        <button type="button" class="leaderboard-btn" @click="onPuzzleSelection(option.id)">{{ option.title }}</button>
      </li>
    </ul>
    <ul id="leaderboard-rankings">
      <li
        v-for="person, index in leaderboardData"
        :key="person.name"
        class="ranking-container"
      >
        <RankingWidget
          :name="person.name"
          :place="index + 1"
          :time="new Date(person[selectedLeaderboard].timeElapsed * 1000).toISOString().substring(14, 19)"
          :timeDesc="getTimeDesc(person[selectedLeaderboard].completed, person[selectedLeaderboard].startedAt)"
          :metadata="{
            // TODO: need to add in logic for showing only if it's been completed
            startedAt: person[selectedLeaderboard].startedAt ? new Date(person[selectedLeaderboard].startedAt * 1000).toLocaleString() : 'Not Started',
            finishedAt: person[selectedLeaderboard].solvedAt ? new Date(person[selectedLeaderboard].solvedAt * 1000).toLocaleString() : 'Not Completed',
            usedAutocomplete: person[selectedLeaderboard].usedAutoComplete,
          }"
        />
      </li>
    </ul>
  </section>
</template>

<script>
  import { DatePicker } from 'v-calendar';

  import RankingWidget from '@/components/RankingWidget.vue'
  import { LEADERBOARD_OPTIONS } from '@/utils/constants';

  function formatInitDate() {
    const date = new Date();

    const year = date.toLocaleString('default', { year: 'numeric' });
    const month = date.toLocaleString('default', { month: '2-digit' });
    const day = date.toLocaleString('default', { day: '2-digit' });

    return `${year}-${month}-${day}`;
  }

  // TODOS:
  // Calendar initial date is wrong
  // Prevent req or click event on a disabled date
  // Colors for Calendar (active selection, etc)
  // Loading placeholder
  // Active state for selected option
  export default {
    name: 'Leaderboard',
    data() {
      return {
        selectedDate: formatInitDate(),
        leaderboardOptions: LEADERBOARD_OPTIONS,
        selectedLeaderboard: LEADERBOARD_OPTIONS[0].id,
        leaderboardData: [],
      };
    },
    created: function () {
      this.fetchData(this.selectedDate);
    },
    methods: {
      fetchData: async function (date) {
        const data = await fetch(`http://localhost:5000/leaderboard?date=${date}`);
        const { leaderboard } = await data.json();
        console.log("response data", leaderboard);
        return this.leaderboardData = this.sortLeaderboard(leaderboard);
      },
      sortLeaderboard: function (data) {
        const lbData = data;
        return lbData.sort((a, b) => {
          if (a[`${this.selectedLeaderboard}`].timeElapsed === 0) return 1;
          if (b[`${this.selectedLeaderboard}`].timeElapsed === 0) return -1;
          return a[`${this.selectedLeaderboard}`].timeElapsed - b[`${this.selectedLeaderboard}`].timeElapsed;
        });
      },
      onPuzzleSelection: function (selectedOption) {
        this.selectedLeaderboard = selectedOption;
        this.leaderboardData = this.sortLeaderboard(this.leaderboardData);
      },
      getTimeDesc(completion, startTime) {
        if (completion) {
          return '';
        } else if (!completion && startTime) {
          return 'Not Completed';
        }

        return 'Not Started';
      },
    },
    components: { DatePicker, RankingWidget },
};
</script>

<style scoped lang="scss">
  section {
    display: flex;
    flex-direction: column;
    align-items: center;

    h2 {
      font-size: 32px;
    }

    ul {
      list-style-type: none;
    }

    #date-selector-container {
      label {
        position: relative;
        display: flex;
        align-items: center;
        margin-top: 24px;

        #date-input {
          padding: 8px 12px;
          outline: 0;
          border-radius: 8px;
          border: 1px solid $GRAYSCALE_400;
          margin-left: 12px;
          line-height: 16px;
          font-size: 16px;
          font-family: 'Montserrat-Bold';
        }

        svg {
          margin-left: -28px;
        }
      }
    }

    #leaderboard-options {
      display: flex;
      width: 100%;
      justify-content: center;
      margin-top: 24px;

      .leaderboard-btn {
        outline: none;
        border: none;
        margin: 0 24px; // TODO: revisit this
        text-transform: uppercase;
        font-family: 'Montserrat-Bold';
        padding: 12px 24px;
        border-radius: 4px;
        color: $WHITE;
        letter-spacing: 0.5px;
        background-color: $PRIMARY_500;
        transition: ease-in-out 0.3s;

        &:hover {
          cursor: pointer;
          background-color: $PRIMARY_300;
          color: $PRIMARY_900;
        }
      }
    }

    #leaderboard-rankings {
      width: 50%;
    }
  }
</style>