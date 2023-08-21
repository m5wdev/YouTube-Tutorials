import {singularPlural} from "../modules/singular-plural"


const favorites_url = '/favorites/'
const favorites_api_url = '/favorites/api/'

const add_to_favorites_url = '/favorites/add/'
const remove_from_favorites_url = '/favorites/remove/'

const added_to_favorites_class = 'added'


function add_to_favorites() {
    $(document).on('click', '.add-to-favorites', (e) => {
        e.preventDefault()

        const type = $(e.currentTarget).data('type')
        const id = $(e.currentTarget).data('id')

        // console.log(type)
        // console.log(id)

        // console.log(e)
        // console.log(e.currentTarget)
        // console.log(e.target)

        if ( !$(e.currentTarget).hasClass(added_to_favorites_class) ) {
            $.ajax({
                url: add_to_favorites_url,
                type: 'POST',
                dataType: 'json',
                data: {
                    type: type,
                    id: id,
                },
                success: (data) => {
                    $(e.currentTarget).addClass(added_to_favorites_class)
                    $(e.currentTarget).find('.icon-heart-contour-green').removeClass('icon-heart-contour-green').addClass('icon-heart-solid-green')
                    $(e.currentTarget).find('.add-to-favorites__label').html('В избранном')
                    get_session_favorites_statistics()
                }
            })
        } else {
            $.ajax({
                url: remove_from_favorites_url,
                type: 'POST',
                dataType: 'json',
                data: {
                    type: type,
                    id: id,
                },
                success: (data) => {
                    $(e.currentTarget).removeClass(added_to_favorites_class)
                    $(e.currentTarget).find('.icon-heart-solid-green').removeClass('icon-heart-solid-green').addClass('icon-heart-contour-green')
                    $(e.currentTarget).find('.add-to-favorites__label').html('В избранноe')
                    get_session_favorites_statistics()
                }
            })
        }
    })
}


function get_session_favorites() {
    get_session_favorites_statistics()

    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            for (let i = 0; i < json.length; i++) {
                $('.add-to-favorites').each((index, el) => {
                    const type = $(el).data('type')
                    const id = $(el).data('id')

                    // If in favorites
                    if ( json[i].type == type && json[i].id == id ) {
                        $(el).addClass(added_to_favorites_class)
                        $(el).find('.icon-heart-contour-green').removeClass('icon-heart-contour-green').addClass('icon-heart-solid-green')
                        $(el).find('.add-to-favorites__label').html('В избранном')

                        $('#favorites').addClass(added_to_favorites_class)
                        $('#favorites').find('icon-heart-solid-green').removeClass('icon-heart-contour-green').addClass('icon-heart-solid-white')
                    }
                })
            }
        }
    })
}


function get_session_favorites_statistics() {
    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            let sites_plural = '<strong>' + json.length + '</strong> ' + singularPlural(json.length, ['помещение', 'помещения', 'помещений'])

            $('#favorites .hb-aside-text').empty()
            $('#favorites .hb-aside-text').html('В избранном ' + sites_plural + ', <a href="' + favorites_url + '" target="_blank" title="Откроется в новой вкладке">перейти</a>')

            $('#favorites').addClass(added_to_favorites_class)
            $('#favorites .icon-heart-solid-green').removeClass('icon-heart-solid-green').addClass('icon-heart-solid-white')
        }
        if (json == null) {
            $('#favorites .hb-aside-text').empty()
            $('#favorites .hb-aside-text').html('В избранном пока пусто')

            $('#favorites').removeClass(added_to_favorites_class)
            $('#favorites .icon-heart-solid-white').removeClass('icon-heart-solid-white').addClass('icon-heart-solid-green')
        }
    })
}


function favorites() {
    add_to_favorites()
    get_session_favorites()
}


export {favorites, get_session_favorites}
