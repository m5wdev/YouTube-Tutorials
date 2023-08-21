<template>
    <div id="formula">
        {{ old_num }} {{ operator }} {{ the_num }}<span v-if="result">&nbsp;= {{ result }}</span>
        <!-- {{ test_prop }} -->
    </div>
</template>

<script>
export default {
    props: {
        old_num: [Number, String],
        operator: String,
        the_num: [Number, String],
        result: [Number, String],
        test_prop: String,
    },
    // props: [
    //     old_num,
    //     operator,
    //     the_num,
    //     result,
    //     test_prop,
    // ],
}
</script>

<style scoped>
#formula {
    opacity: .5;
    padding: 5px;
    min-height: 30px;
    display: flex;
    align-items: center;
    justify-content: end;
}
</style>
