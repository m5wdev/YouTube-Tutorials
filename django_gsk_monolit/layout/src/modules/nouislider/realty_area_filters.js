// noUiSlider for realty square filter in homepage
// https://refreshless.com/nouislider/examples/#section-html5

function realtyAreaFilters() {
    const realtySquareSlider = document.getElementById('realty-filter__area-slider')
    let urlParams = new URLSearchParams(window.location.search)

    // Get min & max area from data attributes
    const min_area = $('#section-realty-sites-filters__area-block').data('min-area')
    const max_area = $('#section-realty-sites-filters__area-block').data('max-area')

    noUiSlider.create(realtySquareSlider, {
        // start: [35, 245],
        // start: (urlParams.has('area_min')) ? [urlParams.get('area_min'), urlParams.get('area_max')] : [35, 245],
        start: (urlParams.has('area_min')) ? [urlParams.get('area_min'), urlParams.get('area_max')] : [min_area, max_area],
        // step: 1,
        connect: true,
        range: {
            // 'min': 35,
            'min': min_area,
            // 'max': 245,
            'max': max_area,
        }
    })

    const inputNumberMin = document.getElementById('realty-filter__area--input-min')
    const inputNumberMax = document.getElementById('realty-filter__area--input-max')

    realtySquareSlider.noUiSlider.on('update', function(values, handle) {
        let value = values[handle]

        if (handle) {
            inputNumberMax.value = Math.round(value)
        } else {
            inputNumberMin.value = Math.round(value)
        }
    })

    inputNumberMin.addEventListener('change', function() {
        realtySquareSlider.noUiSlider.set([this.value, null])
    })
    inputNumberMax.addEventListener('change', function() {
        realtySquareSlider.noUiSlider.set([null, this.value])
    })
}

export {realtyAreaFilters}
