function toTitleCase(str) {
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}
function display_courses(div_att, j_courses, j_nc){
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
        var test = "#" + j_courses[i].course_unique;
        but.setAttribute("data-target",test);
        but.innerHTML = toTitleCase(j_courses[i].course_name) + " - " +  j_courses[i].course_sec + " - " + j_courses[i].semester;
        but_text.appendChild(but);

        var db = document.createElement("div");
        db.id = j_courses[i].course_unique;
        db.className = "collapse";
        db.setAttribute("data-parent",div_att.id);
        div_att.appendChild(db);
        var dt = document.createElement("div");
        dt.className = "table-responsive";
        db.appendChild(dt);
        var tab = document.createElement("table");
        tab.className="table table-striped";
        dt.appendChild(tab);
        var thead = tab.createTHead();
        var hrow = thead.insertRow();
        var hc1 = document.createElement("th"); hrow.appendChild(hc1);
        var hc2 = document.createElement("th"); hrow.appendChild(hc2);
        var hc3 = document.createElement("th"); hrow.appendChild(hc3);
        var hc4 = document.createElement("th"); hrow.appendChild(hc4);
        var hc5 = document.createElement("th"); hrow.appendChild(hc5);
        var hc6 = document.createElement("th"); hrow.appendChild(hc6);
        var hc7 = document.createElement("th"); hrow.appendChild(hc7);
        hc1.innerHTML = "Sr .#";
        hc2.innerHTML = "Student Name";
        hc3.innerHTML = "Roll Number";
        hc4.innerHTML = "Semester";
        hc5.innerHTML = "Batch";
        hc6.innerHTML = "Course";
        hc7.innerHTML = "Course Section";
        var test = 0;
        for (z in j_nc[i]){
            var r = thead.insertRow();
            var c1 = r.insertCell();
            c1.innerHTML = +z+1;
            var c2 = r.insertCell();
            c2.innerHTML = toTitleCase(j_nc[i][z].student_name);
            var c3 = r.insertCell();
            c3.innerHTML = j_nc[i][z].roll_num;
            var c4 = r.insertCell();
            c4.innerHTML = j_nc[i][z].semester;
            var c5 = r.insertCell();
            c5.innerHTML = j_nc[i][z].batch;
            var c6 = r.insertCell();
            c6.innerHTML = j_nc[i][z].course_code;
            var c7 = r.insertCell();
            c7.innerHTML = j_nc[i][z].section;
            test = 1;
        }
        if(test == 0){
            var r = thead.insertRow();
            r.className = "table-danger";
            var c1 = r.insertCell();
            c1.setAttribute("colspan",7);
            c1.innerHTML = "No Registered Student";
        }


    }
    return ;
}