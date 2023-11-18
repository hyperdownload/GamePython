import numpy as np
def canView(x1,x2,y1,y2,screen_width, screen_height):
        distance = np.sqrt((np.abs(x2 - x1))**2 + (np.abs(y2 - y1))**2)
        return distance <= x1 + screen_width + screen_height