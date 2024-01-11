from numba import njit
@njit
def canView(x1, x2, y1, y2, screen_width, screen_height):
    distance_squared = (x2 - x1)**2 + (y2 - y1)**2
    return distance_squared <= (x1 + screen_width + screen_height)**2