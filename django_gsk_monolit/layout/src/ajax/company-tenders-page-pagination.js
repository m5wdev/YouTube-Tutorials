function selectTenderCategory() {
    $('select[name="tender_category"]').change((e) => {
        e.preventDefault()

        $('select[name="tender_category"] option:selected').each((index, el) => {
            const page_url = $(el).data('page_url')

            $.ajax({
                url: page_url,
                type: 'GET',
                success: (data) => {
                    $('#vacancies-list-accordion').empty()
                    $('#vacancies-list-accordion').append( $(data).find('#vacancies-list-accordion').html() )
                }
            })
        })
    })
}

function companyTendersPagination() {
    $('#tenders-pagination a.page-link').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()
            const page_url = $(el).attr('href')

            $.ajax({
                url: page_url,
                type: 'GET',
                success: (data) => {
                    $('#vacancies-list-accordion').empty()
                    $('#vacancies-list-accordion').append( $(data).find('#vacancies-list-accordion').html() )
                }
            })
        })
    })
}


export {companyTendersPagination, selectTenderCategory}
