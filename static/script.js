$( document ).ready(function() {
  // searchform submit button handler
  $('#document-search-form').submit(function(event) {
    event.preventDefault();

    var action = $(this).attr("action");
    var documentId = $("[name=id]").val();
    console.log('documentId', documentId);

    $.post(action, function(data) {
      $(".document-title").text(documentId);
      visualizeStuff(data);
    });
  });


  function visualizeStuff(json) {
    // visualization
    var width = 1140;
    var height = 1200;
    var minRadius = 3;
    var maxRadius = 7;

    // helpers
    function stayInsideBoxWidth(x) { return Math.max((2 * maxRadius), Math.min(width - (2 * maxRadius), x)); }
    function stayInsideBoxHeight(y) { return Math.max((2 * maxRadius), Math.min(height - (2 * maxRadius), y)); }

    var color = d3.scale.category20();

    var force = d3.layout.force()
                  .charge(-100)
                  .linkDistance(20)
                  .size([width, height]);

    var svg = d3.select("#vis")
                .append("svg")
                .attr("width", width)
                .attr("height", height);

    // TODO: Get current Max and Min year
    var earliestYear = 1971;
    var latestYear = 2014;

    var color = d3.scale.category20();

    var publications = json.list;

    // TODO: Get current Max and Min global_citation_count
    var minCitationCount = 0;
    var maxCitationCount = 100;

    var scale = d3.scale.sqrt()
                        .domain([minCitationCount, maxCitationCount])
                        .range([minRadius, maxRadius]);

    // TODO: Figure out links and add them to force
    force.nodes(publications)
         .start();

    var node = svg.selectAll(".node")
                  .data(publications)
                  .enter().append("circle")
                  .attr("class", "node")
                  .attr("r", function(d) { return scale(d.global_citation_count) })
                  .style("fill", function(d) {
                    var tempDate = new Date(d.date);
                    return color(tempDate.getFullYear());
                  })
                  .call(force.drag);

    node.append("title")
        .text(function(d) { return d.title + " | Citations: " + d.global_citation_count + " | date: " + d.date; });

    var y = d3.time.scale().domain([latestYear, earliestYear]).range([0, height]);

    force.on("tick", function() {
      node.attr("cx", function(d) { return d.x = stayInsideBoxWidth(d.x); })
          .attr("cy", function(d) {
            var tempDate = new Date(d.date);
            var yValue = y(tempDate.getFullYear());
            return d.y = stayInsideBoxHeight(yValue);
          });
    });

  }
});
