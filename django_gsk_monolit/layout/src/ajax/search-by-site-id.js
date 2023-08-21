function preventPressEnter() {
    $(window).keydown((event) => {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    })
}


function searchBySiteId() {
    const search_id = $('#search-by-site-id')
    const search_results_id = $('#search-by-site-id__results')
    const sites_base_url = search_results_id.data('site-base-url')
    const all_sites_api = search_id.data('api-all-sites')

    preventPressEnter()

    $('#search-by-site-id').keyup((event) => {
        search_results_id.empty()

        let search_val = search_id.val()
        let expression = new RegExp("^" + search_val, "i")

        // console.log(search_val)

        $.getJSON(all_sites_api, (data) => {
            $.each(data, (index, el) => {
                if (search_val.length >= 2) {
                    if (el.crm_id.search(expression) != -1) {
                        // search_results_id.append('<div class="sbid-res-item"><a href="' + sites_base_url + el['id'] + '">' + el['crm_id'] + '</a></div>')
                        search_results_id.append('<div class="sbid-res-item"><a href="' + sites_base_url + el['id'] + '">' +
                            // highlite matching text
                            el['crm_id'].replace(expression, (str) => { return '<strong>' + str + '</strong>' }) +
                            '</a></div>')
                    }
                }
            })
        })
    })

    // If clicked outside #hb-aside
    window.addEventListener('click', function(e) {
        if (document.getElementById('hb-aside').contains(e.target)) {
            // Clicked inside box
        } else {
            // Clicked outside the box
            search_results_id.empty()
            search_id.val('')
        }
    })
}


export {searchBySiteId}
