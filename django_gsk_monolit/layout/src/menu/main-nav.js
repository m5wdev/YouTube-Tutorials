function stickyMainNav() {
    let pxFromTop = $(document).scrollTop()
    const mainNav = $("#header__bottom")
    const stickyClass = 'sticky-main-nav'

    // 40px from top
    if (pxFromTop >= 40) {
        mainNav.addClass(stickyClass)
    } else {
        mainNav.removeClass(stickyClass)
    }
}


function mainNav() {
    // Toggle main-nav
    const mainNav = $('#main-navigation')
    const menuToggle = $('#main-navigation-toggle')

    const opened_class = 'opened'
    const body_overflow_class = 'body-overflow-hidden'

    menuToggle.click(() => {
        if (mainNav.hasClass(opened_class)) {
            $('body').removeClass(body_overflow_class)
            $(this).removeClass(opened_class)
            mainNav.removeClass(opened_class)
            menuToggle.removeClass(opened_class)
        } else {
            $('body').addClass(body_overflow_class) // prevent background scroll
            $(this).addClass(opened_class)
            mainNav.addClass(opened_class)
            menuToggle.addClass(opened_class)
        }
    })

    // Submenu behavior
    $('.has-dropdown').each((index, el) => {
        // wrap .main-nav__link
        $(el).find('.main-nav__link').wrap(() => {
            return '<div class="main-nav__link-wrap">' + $(this).text() + '</div>'
        })

        // Append open-sub-nav to wrapper
        $(el).find('.main-nav__link-wrap').append('<span class="open-sub-nav"></span>')

        $(el).find('.open-sub-nav').click(() => {
            if ( $(el).find('.dropdown').hasClass('opened') ) {
                $(el).find('.dropdown').removeClass('opened')
                $(el).find('.open-sub-nav').removeClass('opened')
            } else {
                // Close other opened
                $('#main-navigation').find('.dropdown').removeClass('opened')
                $('#main-navigation').find('.open-sub-nav').removeClass('opened')

                $(el).find('.dropdown').addClass('opened')
                $(el).find('.open-sub-nav').addClass('opened')
            }
        })

        // Make opened to active
        if ( $(el).hasClass('active') ) {
            $(el).find('.dropdown').addClass('opened')
            $(el).find('.open-sub-nav').addClass('opened')
        }
    })
}


export {stickyMainNav, mainNav}
