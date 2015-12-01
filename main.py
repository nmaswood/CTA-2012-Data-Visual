from Map import Map
from Bubble import Bubble




if __name__ == "__main__":

    map = Map()

    map.create_map("heat")
    map.create_map("marker")

    bubble = Bubble()
    bubble.create_bubble()