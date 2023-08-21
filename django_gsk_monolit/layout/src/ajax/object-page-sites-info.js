import {formatNumber, formatNumberText} from "../modules/format-number"


function objectPageSitesInfo() {
    if ( $('#section-object-page-main-info').data('sites-info-api-url') ) {
        const site_info_url = $('#section-object-page-main-info').data('sites-info-api-url')

        $.getJSON(site_info_url, (data) => {
            const objectStats = data[0]

            if ( objectStats['object_total_sites_qty'] === 0 ) {
                $('#section-object-page-main-info__stats').remove()
            } else {
                $('.obj-area-min').append('<small>от</small> ' + formatNumber(objectStats['object_min_site_area'], 2))
                $('.obj-area-max').append('<small>до</small> ' + formatNumber(objectStats['object_max_site_area'], 2) + ' <small>м<sup>2</sup></small>')
                $('.obj-min-price').append('<small>от</small> ' + formatNumber(objectStats['object_min_site_price'], 0) + ' <small>руб.</small>')

                // Show objects qty in commercial object page
                if ( $('.commercial-object-page').length ) {
                    $('#commercial-qty-block__number').html(objectStats['object_total_sites_qty'])
                }
            }
        })
    }
}


function objectPageSitesTypesInfo() {
    if ( $('#section-object-page-main-info').data('sites-info-api-url') ) {
        const site_info_url = $('#section-object-page-main-info').data('sites-info-api-url')
        const sectionFlatsType = $('#section-sites-types')

        $.getJSON(site_info_url, (data) => {
            // const objectStats = data[0]
            const objectSitesInfo = data[1]['sites_info']

            $.each(objectSitesInfo, (index, el) => {
                let site_card = sectionFlatsType.find('.site-type-card__room-'+index)

                if ( el['sites_qty'] > 0 ) {
                    site_card.addClass('active')
                    site_card.find('.site-type-card__info--area').append('от ' + formatNumber(el['min_area'], 1) + '<br>до ' + formatNumber(el['max_area'], 1) + ' м<sup>2</sup>' )
                    site_card.find('.site-type-card__info--price').append('от ' + formatNumberText(el['min_price']) + ' руб.' )
                }
            })
        })
    }
}


function mainSliderObjectSitesInfo() {
    $('#main-slider .carousel-item').each((index, el) => {
        let site_info_url = $(el).find('.slide').data('sites-info-api-url')

        $.getJSON(site_info_url, (data) => {
            let objectStats = data[0]

            if ( objectStats['object_total_sites_qty'] === 0 ) {
                $(el).find('.caption-info').empty()
            } else {
                $(el).find('.caption-info__area .caption-info__value').append('от ' + formatNumber(objectStats['object_min_site_area'], 2) + ' до ' + formatNumber(objectStats['object_max_site_area'], 2) + ' м<sup>2</sup>')
                $(el).find('.caption-info__price .caption-info__value').append('от ' + formatNumber(objectStats['object_min_site_price'], 0) + ' руб.')
            }
        })
    })
}


export {objectPageSitesInfo, objectPageSitesTypesInfo, mainSliderObjectSitesInfo}
