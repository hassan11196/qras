function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}
function display_courses(div_att, j_courses){
    console.table(j_courses);
    for (i in j_courses){
        var d1 = document.createElement("div");
        d1.className = "card";
        div_att.appendChild(d1);
        var d2 = document.createElement("div");
        d2.className = "card-header";
        d1.appendChild(d2);
        var but_text = document.createElement("h2");
        but_text.className = "mb-0";
        d2.appendChild(but_text);
        var but = document.createElement("button");
        but.className = "btn btn-outline-info btn-lg btn-block";
        but.style = "white-space: normal !important;word-wrap: break-word !important;";
        but.type = "button";
        but.setAttribute("data-toggle","collapse");
        but.setAttribute("aria-expanded","false");
        var test = "#" + j_courses[i].course_code + j_courses[i].section + j_courses[i].semester;
        but.setAttribute("data-targer",test);
        but.innerHTML = toTitleCase(j_courses[i].course_name) + " - " +  j_courses[i].course_sec + " - " + j_courses[i].semester;
        but_text.appendChild(but);

        var db = document.createElement("div");
        db.id = j_courses[i].course_code + j_courses[i].section + j_courses[i].semester;
        db.className = "collapse";
        db.setAttribute("data-parent",div_att.id);
        div_att.appendChild(db);
        var dt = document.createElement("div");
        dt.className = "table-responsive";
        db.appendChild(dt);
        var tab = document.createElement("table");
        tab.className="table table-striped table-hover";
        dt.appendChild(tab);

    }
    return ;
}