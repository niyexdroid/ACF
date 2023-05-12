
// we are getting the url of the page
const url = window.location.href

// getting the form...
const searchForm = document.getElementById('search-form')

// and the input box...
const searchInput = document.getElementById('eventSearchBox')

// and not to forget the result box 
const resultsBox = document.getElementById('eventResultBox')

// and for some reason, also the csrf token
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

// this is the function that will take care of passing the input to the search_results method \
// in the views through the url.
// then it will receive whatever the function returns (which is a json response) and then changes \
// the html of the results box realtime!
// this is the basic overview of how this file performs a livesearch(well atleast to me:->)
const sendSearchData = function(input){
    $.ajax({
        type: 'POST',
        url: '/search_events/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'search_query': input
        },
        success: (res) => {
            // console.log(res)

            // if we log just res, we will be getting a data array of the objects returned from the function the url links to.
            // but i we use res.data, we will be able to access the data directly
            // console.log(res.data)

            const data = res.data
            // checking if there are results
            if(Array.isArray(data)){
                resultsBox.innerHTML = ''
                data.forEach(event=>{
                    resultsBox.innerHTML += `
                        <a href="/event-single/${event.pk}" class="text-decoration-none" >
                            <div class="row mt-2 mb-2">
                                <div class="col-3">
                                    <img src="${event.image}" class="search-event-image" >
                                </div>
                                <div class="col-9"> 
                                    <h5>${event.name}</h5>
                                    <p> <span class="icon-calendar"></span> ${event.date}</p>
                                </div>
                            </div>
                        </a>
                    `
                })                
            } else {
                if(searchInput.value.length > 0){
                    resultsBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultsBox.classList.add('not-visible')
                }

            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}

searchInput.addEventListener('keyup', inp=> {
    // console.log(inp.target.value);
    if(resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    };

    sendSearchData(inp.target.value)

})
