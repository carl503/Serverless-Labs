<template>
  <div class="container has-text-centered">
    <div class="columns is-flex is-flex-wrap-wrap is-vcentered is-fullheight">
      <div class="column is-12">
        <span class="title" v-if="intervalMinutes > 0 || intervalSeconds > 0">
          Bewegen in {{intervalMinutes}}:{{(intervalSeconds).toString().padStart(2, 0)}}
        </span>

        <span class="title" v-else>
          Bewegen für {{durationMinutes}}:{{(durationSeconds).toString().padStart(2, 0)}} Minuten
        </span>
      </div>
      <div class="column is-12">
        <div class="level">
          <div class="level-item">
            <label for="interval">
              <span class="mr-2">Alle {{intervalMinutes}} Minuten bewegen</span>
              <input class="input" type="number" name="interval" v-model="intervalMinutes">
            </label>
          </div>

          <div class="level-item">
            <label for="duration">
              <span class="mr-2">Wie viele Minuten wollen Sie sich bewegen?</span>
              <input class="input" type="number" name="duration" v-model="durationMinutes">
            </label>
          </div>
        </div>
      </div>

      <div class="column is-12 is-flex is-justify-content-center">
        <div class="buttons">
          <button class="button is-success" @click="startTimer">Timer starten</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "@vue/reactivity";
import { Ref } from "vue";
const durationMinutes = ref(5);
const durationSeconds = ref(0);
const intervalMinutes = ref(60)
const intervalSeconds = ref(0);
let intervalResetValue = 0;
let durationResetValue = 0;

function startTimer(): void {
  intervalResetValue = intervalMinutes.value;
  durationResetValue = durationMinutes.value;
  
  setInterval(startInterval, 1000);
  
}

function startInterval(): void {
  if (intervalMinutes.value === 0 && intervalSeconds.value === 0) {
    if (durationMinutes.value === 0 && durationSeconds.value === 0) {
      intervalMinutes.value = intervalResetValue;
      durationMinutes.value = durationResetValue;
    } else {
      updateTimer(durationMinutes, durationSeconds);
    }
  } else {
    updateTimer(intervalMinutes, intervalSeconds);
  }
}

function updateTimer(_minutes: Ref<number>, _seconds: Ref<number>) {
  if (_seconds.value > 0 && _minutes.value >= 0) {
    _seconds.value--
  } else if (_minutes.value > 0) {
    _seconds.value = 5
    _minutes.value--
  }
  console.log(`Minutes: ${_minutes.value} Seconds: ${_seconds.value}`);
}

</script>

<style>
@import "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css";

.is-fullheight {
  height: 100vh;
}
</style>