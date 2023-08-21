export default function ({ app, store, req, redirect }) {
  try {
    // if (req.headers.host === 'localhost') {
    //   // redirect('http://moscow.localhost:3000')
    //   redirect('http://localhost:3000')
    // }
    // if (req.headers.host === 'localhost:3000') {
    //   // redirect('http://moscow.localhost:3000')
    //   redirect('http://localhost:3000')
    // }
    // if (req.headers.host === 'moscow.localhost:3000') {
    //   // redirect('http://moscow.localhost:3000')
    //   redirect('http://localhost:3000')
    // }

    if (req.url === '/sitemap.xml') {
      redirect('http://servis-centers.ru:8001/sitemap.xml')
    }

    // if (req.headers.host === 'moscow.localhost') {
    //   redirect('http://servis-centers.ru:8000')
    // }
    // if (req.headers.host === 'moscow.localhost:8000') {
    //   redirect('http://servis-centers.ru:8000')
    // }

    if (req.headers.host === 'moscow.servis-centers.ru') {
      // redirect('http://servis-centers.ru:8000')
      redirect('http://servis-centers.ru')
    }
    // if (req.headers.host === 'moscow.servis-centers.ru:8000') {
    //   // redirect('http://servis-centers.ru:8000')
    //   redirect('http://servis-centers.ru')
    // }

    // if (req.headers.host === 'servis-centers.ru') {
    //   // redirect('http://moscow.servis-centers.ru:3000/')
    //   redirect('http://servis-centers.ru:3000/')
    // }
  } catch (error) {
    // console.error(error);
  }
}
