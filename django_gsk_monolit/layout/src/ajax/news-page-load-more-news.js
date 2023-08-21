function newsPageLoadMoreNews() {
    const load_more_news_btn = $('#load-more-news button[name="load-more-news-btn"]')
    const load_more_news = '#load-more-news'
    const section_news = '#section-news__inner'
    let next_page = $(load_more_news_btn, this).data('next-page')

    // Remove #load-more-news if no records in next page
    if (next_page === '') {
        $(load_more_news).remove()
    }

    load_more_news_btn.click((e) => {
        e.preventDefault()
        // console.log(next_page)

        $.ajax({
            url: next_page,
            type: 'GET',
            success: (data) => {
                // If records exist in next page, update #load-more-news
                if (next_page) {
                    $(load_more_news).empty()
                    $(load_more_news).append( $(data).find(load_more_news).html() )
                } else {
                    $(load_more_news).remove()
                }

                // Append news to #section-news__inner
                $(section_news).append( $(data).find(section_news).html() )

                // Remeve all .news-card__fixed but first
                $(section_news + ' .news-card').not( $(section_news + ' .news-card')[0] ).removeClass('news-card__fixed')
            }
        })
    })
}


export {newsPageLoadMoreNews}
