from Map import Map
from Bubble import Bubble

if __name__ == "__main__":

    map = Map()
    bubble = Bubble()

    map.create_map("heat")
    map.create_map("marker")

    bubble.create_bubble()