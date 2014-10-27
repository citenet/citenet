$( document ).ready(function() {
  // get DOM elements that don't change
  var $title = $(".document-title");
  var $logo = $("#logo");

  function enableLoadingState() {
    var $existingSvg = $("#vis").find("svg");

    // create and add spinner
    var $spinner = $("<span />").addClass("glyphicon")
                                .addClass("glyphicon-refresh")
                                .addClass("glyphicon-refresh-animate");
    $title.empty()
          .text("Loading ")
          .addClass("spinner")
          .addClass("text-center")
          .append($spinner);

    if ($existingSvg.length > 0) {
      $existingSvg.remove();
      $logo.show();
    }
  }

  function disableLoadingState(newTitle, documentId) {
    $title.empty()
          .removeClass("spinner")
          .removeClass("text-center")
          .text(newTitle);

    // create and add subtitle to title
    var $subtitle = $("<small />").text(" [" + documentId + "]")
                                  .appendTo($title);

    // remove spinner
    $title.next("h1").remove();

    // hide logo
    $logo.hide();
  }

  // cached json helper for dev
  $(".cached-json").click(function(event) {
    event.preventDefault();

    enableLoadingState();

    $.getJSON("/cached-papers.json", function(json) {
      var title = json.object["MED,19245337"].title;

      disableLoadingState(title, "MED,19245337");

      // new visualization
      visualizeStuff(json); // TODO: update existing instead of remove + add
    });
  });

  // searchform submit button handler
  $("#document-search-form").submit(function(event) {
    event.preventDefault();

    enableLoadingState();

    var action = $(this).attr("action");
    var documentId = $("[name=id]").val();

    // make ajax post and handle received data
    $.post(action, {"id": documentId}).done(function(json) {
      var title = json.object[documentId].title;

      disableLoadingState(title, documentId);

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

    var publicationsWithReferences = publications.filter(function(item) { return item.references.length > 0; });
    var links = [];
    publicationsWithReferences.forEach(function(item) {
      item.references.forEach(function(reference) {
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
                .attr("class", "d3-tip")
                .offset([-10, 0])
                .html(function(d) {
                  var htmlString = "<strong>" + d.title + "</strong>";
                  htmlString += "<br/>By: " + d.authors;
                  htmlString += "<br/>Published: " + d.date;
                  htmlString += "<br/><br/><strong>Number of global citations: " + d.global_citation_count + "</strong>";
                  htmlString += "<br/>Number of local citations: " + d.local_citation_count;
                  if (d.isOpenAccess) {
                    htmlString += "<br/><br/><strong class=\"green\">Open Access</strong>"
                  } else {
                    htmlString += "<br/><br/><strong class=\"red\">NOT Open Access</strong>"
                  }
                  return htmlString;
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
                  .on("mouseover", tip.show)
                  .on("mouseout", tip.hide);

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
