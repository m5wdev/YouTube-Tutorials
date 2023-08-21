<template>
    <div class="modal fade"
        @change="showModal" ref="applicationModal"
        id="applicationModal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="applicationModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title h5" id="applicationModalLabel">Оставить заявку в компанию</div>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="application_name" class="form-label">Имя <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="application_name" v-model="form.name" placeholder="Ваше Имя">
                        <template v-if="errors">
                            <div v-for="(error, index) in errors.name" :key="index"
                                class="text-danger">
                                {{ error }}
                            </div>
                        </template>
                    </div>
                    <div class="mb-3">
                        <label for="application_phone" class="form-label">Телефон <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="application_phone" v-model="form.phone" placeholder="+7 000 000-00-00">
                        <template v-if="errors">
                            <div v-for="(error, index) in errors.phone" :key="index"
                                class="text-danger">
                                {{ error }}
                            </div>
                        </template>
                    </div>
                    <div class="mb-3">
                        <label for="application_issue" class="form-label">Что сломалось? <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" id="application_issue" v-model="form.issue_type" placeholder="Кофемашина, Утюг, Монитор, Телефон...">
                        <template v-if="errors">
                            <div v-for="(error, index) in errors.issue_type" :key="index"
                                class="text-danger">
                                {{ error }}
                            </div>
                        </template>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="application_personal_data" v-model="form.personal_data" checked>
                        <label class="form-check-label" for="application_personal_data">
                            Согласен на обработку персональных данных
                        </label>
                        <div v-if="form.personal_data !== true" class="text-danger">
                            Вы должны согласиться с условиями обработки персональных данных
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" @click.prevent="submitForm">Отправить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['company'],
    data() {
        return {
            form: {
                name: '',
                phone: '',
                issue_type: '',
                personal_data: true,
            },
            errors: {},
        }
    },
    methods: {
        showModal() {
            // console.log(this.$refs.applicationModal)
        },
        submitForm() {
            this.errors = {}
            // console.log('submitForm()')
            // console.log(this.name, this.phone, this.issue_type, this.personal_data, this.company.name)

            if (this.form.personal_data) {
                // Submit data to server
                // const data = {
                //     name: this.name,
                //     phone: this.phone,
                //     // email: this.email,
                //     issue_type: this.issue_type,
                //     description: this.description,
                // }
                console.log(this.form)

                // http://localhost:8000/api/v1/email/create-company-application/
                this.$axios.$post(`api/v1/email/create-repair-application/`, this.form)
                        .then(res => {
                            // console.log(res, data)
                            console.log(res)
                            console.log(res.response)

                            // this.name = ''
                            // this.phone = ''
                            // this.email = ''
                            // this.issue_type = ''
                            // this.description = ''
                            // this.company.name = ''
                            // this.errors = {}
                        })
                        .catch(error => {
                            if (error.response.data) {
                                this.errors = {...error.response.data}
                            }
                        })
            } else {
                // fill errors
                console.error('Нет согласия на обработку персональных данных')
            }
        }
    }
}
</script>
