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


class Map(object):
    def __init__(self,db_name='bus_data.db'):
        self.db_name = db_name
        self.html_body = self.html_body()
        self.html_dom = self.html_dom()

    def html_body(self):
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

                var pinImage{index} = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + "{color}",
                new google.maps.Size(21, 34),
                new google.maps.Point(0,0),
                new google.maps.Point(5, 5));
                
                """,

        "verbose_visual_dom" : """

            var marker{index} = new google.maps.Marker({{
            position: {{lat: {lat}, lng: {lon}}},
            map: map,
            icon : pinImage{color_num},
            title: 'name (Chicago)'
            }});

            marker{index}.addListener('click', function () {{
            new google.maps.InfoWindow({{content: '<div id="content">'
            + 'name: ' + '{name}' +
            ' count: ' + '{count}' +
            ' avg_alight: ' + '{avg_alight}' +
            ' avg_board:' + '{avg_board}' +'</div>'}}).open(map, marker{index});}});

            """
        }
   
    def basic_visual(self):

        connection = sql.connect(self.db_name)

        cursor = connection.cursor()

        points = cursor.execute("""SELECT latitude, longitude FROM CTA1012""")

        points = [pair for pair in points.fetchall()]

        center_lat = sum(( x[0] for x in points )) / len(points)
        center_lon = sum(( x[1] for x in points )) / len(points)

        map_points = "[" + ",".join(
            [self.html_dom["basic_visual_dom"].format(lat=x[0], lon=x[1]) for x in points]) + "]"

        return self.html_body["basic_visual"].format(map_points=map_points, center_lat=center_lat, center_lon=center_lon)



    def verbose_visual_data(self):
        

        dicts = {

        "error" : "Invalid Selection Error:",

        "selection": """

        Select ON STREET OR ROUTE?\n
        1 for ON STREET ... 2 for ROUTE\n

        """,

        "category" : { 1 : "on_street",2 :"route"},

        "table_name" : {"on_street": "ON_STREET_AGG", "route": "ROUTE_AGG"},

        "column_count" :{"on_street": "on_street_count", "route":"route_count"}

        }

        selection = int(raw_input(dicts['selection']))

        if selection not in [1,2]: print dicts['error'] + str(selection); exit(1)

        category = dicts["category"][selection]

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

    def assign_colors(self,num, type):

        print "TYPE", type

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
        1 for COUNT ... 2 for AVG_ALIGHT ... 3 AVG_BOARD\n
        """,

        "error": "Invalid input:\n",

        "colors" : ["FFFFFF","E3F1F0","C7E3E2","ABD6D3","8FC8C5","74BBB6","58ADA8","3CA099","20928B","05857D","000000"],

        "metric_to_color" : {1:1, 2:2, 3:4}

        } 

        data_list = self.verbose_visual_data()

        center_lat = sum(( x[1] for x in data_list )) / len(data_list)

        center_lon = sum(( x[2] for x in data_list )) / len(data_list)

        metric = int(raw_input(dicts['metric']))

        if metric not in [1,2,3]:
            print prompts['error'] + str(metric)
            exit(1)

        select_metric = dicts["metric_to_color"][metric]

        colors = ('\n'.join(self.html_dom["verbose_visual_colors"].format(index=idx, color=color) for idx,color in enumerate(dicts["colors"])))

        map_points = "\n".join(
            [self.html_dom["verbose_visual_dom"].format(index =index, lat=x[1], lon=x[2], name=x[0][0], count=x[0][1], avg_alight=x[0][2], avg_board=x[0][4], color_num=self.assign_colors(x[0][select_metric],metric)) for index,x in enumerate(data_list)])

        return self.html_body["verbose_visual"].format(colors=colors,map_points=map_points, center_lat=center_lat, center_lon=center_lon)

    def create_map(self, map_type):
        map_type_dict = {

        "verbose" :'verbose_visual.html',
        "basic" : 'basic_visual.html'

        }

        if map_type == "verbose": html = self.verbose_visual()

        elif map_type == "basic": html = self.basic_visual()

        else: print "Error invalid input"; exit(1)

        with open( map_type_dict[map_type], "w") as out:
            out.write(html)


if __name__ == "__main__":
        map = Map()
        map.create_map("verbose")



