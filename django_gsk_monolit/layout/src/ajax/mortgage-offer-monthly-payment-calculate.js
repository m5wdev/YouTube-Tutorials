import {formatNumber} from "../modules/format-number"

/*
    [ Расчет ежемесячного платежа по ипотеке ]

    Расчет ипотеки для аннуитетных платежей
    https://mortgage-calculator.ru/%D1%84%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0-%D1%80%D0%B0%D1%81%D1%87%D0%B5%D1%82%D0%B0-%D0%B8%D0%BF%D0%BE%D1%82%D0%B5%D0%BA%D0%B8

    Ежемесячный процент
    Возьмем годовую процентную ставку (пусть 11.5%), поделим на 100 и получим 0.115. Посчитаем, какую часть это годовой процентной ставки надо платить ежемесячно. Для этого поделим полученное число 0.115 на 12: получаем 0.009583. Полученное число будем называть ежемесячным процентом. Итого, ежемесячный процент считается по формуле:
    ежемесячный процент = (процентная ставка годовых) / 100 / 12

    Ежемесячный платеж
    Итак, мы рассчитали ежемесячный процент, теперь на его основе рассчитаем размер ежемесячного платежа. Мы должны определить для себя сумму ипотечного кредита в рублях и срок кредитования. Для расчета размера ежемесячного платежа воспользуемся формулой:
    tmp = (1 + ежемесячный процент) ^ (срок кредитования)
    ежемесячный платеж = (сумма ипотечного кредита) * (ежемесячный процент) * tmp / (tmp - 1)

    Крышка (^) - это возведение в степень. Если мы берем ипотечный кредит на сумму 1.500.000 рублей на 20 лет, то
    tmp = (1 + 0.009583) ^ (20 лет * 12 месяцев/год) = 9.8647
    ежемесячный платеж = 1.500.000 рублей * 0.009583 * 9.8647 / (9.8647 - 1) = 15.996 рублей

    Корректность расчета можно проверить на https://www.rshb.ru/natural/loans/mortgage/
*/

function monthlyPaymentCalculate(site_price_total, first_payment_from, rate_from, years) {
    // Сумма первоначального взноса в руб
    let first_payment_rub = (site_price_total / 100) * first_payment_from
    // Сумма займа в рублях
    let loan_rub = site_price_total - first_payment_rub
    // Кол-во месяцев в годах
    let months = years * 12

    // Расчет ежемесячного платежа
    let monthly_rate = rate_from / 100 / 12
    let tmp = (1 + monthly_rate) ** months
    let monthly_payment = (loan_rub * monthly_rate) * (tmp / (tmp - 1))

    return monthly_payment
}


function generateRandomNumInRange(num1, num2) {
    return Math.floor(Math.random() * (num2 - num1)) + num1
}


function mortgageOfferMonthlyPayment() {
    if ( $('#section-site-page-content').data('object-site') ) {
        const site_info_url = $('#section-site-page-content').data('object-site')

        if ( $('#section-site-page-mortgage') ) {
            $.getJSON(site_info_url, (site_info_data) => {
                // Стоимость квартиры
                const site_price_total = site_info_data[0]['price_total']

                $('.mortgage-offer').each((index, el) => {
                    let mortgage_offer_api_url = $(el).data('api-mortgage-offer')

                    $.getJSON(mortgage_offer_api_url, (mortgage_offer_data) => {
                        let offer_id = mortgage_offer_data[0]['id']

                        // Первоначальный платеж
                        let first_payment_from = mortgage_offer_data[0]['first_payment_from']
                        let first_payment_to = mortgage_offer_data[0]['first_payment_to']

                        // Срок кредита
                        let loan_term_from = mortgage_offer_data[0]['loan_term_from']
                        let loan_term_to = mortgage_offer_data[0]['loan_term_to']

                        // % ставка
                        let rate_from = mortgage_offer_data[0]['rate_from']
                        let rate_to = mortgage_offer_data[0]['rate_to']

                        // Create loan term slider
                        let loan_term_slider_id = 'loan_term_slider_' + offer_id
                        let loan_term_slider_years_id = 'loan_term_years_' + offer_id

                        $(el).find('.mortgage-offer__pay-off .mortgage-offer__val').append('<div id="' + loan_term_slider_years_id + '" class="mortgage-offer__years"></div>' +
                                                                                           '<div id="' + loan_term_slider_id + '"></div>')

                        // Create loan term slider
                        let loanTermSlider = document.getElementById(loan_term_slider_id)
                        noUiSlider.create(loanTermSlider, {
                            behaviour: 'snap',
                            start: generateRandomNumInRange(loan_term_from, loan_term_to),
                            step: 1,
                            connect: [true, false],
                            range: {
                                'min': loan_term_from,
                                'max': loan_term_to
                            },
                            format: {
                                to: (value) => {
                                    return Math.round(value)
                                },
                                from: (value) => {
                                    return Math.round(value)
                                }
                            }
                        })
                        // END Create loan term slider

                        // loan term slider Changed
                        loanTermSlider.noUiSlider.on('update', (years) => {
                            $('#' + loan_term_slider_years_id).empty()
                            $('#' + loan_term_slider_years_id).html(years + ' лет')

                            let monthly_payment = monthlyPaymentCalculate(site_price_total, first_payment_from, rate_from, years)
                            $(el).find('.mortgage-offer__monthly-payment .mortgage-offer__val').empty()
                            $(el).find('.mortgage-offer__monthly-payment .mortgage-offer__val').html( formatNumber(monthly_payment, 2) + ' руб')
                        })
                        // END loan term slider Changed
                    })
                })
            })
        }
    }
}


export {mortgageOfferMonthlyPayment}
