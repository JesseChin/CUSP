import math
class Overlap:
        percent_overlap = 0.1
        radius = 10.0
        coords = []
        
        __instance = None

        #Overrides __new__ to force Singleton implementation
        def __new__(cls, *args, **kwargs):
                if cls.__instance is None:
                        cls.__instance = super().__new__(cls)
                return cls.__instance

        def __init__(self, percent_overlap, radius, coordinate):
                self.percent_overlap = percent_overlap
                self.radius = radius
                self.coords.append(coordinate)

        # Given a coordinate, will check to see if exceeds overlap required to take new photo
        # Returns true if picture should be taken
        # Returns false if still within range of another picture
        def check_coordinate(self, coordinate):
                shortest_distance = math.sqrt((x[0] - coordinate[0])**2 + (x[1] - coordinate[1]))
                index = 1
                for x in self.coords[1:]:
                        distance = math.sqrt((x[0] - coordinate[0])**2 + (x[1] - coordinate[1]))
                        if(distance < shortest_distance):
                                shortest_distance = distance
                        index += 1
                if(shortest_distance >= (2*self.radius - self.radius*self.percent_overlap)):
                        print("Taking Picture")
                        self.coords.append(coordinate)
                        return True
                else:
                        print("Skipping Picture")
                        return False