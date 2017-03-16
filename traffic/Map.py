import sqlite3 as sql
from googlemaps import Client
from sys import exit
from Color import Colors
from data_prime import all_data
from process import read_data

class Map(object):

    def gen_html_body(self):

        return  """
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                <meta charset="utf-8">
                <title>Coffee Map</title>
                {style}
            </head>
            <body>
            <div id="floating-panel">

                    <b>Rainbow Push Traffic Guide</b>
                    <br>
                    So you'd like to get a cup of coffee down town?

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
                        src="https://maps.googleapis.com/maps/api/js?key=&signed_in=true&callback=initMap"></script>
            </body>
            </html>
            """

    def gen_html_dom(self):
        return {
        "heat_map_dom": "new google.maps.LatLng({lat}, {lon})",

        "marker_map_colors"  : """
                var dunkin = new google.maps.MarkerImage("d.png");
                var starbucks = new google.maps.MarkerImage("s.png");
                var misc = new google.maps.MarkerImage("m.png");
                var peets = new google.maps.MarkerImage("p.png");
                var argos = new google.maps.MarkerImage("a.png");
                var argo = new google.maps.MarkerImage("a.png");
                """,

            "marker_map_dom_prime" : """

            var marker{idx} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            icon : {icon},
            size: new google.maps.Size(1, 2),
            title: \"name jklasdjf({name})\"
            }});

            marker{idx}.addListener('click', function () {{
            new google.maps.InfoWindow({{content: '<div id="content">'
            + 'name: ' + \"{name}\"
            +'</div>'}}).open(map, marker{idx});}});

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



    def marker_map(self):

        a = all_data()
        df = read_data()

        print (df.as_matrix())

        html_dom_dict = self.gen_html_dom()
        html_body = self.gen_html_body()

        center_lat_prime = sum((x[1] for x in a)) / len(a)
        center_lon_prime = sum((x[2] for x in a)) / len(a)

        colors = html_dom_dict["marker_map_colors"]
        print (colors)

        map_points_prime = "\n".join(
            [html_dom_dict["marker_map_dom_prime"]
            .format(
                idx = idx,
                lat = agg[1],
                lon = agg[2],
                name = agg[0],
                icon = agg[3],
                ) for idx,agg in enumerate(a)])


        return html_body.format(
            map_points=map_points_prime,
            center_lat=center_lat_prime,
            center_lon=center_lon_prime,
            colors = colors,
            style=html_dom_dict["style"])

    def create_map(self):

        html = self.marker_map()

        with open('gmaps/marker_map.html', "w") as out:
            out.write(html)

