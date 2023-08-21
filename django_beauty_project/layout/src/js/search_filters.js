const api_cities_url = "/api/cities/";
const api_services_url = "/api/services/";

document.getElementById('search-tile-input__date').valueAsDate = new Date();

// const searchInputPlaces = document.getElementsByClassName('search-tile-input__place');
const searchInputPlaces = document.getElementById('search-tile-input__place');
// const searchInputServices = document.getElementsByClassName('search-tile-input__services');
const searchInputServices = document.getElementById('search-tile-input__services');


function fetchCitiesData() {
    return fetch(api_cities_url)
                .then(response => response.json());
}

function fetchServicesData() {
    return fetch(api_services_url)
                .then(response => response.json());
}


fetchCitiesData().then(response => {
    for (let i = 0; i < response.length; i++) {
        let search_option = document.createElement("option");
        search_option.value = response[i].id;
        search_option.text = response[i].name;
        searchInputPlaces.add(search_option);
        // searchInputPlaces[i].add(search_option);
    }
});

fetchServicesData().then(response => {
    for (let i = 0; i < response.length; i++) {
        // Menu #search-form__services-nav
        let menu_link = document.createElement("a");
        menu_link.href = '';
        menu_link.text = response[i]['name'];
        menu_link.setAttribute('data-list-id', i);
        menu_link.setAttribute('data-service-id', response[i]['id']);
        document.getElementById('search-form__services-nav').appendChild(menu_link);

        for (let k = 0; k < response[i]['services'].length; k++) {
            let search_option = document.createElement("option");
            search_option.value = response[i]['services'][k].id;
            search_option.text = response[i]['services'][k].name;
            searchInputServices.add(search_option);
            // searchInputServices[i].add(search_option);
        }
    }

    const searchMenuLinks = document.querySelectorAll('#search-form__services-nav a');
    for (let i = 0; i < searchMenuLinks.length; i++) {
        // console.log(searchMenuLinks[i]);
        searchMenuLinks[i].onclick = testFunction;
    }
});


function testFunction(e) {
    e.preventDefault();

    const searchMenuLinks = document.querySelectorAll('#search-form__services-nav a');
    const data_list_id = e.target.attributes.getNamedItem('data-list-id').value;
    const data_service_id = e.target.attributes.getNamedItem('data-service-id').value;

    // Remove class="active"
    for (let i = 0; i < searchMenuLinks.length; i++) {
        searchMenuLinks[i].classList = '';
    }

    e.currentTarget.classList.add("active");

    // console.log(e.target);
    // console.log(data_service_id);

    fetchServicesData().then(response => {
        document.getElementById("search-tile-input__services").innerHTML = '';

        const services_list = response[data_list_id]['services'];

        if (services_list.length > 0) {
            for (let i = 0; i < services_list.length; i++) {
                let search_option = document.createElement("option");
                search_option.value = services_list[i].id;
                search_option.text = services_list[i].name;
                searchInputServices.add(search_option);
            }
        }
    });
}


// Clone .st-4 .st-5
const st_5 = document.getElementsByClassName('st-5');

// document.getElementsByClassName('st-5')[0].onclick = duplicate_st_4_and_st_5;
st_5[0].onclick = duplicate_st_4_and_st_5;

const original_1 = document.getElementsByClassName('st-4')[0];
const original_2 = document.getElementsByClassName('st-5')[0];

function duplicate_st_4_and_st_5() {
    const clone_1 = original_1.cloneNode(true);
    const clone_2 = original_2.cloneNode(true);

    original_1.parentNode.appendChild(clone_1);
    original_2.parentNode.appendChild(clone_2);

    // for (let i = 0; i < st_5.length; i++) {
    //     console.clear();
    //     console.log(st_5[i]);
    //     st_5[i].click = duplicate_st_4_and_st_5;
    // }
}