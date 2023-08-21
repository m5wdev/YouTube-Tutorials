import {get_session_favorites} from "./favorites"


$.fn.isInViewport = function() {
    var elementTop = $(this).offset().top
    var elementBottom = elementTop + $(this).outerHeight()

    var viewportTop = $(window).scrollTop()
    var viewportBottom = viewportTop + $(window).height()

    return elementBottom > viewportTop && elementTop < viewportBottom
}


function getSites(page_number) {
    let page_url = $('#section-sites-list').data('page-url')

    // Check if url have any parameters in GET request to avoid stop infinate sroll working in case url have GET parameters 
    let page_params = ''
    let url = window.location.href
    if(url.includes('?')) {
        // console.log('Parameterised URL')
        page_params = '&page='
    } else {
        // console.log('No Parameters in URL')
        page_params = '?page='
    }

    $.ajax({
        // url: page_url + '?page=' + page_number.toString(),
        // url: page_url + '&page=' + page_number.toString(),
        url: page_url + page_params + page_number.toString(),
        type: 'GET',
        success: (data) => {
            $('#section-sites-list__infinate_scroll').append( $(data).find('#section-sites-list__infinate_scroll').html() )

            // Run to display favorite icons for objects already in session after ajax request to load more object sites
            get_session_favorites()
        }
    })
}


let current_pagination_number = parseInt($('#section-sites-list').data('current-pagination-number'), 10)
const max_pagination_number = parseInt($('#section-sites-list').data('max-pagination-number'), 10)

let working = false

function site_list_infinate_scroll() {
    // if #footer in viewport
    if ( $('#footer').isInViewport() ) {
        if ( current_pagination_number < max_pagination_number ) {
            if ( working == false ) {
                working = true

                current_pagination_number++
                getSites(current_pagination_number)

                // Timeout before call
                setTimeout(function(){
                    working = false
                }, 500)
            }
        }
    }
}


export {site_list_infinate_scroll}
