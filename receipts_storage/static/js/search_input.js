class SearchInput{
    constructor(search_container) {
        this.search_container = search_container;
        this.input = search_container.querySelector("input");

        this.timeout = null;

        var search_input = this;
        this.input.addEventListener("keyup", function(){
            if(search_input.timeout){
                clearTimeout(search_input.timeout);
                search_input.timeout = null;
            }else{
                search_input.timeout = setTimeout(function(){search_input.make_search();}, 500);
            }
        });
    }

    make_search(){
        var query = this.input.value;
        getJSON("POST", )
    }

    show_results(){

    }
}

var search_input = new SearchInput(document.getElementById("search_container"));