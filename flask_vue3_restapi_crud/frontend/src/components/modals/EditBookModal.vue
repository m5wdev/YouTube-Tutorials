<script setup>
import { ref, onMounted } from 'vue'

import axios from 'axios'
import { Modal } from 'bootstrap'


const emit = defineEmits(['bookUpdated'])

const props = defineProps({
    book: Object,
})

const editBookModal = ref(null)
let modalEl = null

onMounted(() => {
    modalEl = new Modal(editBookModal.value)
})


const editBook = () => {
    console.log('editBook')
    axios
        .put(`/books/edit/${props.book.id}`, props.book)
        .then(response => {
            console.log(response)
            emit('bookUpdated', response.data)

            if (modalEl._isShown) {
                modalEl.hide()
            }
        })
        .catch(error => console.error(error))
}
</script>


<template>
    <div class="modal fade" id="editBookModal" tabindex="-1" aria-labelledby="editBookModalLabel" aria-hidden="true" ref="editBookModal">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <div class="h1 modal-title fs-5" id="editBookModalLabel">Edit book</div>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                {{ props.book }}<br>
                <div class="mb-3">
                    <label for="edit-title" class="form-label">Title</label>
                    <input v-model="props.book.title" type="text" class="form-control" id="edit-title" placeholder="Title">
                </div>
                <div class="mb-3">
                    <label for="edit-author" class="form-label">Author</label>
                    <input v-model="props.book.author" type="text" class="form-control" id="edit-author" placeholder="Author">
                </div>
                <div class="form-check">
                    <input v-model="props.book.read" class="form-check-input" type="checkbox" value="" id="edit-read">
                    <label class="form-check-label" for="edit-read">Read</label>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" @click="editBook">Edit Book</button>
            </div>
            </div>
        </div>
    </div>
</template>
