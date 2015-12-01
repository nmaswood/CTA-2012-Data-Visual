import sqlite3 as sql
from googlemaps import Client
from sys import exit
from haversine import haversine
from Color import Colors

class Map(object):

    def __init__(self,db_name='bus_data.db'):

        self.db_name = db_name

        self.html_body = self.html_body()

        self.html_dom = self.html_dom()

        self.group_by = ""

        self.error = "{function}: The following error occured {error}\n"

        self.colors = Colors()

    def html_body(self):
        return {

        "heat_map": """
        <!DOCTYPE html>
        <html>
            <head>
            <meta charset="utf-8">
            <title>Heatmap</title>
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

        "marker_map": """
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                <meta charset="utf-8">
                <title>Marker Map</title>
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
                        zoom: 12,
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
        "heat_map_dom": "new google.maps.LatLng({lat}, {lon})",

        "marker_map_colors"  : """

                var pinImage{idx} = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + "{color}",
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(5, 5));

                """,

        "marker_map_dom" : """

            var marker{idx} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            icon : pinImage{color_num},
            title: 'name ({name})'
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
   
    def heat_map(self):

        connection = sql.connect(self.db_name)

        cursor = connection.cursor()

        points = cursor.execute("""SELECT latitude, longitude FROM CTA1012""")

        points = [pair for pair in points.fetchall()]

        center_lat = sum(( x[0] for x in points )) / len(points)
        center_lon = sum(( x[1] for x in points )) / len(points)

        map_points = "[" + ",".join(
            [self.html_dom["heat_map_dom"]
            .format(
                lat=x[0],
                lon=x[1]
                ) for x in points]) + "]"

        return self.html_body["heat_map"].format(
            style=self.html_dom["style"],
            map_points=map_points,
            center_lat=center_lat,
            center_lon=center_lon
            )

    ### marker_map_data queries user selected data
    ### from the sql db and returns it as a list

    def marker_map_data(self):
        

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
            print self.error.format(function='marker_map_data', error="Invalid input")
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
                WHERE {category} = ? ORDER BY {category}
                """ .format(category=category,column_count=column_count, table_name=table_name)
            
            agg_data = cursor2.execute(select_agg_data, (info,))

            data_list.append([agg_data.fetchone(), latitude,longitude])

        return data_list
    

    ### thin_data removes close neighbors
    ### so that map data appears less dense
    ### if thin_data = False, the data will
    ### be returned as is

    def thin_data(self,threshold, thin_data):

        data = self.marker_map_data()

        prev_name = data[0][0][0]
        prev_lat = data[0][1]
        prev_lon = data[0][2]  

        new_len = False
        prev_len = thin_data

        while prev_len != new_len:

            prev_len = len(data)

            for line in data[1:]:

                agg,lat,lon = line

                name = agg[0]

                if name == prev_name:

                    distance = haversine((lat,lon),(prev_lat,prev_lon))

                    if distance > threshold: data.remove(line)

                else: prev_name = name

                prev_lat = lat
                prev_lon = lon

            data.sort(key=lambda val: val[0][0])

            new_len = len(data)

        return data


    ### marker_map creates js code for marker map
    ### allows user to select desired metrics

    def marker_map(self,thin_data=True):

        dicts = {

        "metric" : """
        Sort according to COUNT, AVG_ALIGHT or AVG_BOARD?\n
        1 for COUNT ... 2 for AVG_ALIGHT ... 3 for AVG_BOARD\n
        """,

        "metric_to_color" : {1:1, 2:2, 3:4},

        "metric_name" : {1:"Count", 2 : "Average alighting", 3 : "Average boarding"}

        } 

        color_list = self.colors.gradient()

        data_list = self.thin_data(.001,thin_data=thin_data)

        center_lat = sum(( x[1] for x in data_list )) / len(data_list)

        center_lon = sum(( x[2] for x in data_list )) / len(data_list)

        metric = int(raw_input(dicts['metric']))

        if metric not in [1,2,3]:
            print self.error.format(function="marker_map", error="Invalid input")
            exit(1)

        select_metric = dicts["metric_to_color"][metric]

        metric_name = dicts["metric_name"][metric]

        colors = ('\n'.join(self.html_dom["marker_map_colors"]
            .format(
                idx=idx,
                color=color
                ) for idx,color in enumerate(color_list)))

        ### AGG [(NAME, COUNT, SUM_LIGHT, AVG_LIGHT, SUM_BOARD, AVG_BOARD), LAT, LONG]
        map_points = "\n".join(
            [self.html_dom["marker_map_dom"]
            .format(
                idx = idx,
                lat = agg[1],
                lon = agg[2],
                name = agg[0][0],
                count = agg[0][1],
                avg_alight = agg[0][2],
                avg_board = agg[0][4],
                color_num = self.colors.gen_colors(agg[0][select_metric],metric)
                ) for idx,agg in enumerate(data_list)])

        return self.html_body["marker_map"].format(
            group_by = self.group_by,
            metric_name=metric_name,
            colors=colors,
            map_points=map_points,
            center_lat=center_lat,
            center_lon=center_lon,
            style=self.html_dom["style"])

    ### creates desired map and writes it to disk
    ### if verbose is selected data will not be truncated

    def create_map(self, map_type, thin_data=True):

        map_type_dict = {

        "marker" :'gmaps/marker_map.html',
        
        "heat" : 'gmaps/heat_map.html'

        }

        if map_type == "marker": html = self.marker_map(thin_data)

        elif map_type == "heat": html = self.heat_map()

        else: print self.error.format(function="create_map", error="Invalid input"); exit(1)

        with open( map_type_dict[map_type], "w") as out:
            out.write(html)
            
        print "The marker map has been succesfully created\n"