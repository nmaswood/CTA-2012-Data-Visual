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
   
    def custom_visual(self):

        prompts = {

        "ERROR" : "Invalid selectionError at step",
        "CATEGORY": """
        Which category would you like to select ON STREET OR ROUTE?\n
        1 for ON STREET ... 2 for ROUTE\n
        """,
        "ORDER": """
        Order by count,  SUM  alightings, AVG alighting, SUM  boardings or AVG boardings,s\n
        1 for count, 2 for SUM alightings, 3 for AVG alightings, 4 for SUM boardings, 5 for AVG boardings\n
        """,
        "SEQ": """
        How would you like to see your results? ASC or DESC?\n
        1 for ASC, 2 for DESC\n
        """,
        "LIM" : """
        Would you like to limit your results?\n
        1 for NO, i for i results\n
        """
        }

        valid = {
        "CATEGORY" : [1,2],
        "ORDER" : [1,2,3,4,5],
        "SEQ" : [1,2],
        "LIM" : "CUSTOM"
        }

        category = int(raw_input(prompts['CATEGORY']))

        if category not in valid['CATEGORY']:
            print prompts['error'] + 'one'
            exit(1)

        category = { 1 : "stopagg", 2 :"routeagg"}[category]

        order = int(raw_input(prompts['ORDER']))

        if order not in valid['ORDER']:
            print prompts['error'] + 'two'
            exit(1)

        order = {
        1 : {"stopagg" : "count_street", "routeagg" : "count_route"}[category],
        2:"sum_alight",
        3:"avg_alight", 
        4:"sum_board",
        5:"avg_board"}[order]

        seq = int(raw_input(prompts['SEQ']))

        if int(seq)  not in valid['SEQ']:
            print prompts['error'] + 'three'
            exit(1)

        seq = {1: "ASC", 2 :"DESC"}[seq]

        lim = int(raw_input(prompts['LIM']))

        if lim <= 0:
            print prompts['error'] + 'four'
            exit(1)

        if lim == 1:
            lim = False

        query = """SELECT {order} FROM {category}
                   ORDER BY {order}""".format(order=order,category=category) 
        print query
        if lim:
            query += " LIMIT %s" % lim

        print category, order, lim, seq
        










if __name__ == "__main__":
        map = Map()
        map.custom_visual()
        #with open('basic_visual.html', "w") as out:
        #   out.write(map.basic_visual())



