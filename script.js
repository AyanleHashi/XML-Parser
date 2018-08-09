$(document).ready(function() {
    //First, set the cookies if they don't already exist
    var COOKIES = {};
    var elements_per_page = 25;

    //$(".pagination").append("<li><a href=\"#\">1</a></li>");
    for (var i=1;i<($(".paper").length / elements_per_page)+1;i++) {
        $(".pagination").append("<li><a href=\"#" + String(i) + "\">" + String(i) + "</a></li>");
    }

    $(".container").find(".paper").hide();
    for (var i=1;i<elements_per_page+1;i++) {
        $("#" + String(i)).show();
    }

    $("a[href=\"#1\"]").parent().addClass("active");

    if (Cookies.get("COOKIES") == undefined) {
        COOKIES["Labels"] = [];
        Cookies.set("COOKIES",COOKIES,{expires:7});
    }
    else {
        //Otherwise, load the labels from stored cookies
        COOKIES = Cookies.getJSON("COOKIES");
    }

    //Set the labels that were stored in the cookies
    Object.keys(COOKIES).forEach(function(element) {
        COOKIES[element].forEach(function(label) {
            $("#"+element).append("<div class=\"draggable-after\">" + label + "</div>");
        });
    });

    Object.keys(COOKIES["Labels"]).forEach(function(element){
        $("#sidebar").append("<div class=\"draggable\" title=\"Drag me\">" + COOKIES["Labels"][element] + "</div><br>");
        //$("#header").append("<div class=\"draggable\" title=\"Drag me\">" + COOKIES["Labels"][element] + "</div><br>");
    });

    Cookies.set("COOKIES",COOKIES);

    $(".draggable").draggable({
        revert: true,
        revertDuration: 0
    });

    $(".droppable").droppable({
        activeClass: "active",
        drop: function (event, ui) {
            //If the label isn't already on the publication, add it
            var id = $(this).attr("id");

            if (!COOKIES.hasOwnProperty(id)) {
                COOKIES[id] = [];
            }

            if (!COOKIES[id].includes(ui.draggable.text())) {
                $(this).append("<div class=\"draggable-after\" title=\"Click to remove\">" + ui.draggable.text() + "</div>");

                //Set the cookie so it remembers the labels on different sessions
                    if (!COOKIES[id].includes(ui.draggable.text())) {
                        COOKIES[id].push(ui.draggable.text());
                    }

                Cookies.set("COOKIES",COOKIES);
            }
        }
    });

    //Remove the label and cookie on click
  	$(".paper").on("click",".draggable-after",function() {
		COOKIES[$(this).parent().attr("id")].splice(COOKIES[$(this).parent().attr("id")].indexOf($(this).text()),1);
	    $(this).remove();

	    Cookies.set("COOKIES",COOKIES);
	});

    //Temporarily hide any papers that don't contain the text entered in the search bar
    $("#searchbar").on("keyup", function() {
        $(".container").find("li").removeClass("active");
        var value = $(this).val().toLowerCase();
        $(".container .paper").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
        if (value == "") {
            window.location.href = "";
        }
    });

    $("#labelSubmit").on("click",function() {
        if ($("#labelInput").val().length > 1) {
            if (!COOKIES["Labels"].includes($("#labelInput").val())) {
                COOKIES["Labels"].push($("#labelInput").val());
            }
        }
        else {
            alert("Label length must be 2 or more");
        }
        Cookies.set("COOKIES",COOKIES);
    });

    var $divs = $("div.paper");

    $('#titleSort').on('click', function () {
        var titleOrderedDivs = $divs.sort(function (a, b) {
            return $(a).find("h4").text() > $(b).find("h4").text();
        });
        $(".container").html(titleOrderedDivs);
    });

    $('#authorSort').on('click', function () {
        var authorOrderedDivs = $divs.sort(function (a, b) {
            return $(a).find("author").text() > $(b).find("author").text();
        });
        $(".container").html(authorOrderedDivs);
    });

    $("li").each(function(index) {
        var that = this;
        $(that).on("click",function() {
            $(that).parent().find("li").removeClass("active");
            $(that).addClass("active");
            $("a[href="+$(that).text()+"]").addClass("active");
            $(".container").find(".paper").hide();
            $(".paper").each(function(index2) {
                if ((parseInt($(that).text()) - 1) * elements_per_page < parseInt($(this).attr("id")) && parseInt($(this).attr("id")) <= parseInt($(that).text()) * elements_per_page) {
                    $(this).show();
                    console.log($(this).attr("id"));
                }
            });
        });
    });
});
