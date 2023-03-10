<template>
  <section>
    <h2>Head-To-Head Leaderboard</h2>
    <DatePicker
      color="purple"
      v-model="selectedDate"
      :max-date="new Date()"
      :select-attribute="{ dot: true }"
      :popover="{ visibility: 'click' }"
      @dayclick="onCalendarSelection($event)"
      id="date-selector-container"
    >
      <template v-slot="{ inputValue, inputEvents }">
        <label for="date-input">
          Show Results For:
          <div class="input-container">
            <input id="date-input" :value="inputValue" v-on="inputEvents" />
            <FontAwesomeIcon icon="fa-solid fa-calendar-days" />
          </div>
        </label>
      </template>
    </DatePicker>
    <ul id="leaderboard-options">
      <li v-for="option in leaderboardOptions" :key="option.id">
        <button
          type="button"
          class="leaderboard-btn"
          v-bind:class="{ active: selectedLeaderboard === option.id }"
          @click="onPuzzleSelection(option.id)"
        >
          {{ option.title }}
        </button>
      </li>
    </ul>
    <ul id="leaderboard-rankings">
      <Overlays
        :error="{ status: error, message: errorMsg }"
        :loading="{ status: loading, message: 'Getting the data...' }"
      />
      <RankingWidget
        v-for="(person, index) in leaderboardData"
        :key="person.name"
        :name="person.name"
        :place="index + 1"
        :time="
          new Date(person[selectedLeaderboard].timeElapsed * 1000)
            .toISOString()
            .substring(14, 19)
        "
        :timeDesc="
          getTimeDesc(
            person[selectedLeaderboard].completed,
            person[selectedLeaderboard].startedAt
          )
        "
        :metadata="{
          startedAt: person[selectedLeaderboard].startedAt
            ? new Date(
                person[selectedLeaderboard].startedAt * 1000
              ).toLocaleString()
            : 'Not Started',
          finishedAt: person[selectedLeaderboard].solvedAt
            ? new Date(
                person[selectedLeaderboard].solvedAt * 1000
              ).toLocaleString()
            : 'Not Completed',
          usedAutoComplete: person[selectedLeaderboard].usedAutoComplete,
        }"
      />
    </ul>
  </section>
</template>

<script>
import { DatePicker } from "v-calendar";

import RankingWidget from "@/components/RankingWidget.vue";
import Overlays from "@/components/Overlays.vue";
import { LEADERBOARD_OPTIONS } from "@/utils/constants";
import fetcher from "@/utils/fetcher";

function formatInitDate(date) {
  const year = date.toLocaleString("default", { year: "numeric" });
  const month = date.toLocaleString("default", { month: "2-digit" });
  const day = date.toLocaleString("default", { day: "2-digit" });

  return `${year}-${month}-${day}`;
}

export default {
  name: "Leaderboard",
  data() {
    return {
      selectedDate: new Date(),
      leaderboardOptions: LEADERBOARD_OPTIONS,
      selectedLeaderboard: LEADERBOARD_OPTIONS[0].id,
      leaderboardData: [],
      loading: false,
      error: false,
      errorMsg: "",
    };
  },
  created: function () {
    this.fetchData(formatInitDate(this.selectedDate));
  },
  methods: {
    fetchData: async function (date) {
      // clear existing error if present
      if (this.errorMsg) {
        this.errorMsg = "";
      }
      // TODO: better way to do this?
      this.leaderboardData = [];
      this.loading = true;
      const { data, message, status } = await fetcher(
        `/api/leaderboard-single?date=${date}`
      );
      this.loading = false;

      // TODO: constants
      if (status !== "success") {
        this.error = true;
        this.errorMsg = message;
        return (this.leaderboardData = []);
      }

      return (this.leaderboardData = this.sortLeaderboard(data));
    },
    sortLeaderboard: function (data) {
      const lbData = data;
      console.log("data", lbData);
      return lbData.sort((a, b) => {
        if (a[`${this.selectedLeaderboard}`].timeElapsed === 0) return 1;
        if (b[`${this.selectedLeaderboard}`].timeElapsed === 0) return -1;
        return (
          a[`${this.selectedLeaderboard}`].timeElapsed -
          b[`${this.selectedLeaderboard}`].timeElapsed
        );
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
        return "";
      } else if (!completion && startTime) {
        return "Not Completed";
      }

      return "Not Started";
    },
  },
  components: { DatePicker, RankingWidget, Overlays },
};
</script>

<style scoped lang="scss">
section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  flex: 1;

  h2 {
    font-size: 24px;
    text-align: center;
  }

  ul {
    list-style-type: none;
  }

  #date-selector-container {
    margin-top: 24px;

    label {
      display: flex;
      flex-direction: column;
      font-size: 14px;

      .input-container {
        position: relative;

        #date-input {
          outline: 0;
          margin-top: 8px;
          border-radius: 8px;
          border: 1px solid $GRAYSCALE_400;
          line-height: 16px;
          font-size: 14px;
          padding: 6px 10px;
          font-family: "Montserrat-Bold";
        }

        svg {
          position: absolute;
          top: 16px;
          right: 12px;
        }
      }
    }
  }

  #leaderboard-options {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 24px;

    .leaderboard-btn {
      outline: none;
      text-transform: uppercase;
      font-family: "Montserrat-Bold";
      padding: 8px 16px;
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
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;
    flex: 1;
  }

  @media (min-width: $BREAKPOINT_SM) {
    #leaderboard-options {
      justify-content: space-evenly;
    }
  }

  @media (min-width: $BREAKPOINT_MD) {
    h2 {
      font-size: 32px;
    }

    #date-selector-container {
      label {
        flex-direction: row;
        align-items: center;
        font-size: 16px;

        .input-container {
          #date-input {
            font-size: 16px;
            padding: 8px 12px;
            margin-top: 0;
            margin-left: 12px;
          }

          svg {
            top: 10px;
          }
        }
      }
    }

    #leaderboard-options {
      .leaderboard-btn {
        padding: 12px 24px;
      }
    }
  }

  @media (min-width: $BREAKPOINT_LG) {
    #leaderboard-options,
    #leaderboard-rankings > li {
      max-width: 75%;
    }
  }

  @media (min-width: $BREAKPOINT_XL) {
    #leaderboard-options,
    #leaderboard-rankings > li {
      max-width: 50%;
    }
  }
}
</style>
