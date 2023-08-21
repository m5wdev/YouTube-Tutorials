function formatNumber(number, precision=0) {
    number = parseFloat(number).toFixed(precision)
    // Fix NaN issue
    if (isNaN(number)) {
        number = ''
    }
    let result = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    let split_result = result.split('.')
    // console.log( 'part 1: ' + split_result[0] )
    // console.log( 'part 2: ' + split_result[1] )
    if (typeof split_result[1] !== 'undefined') {
        if ( split_result[1] === '0' || split_result[1] === '00' || split_result[1] === '000' ) {
            result = split_result[0]
        }
    }
    return result
}


// https://raymondcamden.com/2012/07/06/Simple-JavaScript-number-format-function-and-an-example-of-Jasmine
function formatNumberText(number, precision=1) {
    if (isNaN(number)) return number

    if (number < 9999) {
        return number
    }
    // if (number < 1000000) {
    //     return Math.round(number / 1000) + ' тыс'
    // }
    if (number < 10000000) {
        number = (number / 1000000).toFixed(precision)
        // return (number / 1000000).toFixed(precision) + ' млн'
        return number.replace('.0', '').replace('.00', '') + ' млн'
    }
}


export {formatNumber, formatNumberText}
