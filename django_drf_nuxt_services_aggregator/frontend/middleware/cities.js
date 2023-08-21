export default async function ({ app, store, req, redirect, $cookies }) {
  // console.log('middleware cities.js')
  try {
    let host = process.env.API_BASE_URL || 'http://localhost:8000/api/v1/'
    // let host = process.env.API_BASE_URL || 'http://backend/api/v1/'

    // const url = `${host}cities/name/?slug_city=${req.headers.host.split('.')[0]}`
    // console.log('req.headers', req.headers);

    let slug = req.headers.host.split('.')[0]
    // if(slug === 'localhost' || 'servis-centers.ru'){
    //     slug = 'moscow'
    // }
    console.log(444,slug);

    const url = `${host}cities/name/?slug_city=${slug}`

    const response = await fetch(url)
    // console.log('resp', response);
    if (response.ok) {
      const json = await response.json()
      console.log(444,slug,json);
      store.commit("cities/setactiveCity", json)
    }
    // console.log(req.headers);
    // console.log(req.headers.host);
  } catch (error) {
      console.log('errrrr');
    // console.log('req.headers',error);
  }
}
