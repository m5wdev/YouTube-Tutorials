function objectPageGalleries() {
    const gallery_images_display_div = $('#bp-and-news-pills-building-progress__inner')

    $('select[name=object_gallery_id]').change(() => {
        let selected_val_url = $('option:selected', this).val()
        let selected_text    = $('option:selected', this).html()

        $.getJSON(selected_val_url, (data) => {
            gallery_images_display_div.empty()

            $.each(data, (i, val) => {
                let path_to_img = '/media/'+val.image
                let link_layout = '<a data-fancybox="bp-gallery" data-caption="'+selected_text+'" class="bp-card" href="'+path_to_img+'" style="background-image: url('+path_to_img+');"><div class="bp-card__date">'+selected_text+'</div></a>'

                // Append images tp gallery_images_display_div
                gallery_images_display_div.append(link_layout)
            })
        })
    })
}


export {objectPageGalleries}
