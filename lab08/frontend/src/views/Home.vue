<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
    <span>{{counter}}</span>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

const counter = ref(0);

const increment = computed(() => counter.value + 1)
</script>
