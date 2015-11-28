import sqlite3 as sql
from googlemaps import Client
from sys import exit

# This code uses code from
#http://stackoverflow.com/questions/22342097/is-it-possible-to-create-a-google-map-from-python


### Basic Visual

### Returns a heat map where higher density refers bus stops that
### appear more frequently


### Verbose Visual

### Returns a heat map  where the darker the pin drop 
### the more frequently the bus stop or route appears
### A user can also click on the pin drop and see the statisitics associated with it

### TO DO ###

### Build a more visually appealing graph that shows aggregate statistics

### Make  Map Keys for all graphs via the html

### Clean up and format Python AND html code

### remove self.addpoints and self_points


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
""",
        "verbose_visual":
        """
        <!DOCTYPE html>
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
            </html>"""}
    def add_point(self, coordinates):
        self._points.append(coordinates)

    def basic_visual(self):

        connection = sql.connect('bus_data.db')

        cursor = connection.cursor()

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

        category = { 1 : "ON_STREET", 2 :"ROUTE"}[category]

        table_name = {"ON_STREET": "ON_STREET_AGG", "ROUTE": "ROUTE_AGG"}[category]

        column = {"ON_STREET": "on_street", "ROUTE": "route"}[category]

        column_count = {"ON_STREET": "on_street_count", "ROUTE":"route_count"}[category]

        connection = sql.connect('bus_data.db')
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()

        select_raw_data = "SELECT {column}, latitude, longitude FROM CTA1012".format(column=column)

        raw_data = cursor1.execute(select_raw_data)

        data_list = []

        for line in raw_data:

            info, latitude, longitude = line

            select_agg_data = """SELECT 
                {column},
                {column_count},
                sum_alight,
                avg_alight,
                sum_board,
                avg_board 
                FROM {table_name} WHERE {column} = ?""" .format(column=column,column_count=column_count, table_name=table_name)
            
            agg_data = cursor2.execute(select_agg_data, (info,))

            data_list.append([agg_data.fetchone(), latitude,longitude])

        return data_list

    def assign_colors(self,num, type):

        base_num = {1:12, 2:1200, 3:1200}[type]

        if num <=  base_num:  print base_num * 2; return "FFFFFF"
        elif num <= base_num * 2:  print base_num * 3;  return "E3F1F0" 
        elif num <= base_num * 4: print base_num * 4; return "C7E3E2" 
        elif num <= base_num * 6:   print base_num * 5;return "ABD6D3"
        elif num <= base_num * 8:   print base_num * 6;return "8FC8C5" 
        elif num <= base_num * 10:   print base_num * 7;return "74BBB6" 
        elif num <= base_num * 12:  print base_num * 8;return "58ADA8" 
        elif num <= base_num * 14:  print base_num * 9;return "3CA099" 
        elif num <= base_num * 16:  print base_num* 10;return "20928B" 
        elif num <= base_num * 18:  print base_num * 10; return "05857D" 

        return "000000"

    def custom_visual(self):
        data_list = self.custom_visual_data()
        center_lat = sum(( x[1] for x in data_list )) / len(data_list)
        center_lon = sum(( x[2] for x in data_list )) / len(data_list)

        prompts ={"METRIC" : """
        Sort according to COUNT, AVG_ALIGHT, SUM_BOARD or AVG_BOARD?\n
        1 for COUNT ... 2 for AVG_ALIGHT ... 3 AVG_BOARD\n
        """,
        "ERROR": "An error has occured:\n"}

        metric = int(raw_input(prompts['METRIC']))
        if metric not in [1,2,3,4,5]:
            print prompts['Error'] + metric
            exit(1)

        metric= {1:1, 2:2, 3:4}[metric]


        map_points = "\n".join(
            ["""


            var pinColor{index} = "{pinColor}";
            var pinImage{index} = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor{index},
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(5, 5));

            var marker{index} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            icon : pinImage{index},
            title: 'Uluru (Ayers Rock)'
            }});

            marker{index}.addListener('click', function () {{
            new google.maps.InfoWindow({{content: '<div id="content">'
            + 'name: ' + '{name}' +
            ' count: ' + '{count}' +
            ' avg_alight: ' + '{avg_alight}' +
            ' avg_board:' + '{avg_board}' +'</div>'}}).open(map, marker{index});}});
        """.format(index =index, lat=x[1], lon=x[2], name=x[0][0], count=x[0][1], avg_alight=x[0][2], avg_board=x[0][4], pinColor=self.assign_colors(x[0][metric],metric)) for index,x in enumerate(data_list)])

        return self.html_text["verbose_visual"].format(map_points=map_points, center_lat=center_lat, center_lon=center_lon)









if __name__ == "__main__":
        map = Map()
        with open('verbose_visual.html', "w") as out:
            out.write(map.custom_visual())



