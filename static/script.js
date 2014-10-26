$( document ).ready(function() {

  // cached json helper for dev
  $('.cached-json').click(function(event) {
    event.preventDefault();

    var action = $(this).attr("action");
    var documentId = $("[name=id]").val();

    var $title = $(".document-title");

    // remove existing visualization
    var $existingSvg = $("#vis").find("svg");
    if ($existingSvg.length > 0) { $existingSvg.remove(); }

    $.getJSON('/cached-papers.json', function(json) {
      // set new title
      var title = json.object["MED,19245337"].title;
      $title.empty()
            .removeClass("spinner")
            .removeClass("text-center")
            .text(title);

      // create and add subtitle to title
      var $subtitle = $('<small />').text(" [" + "MED,19245337" + "]")
                                    .appendTo($title);

      // remove spinner
      $title.next("h1").remove();

      // new visualization
      visualizeStuff(json); // TODO: update existing instead of remove + add
    });
  });

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
    $.post(action, {"id": documentId}).done(function(json) {
      // set new title
      var title = json.object[documentId].title;
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
      visualizeStuff(json); // TODO: update existing instead of remove + add
    });
  });

  function visualizeStuff(json) {
    var width = 1140;
    var height = width * 2;
    var minRadius = 5;
    var maxRadius = 8 * minRadius;

    var publications = json.list;

    // helper to get only year
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
                  .charge(-150)
                  .distance(100)
                  .linkDistance(200)
                  .size([width, height]);

    // TODO: Figure out links and add them to force
    var publicationsWithReferences = publications.filter(function(item) { return item.references.length > 0; });
    var links = [];
    publicationsWithReferences.forEach(function(item) {
      // TODO: Generate links
      item.references.forEach(function(reference) {
        // reference == "MED,19245337"
        var sourceNode = publications.filter(function(source) { return source.api_id === item.api_id })[0];
        var targetNode = publications.filter(function(target) { return target.api_id === reference })[0];

        if (targetNode) {
          links.push({ source: sourceNode,
                       target: targetNode });
        }
      });
    });

    // initialize d3-tip
    var tip = d3.tip()
                .attr('class', 'd3-tip')
                .offset([-10, 0])
                .html(function(d) {
                  return "<strong>" + d.title + "</strong><br/>By: " + d.authors + "<br/>Published: " + d.date;
                });

    // add nodes to layout
    force.nodes(publications)
         .links(links)
         .start();

    // add svg to dom
    var svg = d3.select("#vis")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .call(tip);

    // helper to scale radius
    var scaleRadius = d3.scale.sqrt()
                              .domain([minGlobalCitationCount, maxGlobalCitationCount])
                              .range([minRadius, maxRadius]);

    // color helper
    var color = d3.scale.category20();

    // add links to svg
    var link = svg.selectAll(".link")
                  .data(links)
                  .enter().append("line")
                  .attr("class", "link");

    // add nodes to svg
    var node = svg.selectAll(".node")
                  .data(publications)
                  .enter().append("circle")
                  .attr("class", "node")
                  .attr("r", function(d) { return scaleRadius(d.global_citation_count); })
                  .style("fill", function(d) { return color(getYearFromDateString(d.date)); })
                  .on('mouseover', tip.show)
                  .on('mouseout', tip.hide);

    // TODO: Remove
    // add title to nodes
    // node.append("title")
    //     .text(function(d) { return d.title + " | Citations: " + d.global_citation_count + " | date: " + d.date; });

    // scale foo
    var timeScale = d3.time.scale().domain([maxYear, minYear]).range([maxRadius, height - maxRadius]);

    // handle positioning of circles on svg
    force.on("tick", function() {
      node.attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y = timeScale(getYearFromDateString(d.date)); });

      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
    });

  }
});
