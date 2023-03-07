<template>
  <div class="custom-home">
    <main role="main" class="inner cover">
      <h3>Leader Board</h3>
      <v-date-picker
        v-model="selectedDate"
        @dayclick="onDateChange"
        :max-date='new Date()'
      />
      <ul>
        <li v-for="option in options" :key="option.id">
          <button type="button" @click="onPuzzleSelection(option.id)">{{ option.title }}</button>
        </li>
      </ul>
      <ul>
        <li v-for="person in data" :key="person.name">{{ person.name }} - {{ person[currOption].timeElapsed }}</li>
      </ul>
    </main>
  </div>
</template>

<script>
  export default {
    name: 'LeaderBoard',
    data() {
      return {
        selectedDate: new Date(),
        leaderboard: [],
        data: [],
        currOption: 'mini_results',
        options: [
          { id: 'mini_results', title: 'Mini' },
          { id: 'daily_results', title: 'Daily' },
        ],
      }
    },
    created: function () {
      this.fetchData();
    },
    methods: {
      // TODO: do one fetch and keeo everything in state
      // do one sort in beginning so its one time operation
      fetchData: async function(date) {
        let selectedDate = date;

        // TODO: probably a much better way to do this
        if (!selectedDate) {
          const nDate = new Date();

          const year = nDate.toLocaleString("default", { year: "numeric" });
          const month = nDate.toLocaleString("default", { month: "2-digit" });
          const day = nDate.toLocaleString("default", { day: "2-digit" });

          selectedDate = year + "-" + month + "-" + day;
        }
        const path = `http://localhost:5000/leaderboard?date=${selectedDate}`;
        const data = await fetch(path);

        const { leaderboard } = await data.json();

        console.log('response data', leaderboard);

        return this.data = leaderboard;
      },
      onDateChange: function({ id }) {
        return this.fetchData(id);
      },
      onPuzzleSelection: function (selectedOption) {
        this.currOption = selectedOption;
        // create separate func that compares and also takes "0" or "not started" into consideration
        console.log(this.data.sort((a, b) => a[selectedOption].timeElapsed - b[selectedOption].timeElapsed));
        // this.leaderboard = this.data.sort((a,b) => a[`${selectedOption}`].timeElasped - b[`${selectedOption}`].timeElasped);
        // console.log(this.leaderboard);
      }
    }
  };
</script>
<style>

</style>