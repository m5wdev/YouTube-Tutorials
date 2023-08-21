<template>
    <div id="display">
        <!-- <span v-if="!the_num && !old_num && !result">0</span>
        <span v-else-if="(the_num || old_num) && !result">{{ the_num }}</span>
        <span v-else>{{ result }}</span> -->
        {{ showResult }}
    </div>
</template>

<script>
export default {
    props: {
        old_num: [Number, String],
        the_num: [Number, String],
        result: [Number, String],
    },
    // TIP: Use computed property helps avoid bloating in html template
    computed: {
        showResult() {
            if (!this.the_num && !this.old_num && !this.result) {
                return 0
            } else if ((this.the_num || this.old_num) && !this.result) {
                return this.the_num
            } else {
                return this.result
            }
        }
    },
}
</script>

<style scoped>
#display {
    min-height: 150px;
    font-size: 2.9rem;
    display: flex;
    align-items: center;
    justify-content: end;
    padding: 10px;
    margin-top: -30px;
}
</style>
