import sqlite3 as sql


class Bubble(object):

    def __init__(self):
        self.error = "{function}: The following error occured {error}\n"
        self.group_by = ""
        self.metric = ""
    ### This uses code from http://bl.ocks.org/mbostock/4063269
    def html_text(self):
        return """
        <!DOCTYPE html>
<meta charset="utf-8">

<h1>
    Bubble Map
</h1>
<h2>
    <b>Group by: </b>     {group_by} 
    <br>
    <b>Metric: </b> {metric}
</h2>
<style>
    h1{{
       text-align:center ;
    }}
    h2{{
        text-align: center;
    }}

    text {{
        font: 10px sans-serif;
    }}

</style>
<body>
<script src="d3.min.js"></script>
<script>

    var diameter = 1400,
            format = d3.format(",d"),
            color = d3.scale.category20c();

    var bubble = d3.layout.pack()
            .sort(null)
            .size([diameter, diameter])
            .padding(1.5);

    var svg = d3.select("body").append("svg")
            .attr("width", diameter)
            .attr("height", diameter)
            .attr("class", "bubble");

    d3.json("flare.json", function(error, root) {{
        if (error) throw error;

        var node = svg.selectAll(".node")
                .data(bubble.nodes(classes(root))
                        .filter(function(d) {{ return !d.children; }}))
                .enter().append("g")
                .attr("class", "node")
                .attr("transform", function(d) {{ return "translate(" + d.x + "," + d.y + ")"; }});

        node.append("title")
                .text(function(d) {{ return d.className + ": " + format(d.value); }});

        node.append("circle")
                .attr("r", function(d) {{ return d.r; }})
                .style("fill", function(d) {{ return color(d.packageName); }});

        node.append("text")
                .attr("dy", ".3em")
                .style("text-anchor", "middle")
                .text(function(d) {{ return d.className.substring(0, d.r / 3); }});
    }});

    // Returns a flattened hierarchy containing all leaf nodes under the root.
    function classes(root) {{
        var classes = [];

        function recurse(name, node) {{
            if (node.children) node.children.forEach(function(child) {{ recurse(node.name, child); }});
            else classes.push({{packageName: name, className: node.name, value: node.size}});
        }}

        recurse(null, root);
        return {{children: classes}};
    }}

    d3.select(self.frameElement).style("height", diameter + "px");

</script>"""

    def bubble_data(self):

        dicts = {

        "prompts" :{

        "type" : "1 for on_street ... 2 for route \n",
        "metric" : "1 for count ... 2 for avg_board ... 3 for avg_alight\n"

        },

        "type" : {1:"on_street", 2:"route"},

        "tables" : {1:"on_street_agg", 2: "route_agg"},

        }

        connection = sql.connect("bus_data.db")

        cursor = connection.cursor()

        input_type = int(raw_input(dicts["prompts"]["type"]))

        if input_type not in [1,2]:
            print self.error.format(function="get_data", error="Invalid input"); exit(1)

        input_metric = int(raw_input(dicts["prompts"]["metric"]))

        if input_metric not in [1,2,3]:
            print self.error.format(function="get_data", error="Invalid input"); exit(1)

        table = dicts["tables"][input_type]

        selected_type = dicts["type"][input_type]

        metric = {1: {1:"on_street_count", 2: "route_count"}[input_type], 2: "avg_board", 3:"avg_alight"}[input_metric]

        self.metric = metric


        self.group_by = selected_type

        print metric, self.metric

        print self.group_by, selected_type



        return cursor.execute("SELECT {selected_type},{metric} FROM {table} ORDER BY {metric}".format(
            selected_type=selected_type,
            metric=metric,
            table=table))

    def create_bubble(self):

        data = self.bubble_data()

        bubble_format  = """{{ 
        "name": "{name}",
        "children" : [{{
        "name" : "{name}", "size" : {metric}
        }}]
        }}"""

        body = "[" + ",".join([bubble_format.format(name=x[0], metric=x[1]) for x in data]) + "]"

        map_points = """ 
                    {{ 
                    "name": "body",
                    "children": {body}
                    }}""".format(body=body)

        with open("d3/bubble.html","w") as out:
            out.write(self.html_text().format(group_by=self.group_by,metric=self.metric))
        with open("d3/flare.json", "w") as out:
            out.write(map_points)
        
        print """
        The bubble map has been succesfully created.\n
        If you have trouble opening index.html, try using a different browser\n
        """