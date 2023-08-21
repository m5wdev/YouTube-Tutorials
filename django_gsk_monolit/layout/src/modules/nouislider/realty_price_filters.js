// noUiSlider for realty square filter in homepage
// https://refreshless.com/nouislider/examples/#section-html5

function realtyPriceFilters() {
    const realtyPriceSlider = document.getElementById('realty-filter__price-slider')
    let urlParams = new URLSearchParams(window.location.search)

    // Get min & max price from data attributes
    const min_price = $('#section-realty-sites-filters__price-block').data('min-price')
    const max_price = $('#section-realty-sites-filters__price-block').data('max-price')

    noUiSlider.create(realtyPriceSlider, {
        // start: [2919000, 18360000],
        // start: (urlParams.has('price_min')) ? [urlParams.get('price_min'), urlParams.get('price_max')] : [2919000, 18360000],
        start: (urlParams.has('price_min')) ? [urlParams.get('price_min'), urlParams.get('price_max')] : [min_price, max_price],
        // step: 1,
        behaviour: 'drag',
        connect: true,
        range: {
            // 'min': 2919000,
            'min': min_price,
            // 'max': 18360000,
            'max': max_price,
        }
    })

    const inputNumberMin = document.getElementById('realty-filter__price--input-min')
    const inputNumberMax = document.getElementById('realty-filter__price--input-max')

    realtyPriceSlider.noUiSlider.on('update', function(values, handle) {
        let value = values[handle]

        if (handle) {
            inputNumberMax.value = Math.round(value)
        } else {
            inputNumberMin.value = Math.round(value)
        }
    })

    inputNumberMin.addEventListener('change', function() {
        realtyPriceSlider.noUiSlider.set([this.value, null])
    })
    inputNumberMax.addEventListener('change', function() {
        realtyPriceSlider.noUiSlider.set([null, this.value])
    })
}


export {realtyPriceFilters}
