import sqlite3 as sql
from googlemaps import Client

# This code uses code from
#http://stackoverflow.com/questions/22342097/is-it-possible-to-create-a-google-map-from-python

class Map(object):
    def __init__(self):
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
            [ """new google.maps.LatLng({lat}, {lon})""".format(lat=x[0], lon=x[1]) for x in self._points
            ])
        map_points = '['  + map_points + ']'

        return self.html_text["basic_visual"].format(map_points=map_points, center_lat=center_lat, center_lon=center_lon)



if __name__ == "__main__":
        map = Map()
        with open('basic_visual.html', "w") as out:
            out.write(map.basic_visual())



