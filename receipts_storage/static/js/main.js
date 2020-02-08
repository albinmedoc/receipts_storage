if(document.getElementById("nav_btn") &&  document.getElementById("navigation")){
    document.getElementById("nav_btn").addEventListener("click", function(e){
        var btn = document.getElementById("nav_btn");
        var nav = document.getElementById("navigation");
        if(btn.classList.contains("is-active")){
            btn.classList.remove("is-active");
            nav.classList.remove("is-active")
        }else{
            btn.classList.add("is-active");
            nav.classList.add("is-active");
        }
    });
}

var getJSON = function (method, url, callback, params) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.responseType = "json";
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
        var status = xhr.status;
        callback(status, xhr.response);
    };
    if (params == undefined) {
        params = "";
    }
    xhr.send(params);
};