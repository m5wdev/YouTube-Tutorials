export default {
    router: {
        middleware: ['route'],
        baseURL: "/"
    },

    loadingIndicator: {
        name: 'pulse',
        color: '#FAFAFA',
        background: '#1e2539'
    },
    loading: '~/components/LoadingBar.vue',
    head: {
        title: 'Servis-Centers.ru – реестр сервисных центров России',
        meta: [
            { charset: 'utf-8' },
            { name: "apple-mobile-web-app-status-bar-style", content: "default" },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            // { hid: 'description', name: 'description', content: '' },
            { name: 'format-detection', content: 'telephone=no' },
            { name: "mailru-domain", content: "Kc0kQgfqR5KoNo3t" },
            { property: 'og:type', content: 'website' },
            { property: 'og:locale', content: 'ru_RU' },
            // { property: 'og:site_name', content: 'Servis-Centers.ru – реестр сервисных центров России' },
            // { property: 'og:image', content: 'https://servis-centers.ru/logo-smm.jpg' },
        ],

        link: [
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
            { rel: "apple-touch-icon", type: "image/png", href: "/icon.png" }
        ],
    },
    pwa: {
        workbox: {
        },
        meta: {
            theme_color: "#ffffff"
        },
        manifest: {
            name: 'Агрегатор Сервисных Центров',
            short_name: 'Сервисные Центры',
            description: 'Агрегатор Сервисных центров России',
            lang: 'ru',
            display: 'standalone',
        },
    },

    css: [
        {
            src: 'assets/bootstrap.scss', lang: 'scss'
        },
        {
            src: 'assets/styles.scss', lang: 'scss'
        },
    ],

    loading: {
        color: 'limegreen',
        height: '2px'
    },

    plugins: [
        {
            src: '~/plugins/bootstrap.js',
            mode: 'client'
        },
        {
            src: '~/plugins/ymapPlugin.js',
            mode: 'client',
            ssr: false
        },
        {
            src: '~/plugins/click-outside.js',
            mode: 'client'
        },
        {
            src: '~/plugins/pagination.js',
            mode: 'client'
        },
        {
            src: '~/plugins/v-mask.js',
            mode: 'client'
        },
        {
            src: '~/plugins/autocomplete.js',
            mode: 'client'
        },
    ],

    components: true,

    modules: [
        '@nuxtjs/axios',
        '@nuxtjs/pwa',
        '@nuxtjs/auth-next',
        'cookie-universal-nuxt',
        'dropzone-nuxt',
        'nuxt-lazy-load',

        '@nuxtjs/robots',
        // '@nuxtjs/sitemap',
    ],

    buildModules: [
        ['@nuxtjs/router', { keepDefaultRouter: true }],
    ],

    robots: {
        UserAgent: '*',
        Disallow: [
            '/profile',
            '/login',
            '/register',
            '/resetpassword'
        ],
        Allow: '/'
    },
    // sitemap: {
    //     generate: true,
    //     // hostname: 'http://localhost:3000',
    //     exclude: [
    //         '/profile', '/profile/**',
    //         '/login', '/login/**',
    //         '/registration', '/registration/**',
    //         '/admin', '/admin/**',
    //         '/profile', '/profile/**',
    //     ],
    // },

    proxy: {
        "/api/v1/": {
            target: 'http://servis-centers.ru:8000//api/v1/',
            pathRewrite: { "^/api/v1/": "" },
            changeOrigin: true
        },
        // "/media/": {
        //     target: process.env.API_BASE_URL || 'http://localhost:8000',
        //     pathRewrite: { "^/": "" },
        //     changeOrigin: false
        // }
    },

    axios: {
        // baseURL: process.env.API_BASE_URL || "http://localhost:8000",
        proxy: true,
    },

    auth: {
        strategies: {
            local: {
                scheme: 'refresh',
                token: {
                    property: 'access',
                    maxAge: 3,
                    global: true,
                    type: 'Bearer'
                },
                refreshToken: {
                    property: 'refresh',
                    data: 'refresh',
                    maxAge: 60 * 60 * 24 * 30
                },
                user: {
                    property: false,
                    // autoFetch: true
                },
                endpoints: {
                    login: { url: "/api/v1/users/token/", method: "post" },
                    refresh: { url: "/api/v1/users/token/refresh/", method: "post" },
                    logout: false, //  we don't have an endpoint for our logout in our API and we just remove the token from localstorage
                    user: { url: "/api/v1/users/user-data/", method: "get" },
                },
                // autoLogout: false
            }
        }
    },

    webfontloader: {
        google: {
            families: ['Roboto:100,300,400,500,700,900&display=swap']
        }
    },
    render: {
        bundleRenderer: {
            shouldPreload: (file, type) => {
                return ['script', 'style', 'font'].includes(type)
            }
        }
    },
    build: {
        extractCSS: true,
    }
}
