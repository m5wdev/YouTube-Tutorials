<template>
    <div id="calc">
        {{old_num}} {{operator}} {{the_num}} = {{result}}
        <div id="display">
            <span v-if="!the_num && !old_num && !result">0</span>
            <span v-else-if="(the_num || old_num) && !result">{{the_num}}</span>
            <span v-else>{{result}}</span>
        </div>
        <div id="buttons">
            <div id="operators">
                <button @click="cOp">C</button>
                <button class="ops" @click="getOp('xⁿ')">xⁿ</button>
                <button @click="sqrtOp">√</button>
                <button @click="ltOp">&lt;</button>

                <button></button>
                <button></button>
                <button></button>
                <button @click="getOp('/')">/</button>
            </div>
            <div id="numbers">
                <button class="num" @click="getNum(7)">7</button>
                <button class="num" @click="getNum(8)">8</button>
                <button class="num" @click="getNum(9)">9</button>
                <button class="ops" @click="getOp('*')">*</button>

                <button class="num" @click="getNum(4)">4</button>
                <button class="num" @click="getNum(5)">5</button>
                <button class="num" @click="getNum(6)">6</button>
                <button class="ops" @click="getOp('-')">-</button>

                <button class="num" @click="getNum(1)">1</button>
                <button class="num" @click="getNum(2)">2</button>
                <button class="num" @click="getNum(3)">3</button>
                <button class="ops" @click="getOp('+')">+</button>

                <button @click="pmOp">+/-</button>
                <button class="num" @click="getNum(0)">0</button>
                <button @click="addDot">.</button>
                <button id="eq" @click="calc">=</button>
            </div>
        </div>
    </div>
</template>

<script>
import {
    sqrt, add, format, evaluate
} from 'mathjs'

export default {
    data() {
        return {
            the_num : '',
            old_num : '',
            operator : '',
            result : '',
        }
    },
    methods : {
        clearVal() {
            this.old_num = ''
            this.the_num = ''
            this.operator = ''
            this.result = ''
        },
        getNum(num) {
            this.the_num += num.toString()
        },
        getOp(op) {
            this.operator = (op === 'xⁿ') ? '**' : op
            this.old_num = parseFloat(this.the_num)
            this.the_num = ''
        },
        sqrtOp() {
            this.result = Math.sqrt(this.the_num)
        },
        cOp() {
            this.clearVal()
        },
        calc() {
            this.the_num = parseFloat(this.the_num)
            if (this.operator && this.old_num) {
                const result = evaluate(`${this.old_num} ${this.operator} ${this.the_num}`)
                this.result = format(result, {precision: 14})
                //this.clearVal()
            }
        },
        addDot() {
            let text_dot = this.the_num.toString()
            if (text_dot.indexOf('.') === -1) {
                this.the_num = text_dot + '.'
            }
        },
        ltOp() {
            let text_lt = this.the_num.toString()
            text_lt = text_lt.slice(0, -1)
            this.the_num = parseFloat(text_lt)

            if (!this.the_num) {
                // NaN protect
                this.the_num = ''
            }
        },
        pmOp() {
            this.the_num = this.the_num * -1
        }
    },
}
</script>

<style>
body {
    font-family: sans-serif;
}

button {
    border: none;
    outline: none;
}

#calc {
    width: 500px;
    word-break: break-all;
    background-color: rgb(212, 212, 212);
    margin: 0 auto;
}

#numbers {
    padding: 0 5px 5px 5px;
    display: grid;
    /*grid-template-columns: 1fr 1fr 1fr 1fr;*/
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
    opacity: 0.8;
}

#numbers button:nth-child(4n) {
    background-color: #eee;
}

#operators {
    padding: 5px;
    display: grid;
    /*grid-template-columns: 1fr 1fr 1fr 1fr;*/
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 5px;
}

#operators button {
    background-color: #eee;
}

#display {
    min-height: 150px;
    font-size: 3.3rem;
    display: flex;
    align-items: center;
    justify-content: end;
    padding: 10px;
}

#eq {
    background-color: #72a2c8 !important;
}
</style>
