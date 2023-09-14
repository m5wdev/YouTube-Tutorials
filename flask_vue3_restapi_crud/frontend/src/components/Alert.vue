<script setup>
import { ref, watch } from 'vue'


const props = defineProps({
    show: Boolean,
    type: String,
    message: String,
})

const alertPlaceholder = ref(null)

const appendAlert = (message, type) => {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')

    alertPlaceholder.value.append(wrapper)

    setTimeout(() => {
        // alertPlaceholder.value.innerHTML = ''
        wrapper.innerHTML = ''
    }, 7000)
}


watch(() => props.show, (newValue, oldValue) => {
    console.log('newValue', newValue)
    console.log('oldValue', oldValue)

    if (newValue) {
        // alertPlaceholder.value.innerHTML = ''
        appendAlert(props.message, props.type)
    }
})
</script>


<template>
    <div id="alert-placeholder" ref="alertPlaceholder"></div>
</template>
