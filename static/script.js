$( document ).ready(function() {
  // searchform submit button handler
  $('#document-search-form').submit(function(event) {
    event.preventDefault();

    var action = $(this).attr("action");
    var documentId = $("[name=id]").val();

    var $title = $(".document-title");

    // remove existing visualization
    var $existingSvg = $("#vis").find("svg");
    if ($existingSvg.length > 0) { $existingSvg.remove(); }

    // create and add spinner
    var $spinner = $("<span />").addClass("glyphicon")
                                .addClass("glyphicon-refresh")
                                .addClass("glyphicon-refresh-animate");
    $title.empty()
          .text("Loading ")
          .addClass("spinner")
          .addClass("text-center")
          .append($spinner);

    // make ajax post and handle received data
    $.post(action, function(data) {
      // set new title
      var title = data.object[documentId].title;
      $title.empty()
            .removeClass("spinner")
            .removeClass("text-center")
            .text(title);

      // create and add subtitle to title
      var $subtitle = $('<small />').text(" [" + documentId + "]")
                                    .appendTo($title);

      // remove spinner
      $title.next("h1").remove();

      // new visualization
      visualizeStuff(data); // TODO: update existing instead of remove + add
    });
  });

  function visualizeStuff(json) {
    var width = 1140;
    var height = width * 2;
    var minRadius = 5;
    var maxRadius = 8 * minRadius;

    var publications = json.list;

    // helpers
    function stayInsideBoxWidth(x) { return Math.max(maxRadius, Math.min(width - maxRadius, x)); }
    function stayInsideBoxHeight(y) { return Math.max(maxRadius, Math.min(height - maxRadius, y)); }
    function getYearFromDateString(dateString) {
      var date = new Date(dateString);
      return date.getFullYear();
    }

    // get constrains
    var minYear = d3.min(publications, function(item) { return getYearFromDateString(item.date); });
    var maxYear = d3.max(publications, function(item) { return getYearFromDateString(item.date); });

    var minGlobalCitationCount = d3.min(publications, function(item) { return item.global_citation_count; });
    var maxGlobalCitationCount = d3.max(publications, function(item) { return item.global_citation_count; });

    // initialize force directed d3 layout
    var force = d3.layout.force()
                  .charge(-100)
                  .linkDistance(20)
                  .size([width, height]);

    // add nodes to layout
    // TODO: Figure out links and add them to force
    force.nodes(publications)
         .start();

    // add svg to dom
    var svg = d3.select("#vis")
                .append("svg")
                .attr("width", width)
                .attr("height", height);

    // helper to scale radius
    var scaleRadius = d3.scale.sqrt()
                              .domain([minGlobalCitationCount, maxGlobalCitationCount])
                              .range([minRadius, maxRadius]);

    // color helper
    var color = d3.scale.category20();

    // add nodes to svg
    var node = svg.selectAll(".node")
                  .data(publications)
                  .enter().append("circle")
                  .attr("class", "node")
                  .attr("r", function(d) { return scaleRadius(d.global_citation_count); })
                  .style("fill", function(d) { return color(getYearFromDateString(d.date)); })

    // add title to nodes
    node.append("title")
        .text(function(d) { return d.title + " | Citations: " + d.global_citation_count + " | date: " + d.date; });

    // scale foo
    var timeScale = d3.time.scale().domain([maxYear, minYear]).range([0, height]);

    // handle positioning of circles on svg
    force.on("tick", function() {
      node.attr("cx", function(d) { return d.x = stayInsideBoxWidth(d.x); })
          .attr("cy", function(d) {
            var yValue = timeScale(getYearFromDateString(d.date));
            return d.y = stayInsideBoxHeight(yValue);
          });
    });

  }
});
