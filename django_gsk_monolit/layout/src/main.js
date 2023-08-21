import "./main.scss"
import "./bootstrap/bootstrap"

import {stickyMainNav, mainNav} from "./menu/main-nav"

// Fiters
import {familyFiltersToggle} from "./filters/family-filters-toggle"
import {facetFiltersSites} from "./filters/facet-filters-sites"

// Scroll to Top
import {scrollToTop} from "./modules/scroll-to-top/scroll-to-top"

// Ajax
import csrf from "./ajax/csrf"
import {newsPageLoadMoreNews} from "./ajax/news-page-load-more-news"
import {objectPageGalleries} from "./ajax/object-page-galleries"
import {objectPageDocsPagination} from "./ajax/object-page-documents-pagination"
import {objectCardSitesInfo} from "./ajax/object-card"
import {objectPageSitesInfo, objectPageSitesTypesInfo, mainSliderObjectSitesInfo} from "./ajax/object-page-sites-info"
import {mortgageOfferMonthlyPayment} from "./ajax/mortgage-offer-monthly-payment-calculate"
import {searchBySiteId} from "./ajax/search-by-site-id"
import {companyTendersPagination, selectTenderCategory} from "./ajax/company-tenders-page-pagination"
import {site_list_infinate_scroll} from "./ajax/site_list-infinate-scroll"
import {favorites} from "./ajax/favorites"

import {contacts_maps} from "./pages/pages/contacts_maps"

// Fancybox https://fancyapps.com/fancybox/3/
import '@fancyapps/fancybox'


$(document).ready(function() {
    csrf()

    // Exclude scrollToTop from Object page
    if ( $('.object-page').length == 0 ) {
        scrollToTop()
    }

    // Favorites
    if ( $('.sites').length || $('.site-page').length || $('.favorites-page').length || $('.object-page').length || $('.sites-commercial').length || $('.site-commercial-object-page').length || $('.commercial-object-page').length ) {
        favorites()
    }

    // Main nav
    mainNav()
    stickyMainNav()

    // Search by site id
    searchBySiteId()

    // Homepage
    if ( $('.homepage').length ) {
        mainSliderObjectSitesInfo()
        facetFiltersSites()
    }

    if ( $('.object-page').length ) {
        objectPageSitesInfo()
        objectPageSitesTypesInfo()
        objectPageGalleries()
        objectPageDocsPagination()
    }

    if ( $('.commercial-object-page').length ) {
        objectPageSitesInfo()
    }

    if ( $('.news').length ) {
        newsPageLoadMoreNews()
    }

    if ( $('.sites').length ) {
        familyFiltersToggle()
        facetFiltersSites()
    }

    if ( $('.site-page').length ) {
        mortgageOfferMonthlyPayment()
    }

    // Get object-card sites info
    if ( $('.object-card').length ) {
        objectCardSitesInfo()
    }
    // END Get object-card sites info

    // Company Tenders page
    if ( $('.company-tenders').length ) {
        companyTendersPagination()
        selectTenderCategory()
    }
    // END Company Tenders page

    // Contacts
    if ( $('.contacts').length ) {
        contacts_maps()
    }
})


$(document).ajaxStop(function() {
    // Object Documents Ajax pagination
    if ( $('.object-page').length ) {
        objectPageDocsPagination()
    }
    // END Object Documents Ajax pagination

    // Company Tenders page
    if ( $('.company-tenders').length ) {
        companyTendersPagination()
        selectTenderCategory()
    }
    // END Company Tenders page

    // News page Load more news...
    if ( $('.news').length ) {
        newsPageLoadMoreNews()
    }
    // END News page Load more news...
})


$(window).scroll(function() {
    // Main nav
    stickyMainNav()

    if ( $('.sites').length || $('.sites-commercial').length ) {
        site_list_infinate_scroll()
    }
})
