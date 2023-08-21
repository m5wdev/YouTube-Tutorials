function objectPageDocsPagination() {
    $('#page-docs-pagination a.page-link').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()
            let page_url = $(el).attr('href')
            // console.log(page_url)
            $.ajax({
                url: page_url,
                type: 'GET',
                success: (data) => {
                    $('#section-object-downloads').empty()
                    $('#section-object-downloads').append( $(data).find('#section-object-downloads').html() )
                }
            })
        })
    })
}


export {objectPageDocsPagination}
