class Rule0:
    def __init__(self):
        pass

    def check_value(self, val):
        return val is not None

    def position_rule(self, position):
        error = {"flag": False, "val": None, "type": "position"}
        #if not 10 < position["x"] < 30:
        error["flag"] = True
        error["val"] = position

        return error

    def rotation_rule(self, direction):
        error = {"flag": False, "val": None, "type": "rotation"}
        #if "up" in direction and "left" in direction:
        #error["flag"] = True
        #error["val"] = direction
        return error

    def angle_rule(self, angle_info):
        error = {"flag": False, "val": None, "type": "angle"}
        if (0 < angle_info["x-y"] < 10) and (50 < angle_info["y-z"] < 90) and (50 < angle_info["x-z"] < 90):
            error["flag"] = True
            error["val"] = angle_info
            error["type"] = "angle"
        return error
    
    def distance_rule(self, dist):
        error = {"flag": False, "val": None, "type": "rotation"}
        #if "up" in direction and "left" in direction:
        error["flag"] = True
        error["type"] = "distance"
        error["val"] = dist
        return error

    def apply_rule(self, direction, position, angle_info, dist):

        # write rules below using processed presets
        # RANDOM RULES BELOW
        if self.check_value(direction):
            rot_rule = self.rotation_rule(direction)

        angle_rule = {"flag": True}
        if self.check_value(angle_info):
            angle_rule = self.angle_rule(angle_info)

        pos_rule = {"flag": True}
        if self.check_value(position):
            pos_rule = self.position_rule(position)

        distance_rule = {"flag": True}
        if self.check_value(dist):
            distance_rule = self.distance_rule(dist)

        flag = rot_rule["flag"] and angle_rule["flag"] and pos_rule["flag"] and distance_rule
        return flag, [rot_rule, pos_rule, angle_rule, distance_rule]
