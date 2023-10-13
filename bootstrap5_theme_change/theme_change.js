const themeSwitcher = document.querySelector('#theme-switcher')
const links = themeSwitcher.querySelectorAll('a')

const currentTheme = localStorage.getItem('theme') ?
                        localStorage.getItem('theme') :
                        document.documentElement.getAttribute('data-bs-theme')

const setTheme = theme => {
    if (theme === 'auto' || theme === null || theme === '') {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        localStorage.setItem('theme', 'auto')
    } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
        localStorage.setItem('theme', theme)
    }
}

setTheme(currentTheme)

links.forEach(link => {
    if (localStorage.getItem('theme') === link.getAttribute('data-theme')) {
        link.classList.add('active')
    } else {
        link.classList.remove('active')
    }

    link.addEventListener('click', e => {
        e.preventDefault()

        links.forEach(l => {
            l.classList.remove('active')
        })

        const theme = link.getAttribute('data-theme')
        link.classList.add('active')
        // console.log(theme)
        setTheme(theme)
    })
})
