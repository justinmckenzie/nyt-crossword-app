<template>
  <li class="ranking">
    <div class="ranking__data">
      <div class="ranking__data_place">{{ place }}</div>
      <span class="ranking__data_name">{{ name }}</span>
      <div class="ranking__data_time">
        <span>{{ time }}</span>
        <span v-show="timeDesc" class="ranking__data_time_desc">
          {{ timeDesc }}
        </span>
      </div>
    </div>
    <button id="show-metadata-btn" type="button" @click="toggleMetadata">
      {{ showMetadata ? "Hide" : "Show" }} Puzzle Metadata
      <FontAwesomeIcon
        class="chevron-icon"
        icon="fa-solid fa-chevron-right"
        v-bind:class="{ rotate: showMetadata }"
      />
    </button>
    <transition
      name="metadata"
      v-on:enter="enter"
      v-on:leave="leave"
      v-on:before-enter="beforeEnter"
      v-on:before-leave="beforeLeave"
    >
      <div v-show="showMetadata" class="ranking__metadata">
        <p>Started Puzzle: {{ metadata.startedAt }}</p>
        <p>Finished Puzzle: {{ metadata.finishedAt }}</p>
        <p>Autocomplete Used? {{ metadata.usedAutoComplete ? "Yes" : "No" }}</p>
      </div>
    </transition>
  </li>
</template>

<script>
export default {
  name: "RankingWidget",
  props: ["name", "place", "time", "metadata", "timeDesc"],
  data() {
    return {
      showMetadata: false,
    };
  },
  methods: {
    toggleMetadata: function () {
      return (this.showMetadata = !this.showMetadata);
    },
    beforeEnter: function (el) {
      el.style.height = "0";
    },
    enter: function (el) {
      el.style.height = el.scrollHeight + "px";
    },
    beforeLeave: function (el) {
      el.style.height = el.scrollHeight + "px";
    },
    leave: function (el) {
      el.style.height = "0";
    },
  },
};
</script>

<style scoped lang="scss">
// TODO: more css touch up on these (later on)
.ranking {
  margin-top: 24px;
  position: relative;
  padding: 32px 24px 16px;
  border-radius: 24px;
  overflow: hidden;
  width: 100%;
  @include card-border;

  &__data {
    display: flex;
    align-items: center;
    justify-content: space-between;

    &_place {
      font-size: 16px;
      color: $WHITE;
      background-color: $PRIMARY_500;
      position: absolute;
      top: 0;
      left: 0;
      height: 24px;
      width: 50px;
      @include flex-center;
      border-radius: 0 0 8px 0px;
      font-family: "Montserrat-Bold";
    }

    &_time {
      text-align: right;

      span {
        display: block;
      }

      &_desc {
        font-size: 12px;
        font-style: italic;
        color: $GRAYSCALE_600;
      }
    }
  }

  #show-metadata-btn {
    outline: 0;
    border: none;
    background-color: transparent;
    font-size: 12px;
    color: $GRAYSCALE_600;
    text-transform: uppercase;
    margin-top: 16px;

    &:hover {
      cursor: pointer;
      text-decoration: underline;
    }

    .chevron-icon {
      margin-left: 6px;
      transform: rotate(0deg);
      transition-duration: 0.3s;

      &.rotate {
        transform: rotate(90deg);
        transition-duration: 0.3s;
      }
    }
  }

  &__metadata {
    transition: 200ms ease-out;
    margin-top: 12px;

    p {
      font-size: 12px;
      margin: 6px 0;
      color: $GRAYSCALE_600;
    }
  }
}
</style>
