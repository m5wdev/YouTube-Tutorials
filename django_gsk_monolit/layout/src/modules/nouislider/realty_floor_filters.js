// noUiSlider for realty square filter in homepage
// https://refreshless.com/nouislider/examples/#section-html5

function realtyFloorFilters() {
    const realtyFloorSlider = document.getElementById('realty-filter__floor-slider')
    let urlParams = new URLSearchParams(window.location.search)

    // Get min & max floor from data attributes
    const min_floor = $('#section-realty-sites-filters__floor-block').data('min-floor')
    const max_floor = $('#section-realty-sites-filters__floor-block').data('max-floor')

    noUiSlider.create(realtyFloorSlider, {
        // start: [1, 35],
        // start: (urlParams.has('floor_min')) ? [urlParams.get('floor_min'), urlParams.get('floor_max')] : [1, 35],
        start: (urlParams.has('floor_min')) ? [urlParams.get('floor_min'), urlParams.get('floor_max')] : [min_floor, max_floor],
        // step: 1,
        connect: true,
        range: {
            // 'min': 1,
            'min': min_floor,
            // 'max': 35,
            'max': max_floor,
        }
    })

    const inputNumberMin = document.getElementById('realty-filter__floor--input-min')
    const inputNumberMax = document.getElementById('realty-filter__floor--input-max')

    realtyFloorSlider.noUiSlider.on('update', function(values, handle) {
        let value = values[handle]

        if (handle) {
            inputNumberMax.value = Math.round(value)
        } else {
            inputNumberMin.value = Math.round(value)
        }
    })

    inputNumberMin.addEventListener('change', function() {
        realtyFloorSlider.noUiSlider.set([this.value, null])
    })
    inputNumberMax.addEventListener('change', function() {
        realtyFloorSlider.noUiSlider.set([null, this.value])
    })
}


export {realtyFloorFilters}
