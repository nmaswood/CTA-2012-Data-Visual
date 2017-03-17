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
                <title>Traffic Map</title>
                {style}
            </head>
            <body>
            <div id="floating-panel">

                    <b>Rainbow Push Traffic Guide</b>
                    <br>
                    What are streets are good to drive in Chicago?

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
                        src="https://maps.googleapis.com/maps/api/js?key=&signed_in=true&callback=initMap"></script>
            </body>
            </html>
            """

    def gen_html_dom(self):
        return {
        "heat_map_dom": "new google.maps.LatLng({lat}, {lon})",

        "marker_map_colors"  : """

                var heavy = new google.maps.MarkerImage("heavy/heavy_untouched_0.png");
                var medium = new google.maps.MarkerImage("heavy/heavy_untouched_1.png");
                var easy = new google.maps.MarkerImage("heavy/heavy_untouched_2.png");

                var easy0 = new google.maps.MarkerImage("easy/easy_untouched_0.png");
                var easy1 = new google.maps.MarkerImage("easy/easy_untouched_1.png");
                var easy2 = new google.maps.MarkerImage("easy/easy_untouched_2.png");
                var easy3 = new google.maps.MarkerImage("easy/easy_untouched_3.png");
                var easy4 = new google.maps.MarkerImage("easy/easy_untouched_4.png");

                var medium0 = new google.maps.MarkerImage("medium/medium_untouched_1.png");
                var medium1 = new google.maps.MarkerImage("medium/medium_untouched_1.png");
                var medium2 = new google.maps.MarkerImage("medium/medium_untouched_1.png");
                var medium3 = new google.maps.MarkerImage("medium/medium_untouched_1.png");
                var medium4 = new google.maps.MarkerImage("medium/medium_untouched_1.png");

                var heavy0 = new google.maps.MarkerImage("heavy/heavy_untouched_0.png");
                var heavy1 = new google.maps.MarkerImage("heavy/heavy_untouched_1.png");
                var heavy2 = new google.maps.MarkerImage("heavy/heavy_untouched_2.png");
                var heavy3 = new google.maps.MarkerImage("heavy/heavy_untouched_3.png");
                var heavy4 = new google.maps.MarkerImage("heavy/heavy_untouched_4.png");

                var star =  new google.maps.MarkerImage("star_prime.png");

                var markerpush = new google.maps.Marker({
                    position: {lat: 41.804447, lng: -87.603043},
                    map: map,
                    icon : star,
                    size: new google.maps.Size(1, 2),
                    title: \"name (Rainbow Push HQ)\"
                    });

                markerpush.addListener('click', function () {
                new google.maps.InfoWindow({content: '<div id="content">'
                + 'Rainbow Push HQ'
                +'</div>'}).open(map, markerpush);});

                """,

            "marker_map_dom_prime" : """

            var marker{idx} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            icon : {icon},
            size: new google.maps.Size(1, 2),
            title: \"name ({name})\"
            }});

            marker{idx}.addListener('click', function () {{
            new google.maps.InfoWindow({{content: '<div id="content">'
            + 'Street Name: ' + \"{name}\"
            + '<br>'
            + 'Number of Vehicles: ' + \"{volume}\"
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

    @staticmethod
    def assign_icon(number):

        if number > 38000:
            return "heavy4"
        elif number > 35000 :
            return "heavy4"
        elif number > 32000 :
            return "heavy4"
        elif number > 29000 :
            return "heavy3"
        elif number > 26000:
            return "heavy2"
        elif number > 23000:
            return "heavy1"
        elif number > 20000:
            return "medium4"
        elif number > 17000:
            return "medium3"
        elif number > 14000:
            return "medium2"
        elif number > 11000:
            return "medium1"
        elif number > 8000:
            return "medium0"
        elif number > 5000:
            return "easy4"
        elif number > 2000:
            return "easy3"
        elif number > 1500:
            return "easy2"
        elif number > 1000:
            return "easy1"

        return "easy0"


    @staticmethod
    def create_map_point(html_dom_dict, idx,street_name, traffic_data, lat, lon):

        return html_dom_dict["marker_map_dom_prime"].format(
                    idx = idx,
                    lat = lat,
                    lon = lon,
                    name = street_name,
                    volume = traffic_data,
                    icon = Map.assign_icon(int(traffic_data))
        )

    @staticmethod
    def create_map_points(html_dom_dict, map_data):


        map_points = [
                Map.create_map_point(html_dom_dict, idx, street_name, _lat, _long, traffic) for
                idx, (street_name, _lat, _long, traffic) in enumerate(map_data)
        ]

        return '\n'.join(map_points)

    @staticmethod
    def process_data():

        df = read_data()
        map_data = [[str(y) for y in x[1]] for x in df.iterrows()]

        d = {}
        k = {}

        for street, number, lat, lon in map_data:

            num = int(number)

            if street in d:
                if num > d[street]:
                    d[street] = num
                    k[street] = [street, num, lat, lon]
            else:

                d[street] = num
                k[street] = [street, num, lat, lon]


        sorted_map_data = sorted(map_data, key = lambda x: x[1])

        return sorted_map_data


    def marker_map(self):

        a = all_data()
        df = read_data()


        html_dom_dict = self.gen_html_dom()
        html_body = self.gen_html_body()

        center_lat_prime = 41.7943 #df['Latitude'].mean()
        center_lon_prime = -87.5907# df['Longitude'].mean()

        #41.7943° N, 87.5907° W

        print (center_lat_prime, center_lon_prime)

        colors = html_dom_dict["marker_map_colors"]

        map_data =Map.process_data()

        points = Map.create_map_points(html_dom_dict, map_data)

        return html_body.format(
            map_points=points,#map_points_prime,
            center_lat=center_lat_prime,
            center_lon=center_lon_prime,
            colors = colors,
            style=html_dom_dict["style"])

    def create_map(self):

        html = self.marker_map()

        with open('gmaps/marker_map.html', "w") as out:
            out.write(html)
