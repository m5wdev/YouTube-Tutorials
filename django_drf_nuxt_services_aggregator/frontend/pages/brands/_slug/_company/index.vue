<template>
  <div>
    <h1>Компания {{ $route.params.slug }}</h1>
    <h2>{{ post.title }}</h2>

    <div class="container">
      <div class="row">
        <div class="col-12 col-lg-9">
          <!-- Карта -->
          <section id="section-title">
            <div class="row">
              <div class="col-12">
                <div class="card-company">
                  <div class="row">
                    <div class="col-8">
                      <div class="d-flex">
                        <img height="23" width="23" src="/icon.png" alt="" />
                        <h4 class="ml-2 name-company ">Сервисный центр СМС-ЯСЕНЕВО</h4>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="row">
                        <div class="col-8">

                        </div>
                        <div class="col-4">
                          <strong>1отзыв</strong>
                        </div>
                      </div>
                    </div>
                  </div>
<!--  карта яндекс /components/forms/YandexCard -->
                  <FormsYandexCard />
                </div>
              </div>
            </div>
          </section>

          <!-- О сервисе -->
          <section id="section-about">
            <div class="card-company">
              <div class="d-flex">
                <img height="23" width="23" src="/icon.png" alt="" />
                <h4 class="ml-2">О сервисе</h4>
              </div>

              <div class="row justify-content-center mt-4">
                <div v-for="i in 6" :key="i.id" class="col-2">
                    <!-- доп услуги копании(выезд курьера и т д) -->
                  <div
                    class="
                    dop-services
                      d-flex
                      flex-column
                      align-items-center
                      justify-content-center
                    "
                  >
                    <img height="43" width="43" src="/icon.png" alt="" />
                    <p>Бесплатная диагностика</p>
                  </div>
                </div>
              </div>
              <hr />
              <div>
                <p>
                  Ремонт цифровой, мобильной , мелкой бытовой техники, умных
                  устройств и гаджетов, а так же многое другое!
                  <br>
                  ПОЧИНИМ ВСЕ!
                </p>
                <p>Вход в здание МГТС первый этаж.</p>
              </div>
              <hr />
              <div class="row">
                <div v-for="i in 4" :key="i.id" class="col-3">
                  <img
                    width="150"
                    height="auto"
                    src="https://www.apple.com/newsroom/images/tile-images/apple_global-repair-update_082919.jpg.news_app_ed.jpg"
                    alt=""
                  />
                </div>
              </div>
            </div>
          </section>
          <!-- Виды техники -->
          <section id="tehnick">
            <div class="card-company">
              <div class="d-flex">
                <img height="23" width="23" src="/icon.png" alt="" />
                <h4 class="ml-2">Виды техники</h4>
              </div>
              <div class="row mt-4">
                <div v-for="i in 4" :key="i.id" class="col-6 mt-3">
                  <div class="box-tehnik">
                    <div class="d-flex">
                      <img height="23" width="23" src="/icon.png" alt="" />
                      <h6 class="ml-2">Аудио-видео техника</h6>
                    </div>
                    <p>
                      Телевизоры, усилители, пульты ду, игровые приставки,
                      камеры видеонаблюдения, домашние кинотеатры, музыкальные
                      центры, акустические системы, тв-ресиверы, антенны,
                      кассетные деки, микрофоны, караоке, медиаплееры, проекторы
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>
          <section id="section-brands">
            <div class="card-company">
              <div class="d-flex">
                <img height="23" width="23" src="/icon.png" alt="" />
                <h4 class="ml-2">Бренды</h4>
              </div>
              <div class="row mt-4">
                <div v-for="i in 12" :key="i.id" class="col-2">
                  <span>Acer</span>
                </div>
              </div>
              <div class="mt-4">
                <Nuxt-link to="#">Показать еще</Nuxt-link>
              </div>
            </div>
          </section>

          <section id="section-comments">
            <div class="card-company mt-4 mb-4">
              <div class="row">
                <div class="col-6">
                  <div class="d-flex">
                    <img height="23" width="23" src="/icon.png" alt="" />
                    <h4 class="ml-2">Отзывы</h4>
                  </div>
                </div>
                <div class="col-6 text-right">
                  <button type="button" class="btn btn-primary">
                    Написать
                  </button>
                </div>
              </div>
            </div>
          </section>

          <section id="section-search">
            <div class="card-company mt-4 mb-4">
              <div class="row">
                <div class="col-12">

                </div>
              </div>
            </div>
          </section>

          <section id="section-list-comments">
            <div class="card-company mt-4 mb-4">
              <div class="row">
                <div class="col-9">
                  <div class="d-flex">
                    <img
                      height="43"
                      width="39"
                      src="https://media.istockphoto.com/photos/portrait-of-handsome-latino-african-man-picture-id1007763808?k=20&m=1007763808&s=612x612&w=0&h=q4qlV-99EK1VHePL1-Xon4gpdpK7kz3631XK4Hgr1ls="
                      alt=""
                    />
                    <div class="d-flex flex-column">
                      <span style="font-weight: 600" class="ml-2"
                        >Попков Евгений</span
                      >
                      <span class="ml-2">22 мая 2021 г., 12:58</span>
                    </div>
                  </div>
                </div>
                <div class="col-3 text-right d-flex flex-column">
                  <div>

                    <div class="text-left">
                      <span class="ml-3">Оценил(а) на {{ value }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <hr />
              <div>
                <br>
                <p style="width: 90%">
                  Однозначно это лучший сервисный цент в районе Ясенево!
                  Ремонтировал ноутбук, сделали быстро и вполне бюджетно!
                  Спасибо ребята, буду Вас рекомендовать друзьям!
                </p>
              </div>
              <br>
              <hr />
              <p>Этот отзыв является субьективным мнением пользователя</p>

              <hr />
              <button type="button" class="btn btn-outline-primary">
                Нравиться
              </button>
            </div>
          </section>

          <section id="section-comments">
            <div class="card-company mt-4 mb-4">
              <div class="row">
                <div class="col-12">
                  <div class="d-flex">
                    <h4 class="ml-2">Часто ремонтируемые</h4>
                  </div>
                  <div class="d-flex flex-wrap">
                    <div
                      class="p-2"
                      v-for="subcategory in 24"
                      :key="subcategory.id"
                    >
                      <button
                        style="
                          border-radius: 15px;
                          background: #ecf4fe;
                          color: #1890ff;
                        "
                        type="button"
                        class="btn btn-outline-secondary"
                      >
                        iphone
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
          <section id="section-comments">
            <div class="card-company mt-4 mb-4">
              <div class="row">
                <div class="col-12">
                  <div
                    style="
                      background: #86efff;
                      padding: 1em;
                      border-radius: 12px;
                    "
                  >
                    <p>
                      Вы владелец этой компании? Зарегистрируйтесь и Вы сможете
                      изменять информацию о компании, отвечать на отзывы и
                      вопросы.
                    </p>
                  </div>
                  <button type="button" class="btn btn-primary mt-4">
                    Регистрация владельца
                  </button>
                </div>
              </div>
            </div>
          </section>
        </div>
        <div class="col-12 col-lg-3">
          <div class="card-company">
            <button type="button" class="btn btn-primary" style="width: 100%">
              +7 345 567 89 09
            </button>
            <button
              style="width: 100%"
              type="button"
              class="btn mt-3 btn-outline-secondary"
            >
              Оставить заявку
            </button>
            <hr />
            <Nuxt-link to="#">sms.yasenevo@gmail.com</Nuxt-link>
            <hr />
            <Nuxt-link to="#"> Сегодня работает до 21 </Nuxt-link>
            <button type="button" class="btn mt-2 btn-secondary">
              ясенево
            </button>
            <hr />
            <span class="">Адрес</span>
            <br>
            <span class="mt-2">Москва, Ясногорская д5, Ясногорская д5</span>
            <br>
            <Nuxt-link class="mt-2" to="#">+7 (995) 299-09-90</Nuxt-link>
            <hr />
          </div>

          <div class="card-company">
            <div v-for="i in 4" :key="i.id">
              <div class="d-flex mt-3">
                <img height="23" width="23" src="/icon.png" alt="" />
                <h6 class="ml-2">О сервисе</h6>
              </div>
            </div>
          </div>

          <div class="mt-3">
            <button type="button" class="btn btn-primary btn-sm">
              Написать отзыв
            </button>
            <button type="button" class="btn btn-outline-secondary btn-sm">
              Задать вопрос
            </button>
          </div>
          <div class="mt-3">
            <button
              style="width: 100%"
              type="button"
              class="btn btn-outline-secondary"
            >
              Пожаловаться
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: `Компания ${ $route.params.slug }`,
      meta: [
        // TODO: og:url
        // {
        //   hid: `og:url`,
        //   name: "og:url",
        //   content: `https://sankt-peterburg.servis-centers.ru`,
        // },
      ],
    };
  },
  async asyncData({ route, $axios }) {
    let company = await $axios.get(`/api/v1/companies/company/${route.params.company}/`);
    return { company: company.data };
  },
  data() {
    return {
    }
  },
};
</script>


<style>
.card-company {
  background: white;
  padding: 1em;
  border-radius: 8px;
  margin-top: 3em;
}
.box-tehnik {
  background: #f5f7fb;
  padding: 1em;
}
</style>
