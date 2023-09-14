<script setup>
import { ref, reactive, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import axios from 'axios'

import AddBookModal from '@/components/modals/AddBookModal.vue'
import EditBookModal from '@/components/modals/EditBookModal.vue'
import Alert from '@/components/Alert.vue'


const books = ref([])
const editBook = ref({})

const alert = reactive({
    show: false,
    type: '',
    message: ''
})


const showAlert = (type, message) => {
    alert.show = true
    alert.type = type
    alert.message = message
}

const resetAlert = () => {
    alert.show = false
    alert.type = ''
    alert.message = ''
}


const getBooks = () => {
    books.value = []

    axios
        .get('/books')
        .then(response => {
            console.log('response', response)
            books.value = response.data.books
        })
        .catch(error => console.error(error))
}

const addBookHandler = data => {
    resetAlert()

    console.log('newBookAdded', data)
    books.value.unshift(data.book)

    showAlert('success', `${data.book.title} has been added`)

    setTimeout(() => {
        resetAlert()
    }, 1000)
}


const removeBook = index => {
    resetAlert()

    console.log('removeBook', index)
    books.value.splice(index, 1)

    axios
        .delete(`/books/remove/${index}`)
        .then(response => {
            console.log('response', response)

            showAlert('danger', `${response.data.book.title} has been deleted`)

            setTimeout(() => {
                resetAlert()
            }, 1000)
        })
        .catch(error => console.error(error))
}


const editBookHandler = book => {
    console.log('editBook', book)
    editBook.value = book
}

const bookUpdatedHandler = data => {
    console.log('bookUpdatedHandler', data)

    showAlert('info', `${data.book.title} has been updated`)

    setTimeout(() => {
        resetAlert()
    }, 1000)
}


onMounted(() => {
    getBooks()
})
</script>


<template>
    <div class="container py-4">
        <h1>Books</h1>

        {{ alert }}<br>
        <Alert
            :show="alert.show"
            :type="alert.type"
            :message="alert.message" />
        <br>
        <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addBookModal">
            Add book
        </button>
        <br><br>
        <hr>
        <br>
        <table class="table table-hover">
            <thead>
                <th scope="col">Title</th>
                <th scope="col">Author</th>
                <th scope="col">Read</th>
                <th></th>
            </thead>
            <tbody>
                <tr v-for="(book, index) in books" :key="index">
                    <td>
                        <RouterLink class="" exact-active-class="" active-class="" :to="{name: 'book', params: {id: book.id}}">{{ book.title }}</RouterLink>
                    </td>
                    <td>{{ book.author }}</td>
                    <td>
                        <span v-if="book.read" class="p-2 d-block text-center bg-success-subtle">Yes</span>
                        <span v-else class="p-2 d-block text-center bg-danger-subtle">No</span>
                    </td>
                    <td class="text-end">
                        <div class="btn-group">
                            <button class="btn btn-warning" @click="editBookHandler(book)" data-bs-toggle="modal" data-bs-target="#editBookModal">Edit</button>
                            <button class="btn btn-danger" @click="removeBook(index)">Delete</button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <AddBookModal @newBookAdded="addBookHandler" />
        <EditBookModal @bookUpdated="bookUpdatedHandler" :book="editBook" />
    </div>
</template>
