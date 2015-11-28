import sqlite3 as sql
from googlemaps import Client
from sys import exit

# This code uses code from
#http://stackoverflow.com/questions/22342097/is-it-possible-to-create-a-google-map-from-python

class Map(object):
    def __init__(self,db_name='bus_data.db'):
        self.db_name = db_name
        self._points = []
        self.html_text = self.html()

    def html(self):
        return {
        "basic_visual": """
        <!DOCTYPE html>
        <html>
            <head>
            <meta charset="utf-8">
            <title>Heatmaps</title>
                <style>
                    html, body {{
                        height: 100%;
                        margin: 0;
                        padding: 0;
                    }}
                    #map {{
                        height: 100%;
                    }}
                </style>
            </head>
            <body>
            <div id="map"></div>
            <script>
            
            var map, heatmap;

            function initMap() {{
                map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 10,
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
"""}
    def add_point(self, coordinates):
        self._points.append(coordinates)

    def basic_visual(self):

        connection = sql.connect('bus_data.db')

        cursor= connection.cursor()

        DATA = cursor.execute("""SELECT latitude, longitude FROM CTA1012""")

        for pair in DATA:
            self.add_point(pair)

        center_lat = sum(( x[0] for x in self._points )) / len(self._points)
        center_lon = sum(( x[1] for x in self._points )) / len(self._points)

        map_points = ",".join(
            [ """new google.maps.LatLng({lat}, {lon})""".format(lat=x[0], lon=x[1]) for x in self._points])
        map_points = '['  + map_points + ']'

        return self.html_text["basic_visual"].format(map_points=map_points, center_lat=center_lat, center_lon=center_lon)
   
    def custom_visual_data(self):

        prompts = {

        "ERROR" : "Invalid Selection Error:",
        "CATEGORY": """
        Which category would you like to select ON STREET OR ROUTE?\n
        1 for ON STREET ... 2 for ROUTE\n
        """
        }

        category = int(raw_input(prompts['CATEGORY']))

        if category not in [1,2]:
            print prompts['error'] + str(category)
            exit(1)

        category = { 1 : "stopagg", 2 :"routeagg"}[category]

        column = {"stopagg": "on_street", "routeagg": "routes"}[category]

        category_type = {"stopagg": "on_street", "routeagg": "route"}[category]

        category_count = {"stopagg": "stop_count", "routeagg":"route_count"}[category]

        connection = sql.connect('bus_data.db')
        cursor1= connection.cursor()
        cursor2= connection.cursor()

        query1 = "SELECT {column}, latitude, longitude FROM CTA1012 LIMIT 100".format(column=column)
        A = cursor1.execute(query1)
        data_list = []
        for line in A:
            info, latitude, longitude = line
            query2 = """SELECT 
                {category_type},
                {category_count},
                sum_alight,
                avg_alight,
                sum_board,
                avg_board 
                FROM {category} WHERE {category_type} = ?""" .format(category_type=category_type,category=category, category_count=category_count)
            B= cursor2.execute(query2, (info,))
            data_list.append([B.fetchone(), latitude,longitude])
        return data_list

    def custom_visual(self):
        data_list = self.custom_visual_data()
        center_lat = sum(( x[1] for x in data_list )) / len(data_list)
        center_lon = sum(( x[2] for x in data_list )) / len(data_list)

        map_points = "\n".join(
            ["""
            var marker{index} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            title: 'Uluru (Ayers Rock)'
        }});

        marker{index}.addListener('click', function () {{
            new google.maps.InfoWindow({{content: '<div id="content">' + 'name: ' + '{name}' + ' count: ' + '{count}' + ' avg_alight: ' + '{avg_alight}' + ' avg_board:' + '{avg_board}' +'</div>'}}).open(map, marker{index});
        }});""".format(index =index, lat=x[1], lon=x[2], name=x[0][0], count=x[0][1], avg_alight=x[0][2], avg_board=x[0][4]) for index,x in enumerate(data_list)])


        print map_points
        return """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Verbose Map</title>
    <style>
        html, body {{
            height: 100%;
            margin: 0;
            padding: 0;
        }}
        #map {{
            height: 100%;
        }}
    </style>
</head>
<body>
<div id="map"></div>
<script>

    function initMap() {{
        var map = new google.maps.Map(document.getElementById('map'), {{
            zoom: 12,
            center: {{lat: {center_lat}, lng: {center_lon}}}
        }});

        {map_points}
}}

</script>
<script async defer
        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDTFj3XyhkCRZ5n6qPE23iwre3qFQgn3NI&signed_in=true&callback=initMap"></script>
</body>
</html>""".format(map_points=map_points, center_lat=center_lat, center_lon=center_lon)









if __name__ == "__main__":
        map = Map()
        with open('complex_visual.html', "w") as out:
         out.write(map.custom_visual())



