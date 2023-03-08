<template>
  <section>
    <h2>Head-To-Head Leaderboard</h2>
    <DatePicker
      v-model="selectedDate"
      :max-date='new Date()'
      @dayclick="onCalendarSelection($event)"
      :popover="{ visibility: 'click' }"
      id="date-selector-container"
      color="purple"
      :select-attribute="{ dot: true }"
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
        <button
          type="button"
          class="leaderboard-btn"
          v-bind:class="{ 'active': selectedLeaderboard === option.id }"
          @click="onPuzzleSelection(option.id)"
        >
          {{ option.title }}
        </button>
      </li>
    </ul>
    <ul id="leaderboard-rankings">
      <template v-if="isLoading">
        <div class="loading-container">
          <FontAwesomeIcon class="loading-spinner" icon="fa-solid fa-spinner" />
          <p>Crunching the numbers...</p>
        </div>
      </template>
      <template v-else>
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
              startedAt: person[selectedLeaderboard].startedAt ? new Date(person[selectedLeaderboard].startedAt * 1000).toLocaleString() : 'Not Started',
              finishedAt: person[selectedLeaderboard].solvedAt ? new Date(person[selectedLeaderboard].solvedAt * 1000).toLocaleString() : 'Not Completed',
              usedAutocomplete: person[selectedLeaderboard].usedAutoComplete,
            }"
          />
        </li>
      </template>
    </ul>
  </section>
</template>

<script>
  import { DatePicker } from 'v-calendar';

  import RankingWidget from '@/components/RankingWidget.vue'
  import { LEADERBOARD_OPTIONS } from '@/utils/constants';

  function formatInitDate(date) {
    const year = date.toLocaleString('default', { year: 'numeric' });
    const month = date.toLocaleString('default', { month: '2-digit' });
    const day = date.toLocaleString('default', { day: '2-digit' });

    return `${year}-${month}-${day}`;
  }

  // TODOS:
  // Overall app styling with heights, etc.
  export default {
    name: 'Leaderboard',
    data() {
      return {
        selectedDate: new Date(),
        leaderboardOptions: LEADERBOARD_OPTIONS,
        selectedLeaderboard: LEADERBOARD_OPTIONS[0].id,
        leaderboardData: [],
        isLoading: false,
      };
    },
    created: function () {
      this.fetchData(formatInitDate(this.selectedDate));
    },
    methods: {
      fetchData: async function (date) {
        this.isLoading = true;
        const data = await fetch(`http://localhost:5000/leaderboard-single?date=${date}`);
        const { leaderboard } = await data.json();
        console.log("response data", leaderboard);
        this.isLoading = false;
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
      onPuzzleSelection(selectedOption) {
        this.selectedLeaderboard = selectedOption;
        this.leaderboardData = this.sortLeaderboard(this.leaderboardData);
      },
      onCalendarSelection(selection) {
        // DatePicker component still fires selection events on disabled (future) days
        if (selection?.isDisabled) {
          return;
        }

        return this.fetchData(selection.id);
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
    height: 100%;

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
        margin: 0 24px; // TODO: revisit this
        text-transform: uppercase;
        font-family: 'Montserrat-Bold';
        padding: 12px 24px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        transition: ease-in-out 0.3s;
        background-color: transparent;
        color: $PRIMARY_900;
        border: 1px solid $PRIMARY_900;
        
        &:hover {
          cursor: pointer;
          background-color: $PRIMARY_300;
          border: 1px solid $PRIMARY_300;
        }

        &.active {
          background-color: $PRIMARY_500;
          color: $WHITE;
          border: 1px solid transparent;

          &:hover {
            cursor: initial;
          }
        }
      }
    }

    #leaderboard-rankings {
      width: 50%;
      height: 100%;

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
  }

  @keyframes spin {
    from {transform:rotate(0deg);}
    to {transform:rotate(360deg);}
  }
</style>