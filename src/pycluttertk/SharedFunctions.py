import cairo
import math
def MakeGradient(gradient, h, w):
    if gradient.get("type") == "linear":
        start = gradient.get("start").split("-")
        end = gradient.get("end").split("-")
        pos1 = 0
        pos2 = 0
        pos3 = 0
        pos4 = 0
        if start[0] == "top":
            pos2 = 0
        elif start[0] == "mid":
            pos2 = h / 2
        elif start[0] == "bottom":
            pos2 = h
        if start[1] == "left":
            pos1 = 0
        elif start[1] == "mid":
            pos1 = w / 2
        elif start[1] == "right":
            pos1 = w
        if end[0] == "top":
            pos4 = 0
        elif end[0] == "mid":
            pos4 = h / 2
        elif end[0] == "bottom":
            pos4 = h
        if end[1] == "left":
            pos3 = 0
        elif end[1] == "mid":
            pos3 = w / 2
        elif end[1] == "right":
            pos3 = w
        pattern = cairo.LinearGradient(pos1, pos2, pos3, pos4)
        length = math.sqrt((pos4 - pos2) ** 2 + (pos3 - pos1) ** 2)
        for stop in gradient.findall("stop"):
            color = stop.get("color")
            color = [(int(color[i] + color[i + 1], 16) / float(0xFF)) for i in range(0, len(color), 2)]
            alpha = float(stop.get("alpha")) 
            position = float(stop.get("position"))      
            pattern.add_color_stop_rgba(length*(position*.01), color[0], color[1], color[2],alpha)
    elif gradient.get("type") == "radial":
        start = gradient.get("start").split("-")
        end = gradient.get("end").split("-")
        pos1 = 0
        pos2 = 0
        pos3 = 0
        pos4 = 0
        if start[0] == "top":
            pos2 = 0
        elif start[0] == "mid":
            pos2 = h / 2
        elif start[0] == "bottom":
            pos2 = h
        if start[1] == "left":
            pos1 = 0
        elif start[1] == "mid":
            pos1 = w / 2
        elif start[1] == "right":
            pos1 = w
        if end[0] == "top":
            pos4 = 0
        elif end[0] == "mid":
            pos4 = h / 2
        elif end[0] == "bottom":
            pos4 = h
        if end[1] == "left":
            pos3 = 0
        elif end[1] == "mid":
            pos3 = w / 2
        elif end[1] == "right":
            pos3 = w

        length = math.sqrt((pos4 - pos2) ** 2 + (pos3 - pos1) ** 2)
        radius1 = float(gradient.get("radius1")) * .01
        radius2 = float(gradient.get("radius2")) * .01
        pattern = cairo.RadialGradient(pos1, pos2, radius1, pos3, pos4, radius2)
        for stop in gradient.findall("stop"):
            color = stop.get("color")
            color = [(int(color[i] + color[i + 1], 16) / float(0xFF)) for i in range(0, len(color), 2)]
            alpha = float(stop.get("alpha")) 
            position = float(stop.get("position"))      
            pattern.add_color_stop_rgba(length*(position*.01), color[0], color[1], color[2],alpha)
    return pattern