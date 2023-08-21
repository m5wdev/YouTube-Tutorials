<template>
    <!-- <button id="eq" @click.prevent="$emit('claculateEvent')">=</button> -->
    <button id="eq" @click.prevent="$emit('claculateEvent', 'some data to send')">=</button>
</template>

<script>
export default {
}
</script>

<style scoped>
#eq {
    background-color: #cce7fc !important;
}
</style>
