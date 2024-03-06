class Rule0:   # Building for seated heel slides
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
        error["flag"] = True
        error["val"] = direction
        return error

    def angle_rule(self, angle_info):
        error = {"flag": False, "val": None, "type": "angle"}
        error["flag"] = True
        error["val"] = angle_info
        return error
        
        #if (-10 < angle_info["x-y"] < 10) and (40 < angle_info["y-z"] < 100) and (40 < angle_info["x-z"] < 100):
        #    error["flag"] = True
        #    error["val"] = angle_info
        #    return error

        # Rule for Heel Slide facing left
        #elif (0 < angle_info["x-y"] < 15) and (110 < angle_info["y-z"] < 159) and (110 < angle_info["x-z"] < 159):
        #    error["flag"] = True
        #    error["val"] = angle_info
        #    return error

        # Rule for Heel Slide facing right
        #elif (0 < angle_info["x-y"] < 15) and (0 < angle_info["y-z"] < 39) and (0 < angle_info["x-z"] < 39):
        #    error["flag"] = True
        #    error["val"] = angle_info
        #    return error
    
    def distance_rule(self, dist):
        error = {"flag": False, "val": None, "type": "distance"}
        #if "up" in direction and "left" in direction:
        error["flag"] = True
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

        flag = rot_rule["flag"] and angle_rule["flag"] and pos_rule["flag"] and distance_rule["flag"]
        return flag, [rot_rule, pos_rule, angle_rule, distance_rule]


############### Rule for Backward Lunge
    
class Rule_Backward_Lunge:   # Building for seated heel slides
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
        error["flag"] = True
        error["val"] = direction
        return error

    def angle_rule(self, angle_info):
        error = {"flag": False, "val": None, "type": "angle"}
    
        #works for right, back and front
        #if (85 < angle_info["x-y"] < 145) and (55 < angle_info["y-z"] < 185) and (115 < angle_info["x-z"] < 185):
        #    error["flag"] = True
        #    error["val"] = angle_info
        #    error["type"] = "angle"
        #    return error

        #works for left
        #elif (70 < angle_info["x-y"] < 140) and (15 < angle_info["y-z"] < 65) and (90 < angle_info["x-z"] < 145):
        #    error["flag"] = True
        #    error["val"] = angle_info
        #    error["type"] = "angle"
        #    return error
        
        error["flag"] = True
        error["val"] = angle_info
        error["type"] = "angle"
        return error

    def distance_rule(self, dist):
        error = {"flag": False, "val": None, "type": "distance"}
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

        flag = rot_rule["flag"] and angle_rule["flag"] and pos_rule["flag"] and distance_rule["flag"]
        return flag, [rot_rule, pos_rule, angle_rule, distance_rule]
    