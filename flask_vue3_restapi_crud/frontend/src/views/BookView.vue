<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import axios from 'axios'


const route = useRoute()
const book = ref({})

const getBook = id => {
    console.log('getBook', id)

    axios
        .get(`/books/${id}`)
        .then(response => {
            console.log('response', response)
            book.value = response.data
        })
        .catch(error => console.error(error))
}

onMounted(() => {
    getBook(route.params.id)
})
</script>

<template>
    <div class="container">
        <h1>Book: {{ book.title }}</h1>
        <div>Author: {{ book.author }}</div>
    </div>
</template>
