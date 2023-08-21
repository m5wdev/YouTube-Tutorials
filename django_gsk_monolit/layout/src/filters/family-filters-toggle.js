function familyFiltersToggle() {
    const top_selector = $('#section-family-types-filters__top')
    const class_opened = 'ftf-opened'

    const inner_selector = $('#section-family-types-filters__inner')
    const class_display = 'display-grid-family-filters'

    // hide #section-family-types-filters__inner when clicked outside #section-family-types-filters__top and #section-family-types-filters__inner
    $(document).mouseup((e) => {
        if (!top_selector.is(e.target) &&
            top_selector.has(e.target).length === 0 &&
            !inner_selector.is(e.target) &&
            inner_selector.has(e.target).length === 0 )
        {
            top_selector.removeClass(class_opened);
            inner_selector.removeClass(class_display);
        }
    })

    top_selector.on('click', () => {
        top_selector.toggleClass(class_opened)
        inner_selector.toggleClass(class_display)
    })
}

export {familyFiltersToggle}
