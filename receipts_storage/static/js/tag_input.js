class TagInput{
    constructor(tag_container) {
        this.tags = [];
        this.tag_container = tag_container;
        this.input = tag_container.querySelector("input.tag_input");
        this.output = tag_container.querySelector("input:not(.tag_input)");
        var tag_input = this;
        this.input.addEventListener("keyup", function(e){
            if(e.key === " "){
                tag_input.tags.push(tag_input.input.value.slice(0, -1));
                tag_input.addTags();
                tag_input.input.value = "";
            }
        });

        //Load old tags
        try{
            JSON.parse(this.output.value).forEach(function(tag){
                if(tags != ""){
                    tag_input.tags.push(tag);
                    tag_input.addTags();
                }
            });
        }catch(e){}
    }

    createTag(label){
        const div = document.createElement("div");
        div.classList.add("tag");
        const span = document.createElement("span");
        span.innerHTML = label;
        const close = document.createElement("i");
        close.classList.add("material-icons");
        close.innerHTML = "close";
        var tag_input = this;
        close.addEventListener("click", function(e){
            const value = e.target.parentElement.querySelector("span").innerHTML;
            const index = tag_input.tags.indexOf(value);
            if(index > -1){
                tag_input.tags.splice(index, 1);
            }
            tag_input.addTags();
        });

        div.appendChild(span);
        div.appendChild(close);
        return div;
    }

    reset(){
        this.tag_container.querySelectorAll(".tag").forEach(function(tag){
            tag.parentElement.removeChild(tag);
        });
        this.output.value = "";
    }

    addTags(){
        this.reset();
        var tag_input = this;
        this.tags.slice().reverse().forEach(function(tag){
            const input = tag_input.createTag(tag);
            tag_input.tag_container.prepend(input);
        });
        this.output.value = JSON.stringify(this.tags);
    }
}

var tag_inputs = document.querySelectorAll(".tag_container");
tag_inputs.forEach(function(tag_input){
    var input = new TagInput(tag_input);
});