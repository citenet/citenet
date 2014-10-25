$( document ).ready(function() {
  // searchform submit button handler
  $('#document-search-form').submit(function(event) {
    event.preventDefault();

    var action = $(this).attr("action");
    var documentId = $("[name=id]").val();

    var $title = $(".document-title");

    var $spinner = $("<span />").addClass("glyphicon")
                                .addClass("glyphicon-refresh")
                                .addClass("glyphicon-refresh-animate");

    var $wrappedSpinner = $("<h1 />").addClass("text-center")
                                     .append($spinner);

    $wrappedSpinner.insertAfter($title);

    $.post(action, function(data) {
      $title.text(documentId);
      $title.next("h1").remove();

      var $existingSvg = $("#vis").find("svg");
      if ($existingSvg.length > 0) { $existingSvg.remove(); }

      visualizeStuff(data);
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

    var color = d3.scale.category20();

    var force = d3.layout.force()
                  .charge(-100)
                  .linkDistance(20)
                  .size([width, height]);

    var svg = d3.select("#vis")
                .append("svg")
                .attr("width", width)
                .attr("height", height);

    var earliestYear = d3.min(publications, function(item) { return getYearFromDateString(item.date); });
    var latestYear = d3.max(publications, function(item) { return getYearFromDateString(item.date); });

    var color = d3.scale.category20();

    var minGlobalCitationCount = d3.min(publications, function(item) { return item.global_citation_count; });
    var maxGlobalCitationCount = d3.max(publications, function(item) { return item.global_citation_count; });

    var scale = d3.scale.sqrt()
                        .domain([minGlobalCitationCount, maxGlobalCitationCount])
                        .range([minRadius, maxRadius]);

    // TODO: Figure out links and add them to force
    force.nodes(publications)
         .start();

    var node = svg.selectAll(".node")
                  .data(publications)
                  .enter().append("circle")
                  .attr("class", "node")
                  .attr("r", function(d) { return scale(d.global_citation_count); })
                  .style("fill", function(d) { return color(getYearFromDateString(d.date)); })

    node.append("title")
        .text(function(d) { return d.title + " | Citations: " + d.global_citation_count + " | date: " + d.date; });

    var timeScale = d3.time.scale().domain([latestYear, earliestYear]).range([0, height]);

    force.on("tick", function() {
      node.attr("cx", function(d) { return d.x = stayInsideBoxWidth(d.x); })
          .attr("cy", function(d) {
            var yValue = timeScale(getYearFromDateString(d.date));
            return d.y = stayInsideBoxHeight(yValue);
          });
    });

  }
});
