(async() => {
    let response = await fetch(`${window.origin}/get-ggraph`, {
        method: "GET",
        credentials: "include",
        body: JSON.stringify("Get data"),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    let responseJSON = await response.json();
    console.log(responseJSON)
    var g = svg.append("g")
        .attr("class", "everything");

    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(responseJSON.links)
        .enter().append("line");

    var defaultRadius = 5;
    var node = g.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(responseJSON.nodes)
        .enter().append("circle")
        .attr("r", defaultRadius)
        .attr("fill", "orange")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.on('click', function(node) {
        console.log(node)
        console.log(this)
        // fetch(`${window.origin}/get-frame/` + node.id, {
        //     method: "GET",
        //     credentials: "include",
        //     cache: "no-cache",
        //     headers: new Headers({
        //         "content-type": "application/json"
        //     })
        // }).then(response => response.json()).then(data => console.log(data));
        // console.log(response)
    });

    link.on('click', function(link) {
        console.log(link)
    });

    node.append("data")
        .text(function(d) { return JSON.stringify(d); });

    node.append("title")
        .text(function(d) { return `Id: ${d.id}, Situation: ${d.situation}`; });

    link.append("title")
        .text(function(d) { return `Source: ${d.source}, Target: ${d.target}`; });

    simulation
        .nodes(responseJSON.nodes)
        .on("tick", ticked);

    simulation
        .force("link")
        .links(responseJSON.links);
    var zoom_handler = d3.zoom()
        .on("zoom", zoom_actions);

    zoom_handler(svg);

    function zoom_actions() {
        g.attr("transform", d3.event.transform)
    }

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

})();