const getAllUsersBtn = document.querySelector('#get-all-users')

getAllUsersBtn.addEventListener('click', () => {
    fetch('http://127.0.0.1:8000/user/get-all')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error))
})


// Login
const usernameInput = document.querySelector('#username')
const passwordInput = document.querySelector('#password')
const loginBtn = document.querySelector('#login')
const loginWrp = document.querySelector('#login-wrp')
const userSection = document.querySelector('#user-section')
const welcome = document.querySelector('#welcome')
const logoutBtn = document.querySelector('#logout')

const currentUser = () => {
    if (localStorage.getItem('username')) {
        loginWrp.style.display = 'none'
        userSection.style.display = 'block'
        welcome.innerHTML = `Hi, <strong>${localStorage.getItem('username')}</strong>!`
    }
}

currentUser()

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')

    loginWrp.style.display = 'block'
    userSection.style.display = 'none'
    welcome.innerHTML = ''
})


loginBtn.addEventListener('click', () => {
    let formData = new FormData()
    formData.append('username', usernameInput.value)
    formData.append('password', passwordInput.value)

    fetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)

            localStorage.setItem('token', data.access_token)
            localStorage.setItem('username', data.username)

            currentUser()
        })
        .catch(error => console.error(error))
})


const blogPostInput = document.querySelector('#blog-post-id')
const blogPostBtn = document.querySelector('#get-blog-post')

let token = localStorage.getItem('token')

blogPostBtn.addEventListener('click', () => {
    fetch(`http://127.0.0.1:8000/blog/${blogPostInput.value}`, {
        headers: {
            // Authorization: `Bearer ${token}`
            Authorization: `Bearer ${localStorage.getItem('token') }`
        },
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error))
})
