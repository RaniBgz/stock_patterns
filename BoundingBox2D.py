'''
An instance of BoundingBox2D is a Bounding Box (annotated or detected) that
'''



class BoundingBox2D:
    # def __init__(self):
    #     self.box_center = [0 , 0]
    #     self.box_size = [0 , 0]
    #     #Bottom left, top left, top right, bottom right
    #     self.name = ""

    def __init__(self, x1, y1, w, h, name, confidence):
        self.box_center = [x1 , y1]
        self.box_size = [w , h]
        # Bottom left, top left, top right, bottom right
        self.corners = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.name = name
        self.confidence = confidence


    def __str__(self):
        return f'BoxCenter : {self.box_center} BoxSize : {self.box_size}, class name: {self.name}, confidence: {self.confidence}'


    def compute_corners_from_center_and_WH(self):
        x_center, y_center = self.box_center
        width, height = self.box_size

        # Calculate half the dimensions
        half_width = width / 2
        half_height = height / 2

        # Calculate corners with clamping
        bottom_left = (clamp(x_center - half_width), clamp(y_center + half_height))
        top_left = (clamp(x_center - half_width), clamp(y_center - half_height))
        top_right = (clamp(x_center + half_width), clamp(y_center - half_height))
        bottom_right = (clamp(x_center + half_width), clamp(y_center + half_height))

        # Update self.corners
        self.corners = [bottom_left, top_left, top_right, bottom_right]


def clamp(value, min_value=0.0, max_value=1.0):
    """Clamp the value to the range [min_value, max_value]."""
    return max(min_value, min(max_value, value))