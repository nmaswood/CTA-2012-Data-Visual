import sqlite3 as sql
from googlemaps import Client
from sys import exit

# This file uses code from
#http://stackoverflow.com/questions/22342097/is-it-possible-to-create-a-google-map-from-python


### USAGE ###

#map = Map()
#map.create_map("basic")
##map.create_verbose("visual")


#Bubble = Bubble()
#Bubble.create_bubble()



class Map(object):

    def __init__(self,db_name='bus_data.db'):

        self.db_name = db_name

        self.html_body = self.html_body()

        self.html_dom = self.html_dom()

        self.group_by = ""

        self.error = "{function}: The following error occured {error}\n"


    def html_body(self):
        return {

        "basic_visual": """
        <!DOCTYPE html>
        <html>
            <head>
            <meta charset="utf-8">
            <title>Heatmaps</title>
                {style}
            </head>
            <body>
            <div id="floating-panel">

    <b>Heat Map</b>
    <br>
    Areas that are redder represent areas
    with larger amounts of bus stops.

</div>
            <div id="map"></div>
            <script>
            
            var map, heatmap;

            function initMap() {{
                map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 12,
                center: {{lat: {center_lat}, lng: {center_lon}}},
                mapTypeId: google.maps.MapTypeId.SATELLITE
            }});

            heatmap = new google.maps.visualization.HeatmapLayer({{
                data: getPoints(),
                map: map
            }});
        }}

        function toggleHeatmap() {{
            heatmap.setMap(heatmap.getMap() ? null : map);
        }}

        function changeGradient() {{
            var gradient = [
                'rgba(0, 255, 255, 0)',
                'rgba(0, 255, 255, 1)',
                'rgba(0, 191, 255, 1)',
                'rgba(0, 127, 255, 1)',
                'rgba(0, 63, 255, 1)',
                'rgba(0, 0, 255, 1)',
                'rgba(0, 0, 223, 1)',
                'rgba(0, 0, 191, 1)',
                'rgba(0, 0, 159, 1)',
                'rgba(0, 0, 127, 1)',
                'rgba(63, 0, 91, 1)',
                'rgba(127, 0, 63, 1)',
                'rgba(191, 0, 31, 1)',
                'rgba(255, 0, 0, 1)'
            ]
            heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
        }}

        function changeRadius() {{
            heatmap.set('radius', heatmap.get('radius') ? null : 20);
        }}

        function changeOpacity() {{
            heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
        }}

        // Heatmap data: 500 Points
        function getPoints() {{
            return {map_points};
        }}

            </script>
                <script async defer
                        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDTFj3XyhkCRZ5n6qPE23iwre3qFQgn3NI&signed_in=true&libraries=visualization&callback=initMap">
                </script>
            </body>
        </html>
        """,

        "verbose_visual": """
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                <meta charset="utf-8">
                <title>Verbose Map</title>
                {style}
            </head>
            <body>
            <div id="floating-panel">

                    <b>Marker Map</b>
                    <br>
                    <b>Grouped by</b> : {group_by}
                    <b>Metric</b> : {metric_name}
                    <br>
                    Markers that are darker have higher values. Click on a marker to see its
                    corresponding statistics.

                </div>
                <div id="map"></div>
                    <script>

                        function initMap() {{
                        var map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 13,
                        center: {{lat: {center_lat}, lng: {center_lon}}}
                        }});
                        {colors}
                        {map_points}
                        }}
                    </script>
                    <script async defer
                        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDTFj3XyhkCRZ5n6qPE23iwre3qFQgn3NI&signed_in=true&callback=initMap"></script>
            </body>
            </html>
            """}

    def html_dom(self):
        return {
        "basic_visual_dom": "new google.maps.LatLng({lat}, {lon})",

        "verbose_visual_colors"  : """

                var pinImage{idx} = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + "{color}",
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(5, 5));

                """,

        "verbose_visual_dom" : """

            var marker{idx} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            icon : pinImage{color_num},
            title: 'name (Chicago)'
            }});

            marker{idx}.addListener('click', function () {{
            new google.maps.InfoWindow({{content: '<div id="content">'
            + 'name: ' + '{name}' +
            ' count: ' + '{count}' +
            ' average alight: ' + '{avg_alight}' +
            ' average board:' + '{avg_board}' +'</div>'}}).open(map, marker{idx});}});

            """,
        "style" : """
        <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        #map {
            height: 100%;
        }
        #floating-panel {
            position: absolute;
            top: 10px;
            left: 25%;
            z-index: 5;
            background-color: #fff;
            padding: 5px;
            border: 1px solid #999;
            text-align: center;
            font-family: 'Roboto','sans-serif';
            line-height: 30px;
            padding-left: 10px;
        }

        #floating-panel {
            background-color: #fff;
            border: 1px solid #999;
            left: 25%;
            padding: 5px;
            position: absolute;
            top: 10px;
            z-index: 5;
            font-family: 'Roboto', 'sans-serif';
        }
    </style>"""
        }
   
    def basic_visual(self):

        connection = sql.connect(self.db_name)

        cursor = connection.cursor()

        points = cursor.execute("""SELECT latitude, longitude FROM CTA1012""")

        points = [pair for pair in points.fetchall()]

        center_lat = sum(( x[0] for x in points )) / len(points)
        center_lon = sum(( x[1] for x in points )) / len(points)

        map_points = "[" + ",".join(
            [self.html_dom["basic_visual_dom"]
            .format(
                lat=x[0],
                lon=x[1]
                ) for x in points]) + "]"

        return self.html_body["basic_visual"].format(
            style=self.html_dom["style"],
            map_points=map_points,
            center_lat=center_lat,
            center_lon=center_lon
            )



    def verbose_visual_data(self):
        

        dicts = {

        "selection": """

        Select ON STREET OR ROUTE?\n
        1 for ON STREET ... 2 for ROUTE\n

        """,

        "category" : { 1 : "on_street",2 :"route"},

        "table_name" : { "on_street": "ON_STREET_AGG", "route": "ROUTE_AGG"},

        "column_count" :{ "on_street": "on_street_count", "route":"route_count"}

        }

        selection = int(raw_input(dicts['selection']))

        if selection not in [1,2]:
            print self.error.format(function='verbose_visual_data', error="Invalid input")
            exit(1)

        category = dicts["category"][selection]

        self.group_by = category

        table_name = dicts["table_name"][category]

        column_count = dicts["column_count"][category]

        connection = sql.connect(self.db_name)

        cursor1 = connection.cursor()

        cursor2 = connection.cursor()

        select_raw_data = "SELECT {category}, latitude, longitude FROM CTA1012".format(category=category)

        raw_data = cursor1.execute(select_raw_data)

        data_list = []

        for line in raw_data:

            info, latitude, longitude = line

            select_agg_data = """SELECT 
                {category},
                {column_count},
                sum_alight,
                avg_alight,
                sum_board,
                avg_board 
                FROM {table_name}
                WHERE {category} = ?
                """ .format(category=category,column_count=column_count, table_name=table_name)
            
            agg_data = cursor2.execute(select_agg_data, (info,))

            data_list.append([agg_data.fetchone(), latitude,longitude])

        return data_list

    def gen_colors(self,num, type):

        base_num = {1:12, 2:1200, 3:1200}[type]

        if   num <= base_num:       return 0
        elif num <= base_num * 2:   return 1
        elif num <= base_num * 4:   return 2
        elif num <= base_num * 6:   return 3
        elif num <= base_num * 8:   return 4
        elif num <= base_num * 10:  return 5
        elif num <= base_num * 12:  return 6
        elif num <= base_num * 14:  return 7
        elif num <= base_num * 16:  return 8
        elif num <= base_num * 18:  return 9

        return 10

    def verbose_visual(self):

        dicts = {

        "metric" : """
        Sort according to COUNT, AVG_ALIGHT or AVG_BOARD?\n
        1 for COUNT ... 2 for AVG_ALIGHT ... 3 for AVG_BOARD\n
        """,

        "colors" : [
        "FFFFFF",
        "E3F1F0",
        "C7E3E2",
        "ABD6D3",
        "8FC8C5",
        "74BBB6",
        "58ADA8",
        "3CA099",
        "20928B",
        "05857D",
        "000000"
        ],

        "metric_to_color" : {1:1, 2:2, 3:4},

        "metric_name" : {1:"Count", 2 : "Average alighting", 3 : "Average boarding"}

        } 

        data_list = self.verbose_visual_data()

        center_lat = sum(( x[1] for x in data_list )) / len(data_list)

        center_lon = sum(( x[2] for x in data_list )) / len(data_list)

        metric = int(raw_input(dicts['metric']))

        if metric not in [1,2,3]:
            print self.error.format(function="verbose_visual", error="Invalid input")
            exit(1)

        select_metric = dicts["metric_to_color"][metric]

        metric_name = dicts["metric_name"][metric]

        colors = ('\n'.join(self.html_dom["verbose_visual_colors"]
            .format(
                idx=idx,
                color=color
                ) for idx,color in enumerate(dicts["colors"])))

        ### AGG [(NAME, COUNT, SUM_LIGHT, AVG_LIGHT, SUM_BOARD, AVG_BOARD), LAT, LONG]
        map_points = "\n".join(
            [self.html_dom["verbose_visual_dom"]
            .format(
                idx = idx,
                lat = agg[1],
                lon = agg[2],
                name = agg[0][0],
                count = agg[0][1],
                avg_alight = agg[0][2],
                avg_board = agg[0][4],
                color_num = self.gen_colors(agg[0][select_metric],metric)
                ) for idx,agg in enumerate(data_list)])

        return self.html_body["verbose_visual"].format(
            group_by = self.group_by,
            metric_name=metric_name,
            colors=colors,
            map_points=map_points,
            center_lat=center_lat,
            center_lon=center_lon,
            style=self.html_dom["style"])

    def create_map(self, map_type):

        map_type_dict = {

        "verbose" :'verbose_visual.html',
        "basic" : 'basic_visual.html'

        }

        if map_type == "verbose": html = self.verbose_visual()

        elif map_type == "basic": html = self.basic_visual()

        else: print self.error.format(function="create_map", error="Invalid input"); exit(1)

        with open( map_type_dict[map_type], "w") as out:
            out.write(html)

class Bubble(object):

    def __init__(self):
        self.error = "{function}: The following error occured {error}\n"
        self.group_by = ""
        self.metric = ""

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

    var diameter = 1200,
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



        return cursor.execute("SELECT {selected_type},{metric} FROM {table}".format(
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
                    "name": "flare",
                    "children": {body}
                    }}""".format(body=body)

        with open("d3/index.html","w") as out:
            out.write(self.html_text().format(group_by=self.group_by,metric=self.metric))
        with open("d3/flare.json", "w") as out:
            out.write(map_points)

if __name__ == "__main__":

    print "hello there!"





