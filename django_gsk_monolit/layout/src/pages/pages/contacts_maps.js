function contacts_maps() {
    // First map (on init)
    let contact_group_first_id = $('.contact-card').first().data('contact-group-id')

    $('.contact-card-map').each((index, map_el) => {
        let map_id = $(map_el).data('map-id')

        if ( contact_group_first_id == map_id ) {
            // $(map_el).css('display', 'block')
            $(map_el).css({'display': 'block', 'width': '100%', 'height': '100%'})
        } else {
            $(map_el).css('display', 'none')
        }
    })
    // END First map (on init)

    $('.contact-card').each((index, el) => {
        $(el).click((e) => {
            let contact_group_id = $(el).data('contact-group-id')

            $('.contact-card-map').each((index, map_el) => {
                let map_id = $(map_el).data('map-id')

                if ( contact_group_id == map_id ) {
                    $(map_el).css({'display': 'block', 'width': '100%', 'height': '100%'})
                } else {
                    $(map_el).css('display', 'none')
                }
            })
        })
    })
}


export {contacts_maps}
