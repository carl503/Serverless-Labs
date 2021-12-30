<template>
  <div class="container has-text-centered">
    <div class="columns is-flex is-flex-wrap-wrap is-vcentered is-fullheight">
      <div class="column is-12">
        <span class="title">{{interval}}:{{(seconds).toString().padStart(2, 0)}}
        </span>
      </div>
      <div class="column is-12">
        <div class="level">
          <div class="level-item">
            <label for="interval">
              <span class="mr-2">Alle {{interval}} Minuten bewegen</span>
              <input class="input" type="number" name="interval" v-model="interval">
            </label>
          </div>

          <div class="level-item">
            <label for="duration">
              <span class="mr-2">Wie viele Minuten wollen Sie sich bewegen?</span>
              <input class="input" type="number" name="duration" v-model="duration">
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
interface TimerData {
  interval: number;
  duration: number;
  timestamp: number;
}

import { ref } from "@vue/reactivity";
const duration = ref(5)
const interval = ref(60)
let minutes = 0;
let seconds = ref(0);
let internalInterval: null | number = null;

function startTimer(): void {
  minutes = interval.value;
  const timerData: TimerData = {
    interval: minutes,
    duration: duration.value,
    timestamp: Date.now()
  }
  
  internalInterval = setInterval(startInterval, 1000);
  
}

function startInterval(): void {
  if (seconds.value > 0 && interval.value >= 0) {
    seconds.value--
  } else if (interval.value > 0) {
    seconds.value = 59
    interval.value--
  } else if (internalInterval) {
    clearInterval(internalInterval)
    // call api
  }
  console.log(`Minutes: ${interval.value} Seconds: ${seconds.value}`);
  
}

</script>

<style>
@import "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css";

.is-fullheight {
  height: 100vh;
}
</style>