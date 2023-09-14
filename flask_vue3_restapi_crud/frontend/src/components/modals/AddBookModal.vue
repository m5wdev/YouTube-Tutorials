<script setup>
import { ref, onMounted } from 'vue'

import axios from 'axios'
import { Modal } from 'bootstrap'


const emit = defineEmits(['newBookAdded'])

const addBookModal = ref(null)
let modalEl = null

onMounted(() => {
    modalEl = new Modal(addBookModal.value)
})

const book = ref({
    title: '',
    author: '',
    read: false,
})

const addBook = () => {
    axios
        .post('/books/add', book.value)
        .then(response => {
            console.log(response)
            emit('newBookAdded', response.data)

            if (modalEl._isShown) {
                modalEl.hide()
            }

            book.value.title = ''
            book.value.author = ''
            book.value.read = false
        })
        .catch(error => console.error(error))
}
</script>


<template>
    <div class="modal fade" id="addBookModal" tabindex="-1" aria-labelledby="addBookModalLabel" aria-hidden="true" ref="addBookModal">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <div class="h1 modal-title fs-5" id="addBookModalLabel">Add book</div>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                {{ book }}
                <div class="mb-3">
                    <label for="add-title" class="form-label">Title</label>
                    <input v-model="book.title" type="text" class="form-control" id="add-title" placeholder="Title">
                </div>
                <div class="mb-3">
                    <label for="add-author" class="form-label">Author</label>
                    <input v-model="book.author" type="text" class="form-control" id="add-author" placeholder="Author">
                </div>
                <div class="form-check">
                    <input v-model="book.read" class="form-check-input" type="checkbox" id="add-read">
                    <label class="form-check-label" for="add-read">Read</label>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" @click="addBook">Add New Book</button>
            </div>
            </div>
        </div>
    </div>
</template>
