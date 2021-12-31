<template>
  <div class="container has-text-centered">
    <div class="columns is-flex is-flex-wrap-wrap is-vcentered is-fullheight">
      <div class="column is-12">
        <span class="title" v-if="intervalMinutes > 0 || intervalSeconds > 0">
          Bewegen in {{intervalMinutes}}:{{addPaddingToSeconds(intervalSeconds)}}
        </span>

        <span class="title" v-else>
          Bewegen für {{durationMinutes}}:{{addPaddingToSeconds(durationSeconds)}} Minuten
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

    <div class="message is-floating" v-if="isMessageVisible" :class="hasMoved ? 'is-success' : 'is-danger'">
      <div class="message-header">
        <p v-if="hasMoved">Bewegung erkannt</p>
        <p v-else>Keine Bewegung erkannt</p>
        <button class="delete" aria-label="delete" @click="isMessageVisible = false"></button>
      </div>
      <div class="message-body">
        <span v-if="hasMoved">Sie haben sich bewegt, stelle den Timer erneut</span>
        <span v-else>Sie haben sich leider nicht bewegt :(</span>
        <figure class="image is-128x128" v-if="!hasMoved">
          <img src="https://laughingsquid.com/wp-content/uploads/2016/06/gxrb_bn-iwbd1o7gyrsxyojbeilmz45j7zmzcaxf77y.jpg">
        </figure>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "@vue/reactivity";
import { Ref } from "vue";
import axios from "axios";

interface TimerData {
  interval: number;
  duration: number;
  timestamp: number;
}

const apiUrl = process.env.API_URL || "https://lab08api-bc5wazhcdq-oa.a.run.app";
const durationMinutes = ref(5);
const durationSeconds = ref(0);
const intervalMinutes = ref(60)
const intervalSeconds = ref(0);
const isMessageVisible = ref(false);
const hasMoved = ref(false);
let intervalResetValue = 0;
let durationResetValue = 0;
let timestamp = 0;

const minutesToMilliseconds = (min: number) => min * 60 * 1000;
const addPaddingToSeconds = (sec: number) => (sec).toString().padStart(2, "0");

function startTimer(): void {
  intervalResetValue = intervalMinutes.value;
  durationResetValue = durationMinutes.value;
  timestamp = Date.now()
  setInterval(startInterval, 1000);
}

function startInterval(): void {
  if (intervalMinutes.value === 0 && intervalSeconds.value === 0) {
    if (durationMinutes.value === 0 && durationSeconds.value === 0) {
      const data: TimerData = {
        interval: minutesToMilliseconds(intervalResetValue),
        duration: minutesToMilliseconds(durationResetValue),
        timestamp: timestamp,
      }

      axios.post(`${apiUrl}/move`, data).then((res) => {
        hasMoved.value = res.data;
        isMessageVisible.value = true;
        intervalMinutes.value = intervalResetValue;
        durationMinutes.value = durationResetValue;
        timestamp = Date.now()
      })
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
    _seconds.value = 59
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

.is-floating {
  position: absolute;
  top: 2rem;
  right: 0;
}
</style>