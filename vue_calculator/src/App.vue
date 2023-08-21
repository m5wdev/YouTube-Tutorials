<template>
    <div id="calc">
        <!-- <div id="formula">
            {{ old_num }} {{ operator }} {{ the_num }} = {{ result }}
        </div> -->
        <Formula
            test_prop="test_prop"
            :old_num="old_num"
            :operator="operator"
            :the_num="the_num"
            :result="result"
        />

        <!-- <div id="display">
            <span v-if="!the_num && !old_num && !result">0</span>
            <span v-else-if="(the_num || old_num) && !result">{{ the_num }}</span>
            <span v-else>{{ result }}</span>
        </div> -->
        <Display
            :old_num="old_num"
            :the_num="the_num"
            :result="result"
        />

        <div id="buttons">
            <div id="operators">
                <button class="ops" @click="clearAll">C</button>
                <button></button>
                <button></button>
                <button class="ops" @click="ltOp">&lt;</button>

                <button class="ops" @click="sqrtOp">&radic;</button>
                <button class="ops" @click="getOp('xⁿ')">xⁿ</button>
                <button class="ops" @click="toPow2">x²</button>
                <button class="ops" @click="getOp('/')">&divide;</button>
            </div>
            <div id="numbers">
                <button class="num" @click="getNum(7)">7</button>
                <button class="num" @click="getNum(8)">8</button>
                <button class="num" @click="getNum(9)">9</button>
                <button class="ops" @click="getOp('*')">&times;</button>

                <button class="num" @click="getNum(4)">4</button>
                <button class="num" @click="getNum(5)">5</button>
                <button class="num" @click="getNum(6)">6</button>
                <button class="ops" @click="getOp('-')">&ndash;</button>

                <button class="num" @click="getNum(1)">1</button>
                <button class="num" @click="getNum(2)">2</button>
                <button class="num" @click="getNum(3)">3</button>
                <button class="ops" @click="getOp('+')">+</button>

                <button @click="pmOp">+/-</button>
                <!-- <button class="num" @click="getNum(0)">0</button> -->
                <Button
                    btn_class="num"
                    btn_text="0"
                    @click="getNum(0)"
                />
                <button @click="addDot">.</button>

                <!-- <button id="eq" @click="calc">=</button> -->
                <!-- <Button
                    id="eq"
                    @click="calc"
                    btn_text="="
                /> -->
                <!-- <ButtonEquals @click="calc" /> -->
                <ButtonEquals
                    @claculateEvent="getMyEvent"
                />
            </div>
        </div>
    </div>
</template>

<script>
// Math docs: https://github.com/josdejong/mathjs
import { format, evaluate, pow, sqrt } from 'mathjs'

import Formula from '@/components/Formula'
import Display from '@/components/Display'
import Button from '@/components/buttons/Button'
import ButtonEquals from './components/buttons/ButtonEquals'


export default {
    components: {
        Formula,
        Display,
        Button,
        ButtonEquals,
    },

    data() {
        return {
            the_num:  '',
            old_num:  '',
            operator: '',
            result:   '',
            history:  [],
        }
    },

    methods: {
        getMyEvent(payload) {
            console.log('Hi, i\'m from emit')
            console.log(payload)
            this.calc()
        },

        clearAll() {
            this.old_num  = ''
            this.the_num  = ''
            this.operator = ''
            this.result   = ''
        },

        getNum(num) {
            this.the_num += num.toString()
            // this.the_num = parseFloat(this.the_num)
        },
        toPow2() {
            this.operator = 'x²'
            this.old_num = this.the_num
            this.the_num = ''
            this.result = pow(this.old_num, 2)
        },
        getOp(op) {
            this.operator = (op === 'xⁿ') ? '**' : op

            if (!this.result) {
                this.old_num = this.the_num
            }
            if (this.result) {
                this.old_num = this.result
            }

            this.addDot()
            this.the_num = ''
        },
        sqrtOp() {
            this.old_num = ''
            this.operator = '√'
            if (this.the_num && !this.result) {
                this.result = format(sqrt(this.the_num), {precision: 14})
            } else if (this.result && this.the_num) {
                this.the_num = this.result
                this.result = format(sqrt(this.result), {precision: 14})
            }
        },
        calc() {
            if (this.the_num && this.operator && this.old_num) {
                let res
                if (this.operator === '**') {
                    res = pow(this.old_num, this.the_num)
                } else {
                    res = evaluate(`${this.old_num} ${this.operator} ${this.the_num}`)
                }
                this.result = format(res, {precision: 14})
            }
        },
        addDot() {
            const text_dot = this.the_num.toString()
            if (text_dot.indexOf('.') === -1) {
                this.the_num = text_dot + '.'
            }
        },
        ltOp() {
            let text_lt = this.the_num.toString()
            text_lt = text_lt.slice(0, -1)
            this.the_num = parseFloat(text_lt)

            // if (!this.the_num) {
            //     // NaN protect
            //     this.the_num = ''
            // }
        },
        pmOp() {
            this.the_num = this.the_num * -1
        }
    },
}
</script>

<style>
#calc {
    width: 500px;
    word-break: break-all;
    background-color: rgb(212, 212, 212);
    margin: 30px auto 0;
}

#numbers {
    padding: 0 5px 5px 5px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 5px;
}

#buttons button {
    height: 70px;
    background-color: white;
    font-size: 1.2rem;
    font-weight: 500;
    transition: all ease-in-out 0.4;
}

#buttons button:hover {
    cursor: pointer;
    opacity: .8;
}

#numbers button:nth-child(4n) {
    background-color: #eee;
}

#operators {
    padding: 5px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 5px;
}

#operators button {
    background-color: #eee;
}

.ops {
    font-size: 1.6rem !important;
}
</style>
