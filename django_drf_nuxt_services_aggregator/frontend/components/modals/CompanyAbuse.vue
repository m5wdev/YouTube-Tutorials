<template>
    <div class="modal fade" @change="showModal" ref="companyAbuseModal"
        id="companyAbuseModal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="companyAbuseModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="modal-title h5" id="companyAbuseModalLabel">Пожаловаться</div>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">Напишите вашу претензию, что именно вас беспокоит в данной публикации</div>

                    <div v-for="(issue, index) in issue_types" :key="index"
                        class="form-check">
                        <input class="form-check-input" name="abuse_types" :id="`issue-${index}`" type="radio"
                            :checked="false"
                            @change="changeVal(issue)"
                            >
                        <label class="form-check-label" :for="`issue-${index}`">
                            {{ issue }}
                        </label>
                    </div>

                    <template v-if="form.abuse_type === 'Указана неверная информация' ||
                                    form.abuse_type === 'Проблема в другом'
                            ">
                        <div class="mb-3">
                            <label for="issue_descr" class="form-label">Описание рроблемы</label>
                            <textarea class="form-control" id="issue_descr" rows="2" v-model="form.description"></textarea>
                        </div>
                    </template>
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
            issue_types: [
                'Этот сервисный центр ненастоящий',
                'Этот сервисный центр не работает',
                'Это мошенничество',
                'Указана неверная информация',
                'Проблема в другом',
            ],
            form: {
                company_name: this.company.name,
                abuse_type: '',
                description: '',
            },
            errors: {},
        }
    },
    methods: {
        showModal() {
            // console.log(this.$refs.companyAbuseModal)
        },
        changeVal(val) {
            this.form.abuse_type = val

            if (
                !(val === 'Указана неверная информация' ||
                val === 'Проблема в другом')
            ) {
                this.form.description = ''
            }
        },
        submitForm() {
            console.log(this.form)
            this.errors = {}

            // http://localhost:8000/api/v1/email/create-company-abuse/
            this.$axios.$post(`api/v1/email/create-company-abuse/`, this.form)
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
        }
    }
}
</script>
