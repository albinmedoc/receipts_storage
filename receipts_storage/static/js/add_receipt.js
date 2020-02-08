function addProduct(){
    const template = document.querySelector(".product_container");

    var products_container = document.getElementById("products_container");

    const index = products_container.childElementCount + 1;

    var fieldset = template.cloneNode(true);

    fieldset.querySelector("legend").innerHTML = fieldset.querySelector("legend").innerHTML.replace(/[0-9]/g, index);

    fieldset.removeAttribute("id");

    products_container.appendChild(fieldset);

    fieldset.querySelectorAll("input").forEach(function(input){
        input.value = ""
    });

    fieldset.querySelectorAll("input:not(.tag_input)").forEach(function(input){
        input.setAttribute("name", input.getAttribute("name").replace(/[0-9]/g, index));
        input.setAttribute("id", input.getAttribute("id").replace(/[0-9]/g, index));
    });

    fieldset.querySelectorAll("label").forEach(function(label){
        label.setAttribute("for", label.getAttribute("for").replace(/[0-9]/g, index));
    });

    // Remove all tags
    fieldset.querySelectorAll(".tag").forEach(function(tag){
        tag.parentNode.removeChild(tag);
    });

    tag_input = new TagInput(fieldset.querySelector(".tag_container"));
}