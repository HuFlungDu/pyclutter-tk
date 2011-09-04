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
        color1 = gradient.get("color1")
        color2 = gradient.get("color2")
        color1 = [(int(color1[i] + color1[i + 1], 16) / float(0xFF)) for i in range(0, len(color1), 2)]
        color2 = [(int(color2[i] + color2[i + 1], 16) / float(0xFF)) for i in range(0, len(color2), 2)]
        pattern = cairo.LinearGradient(pos1, pos2, pos3, pos4)
        length = math.sqrt((pos4 - pos2) ** 2 + (pos3 - pos1) ** 2)
        pattern.add_color_stop_rgb(0, color1[0], color1[1], color1[2])
        pattern.add_color_stop_rgb(length, color2[0], color2[1], color2[2])
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
        color1 = gradient.get("color1")
        color2 = gradient.get("color2")
        color1 = [(int(color1[i] + color1[i + 1], 16) / float(0xFF)) for i in range(0, len(color1), 2)]
        color2 = [(int(color2[i] + color2[i + 1], 16) / float(0xFF)) for i in range(0, len(color2), 2)]
        radius1 = float(gradient.get("radius1")) * .01
        radius2 = float(gradient.get("radius2")) * .01
        pattern = cairo.RadialGradient(pos1, pos2, radius1, pos3, pos4, radius2)
        pattern.add_color_stop_rgb(0, color1[0], color1[1], color1[2])
        pattern.add_color_stop_rgb(1, color2[0], color2[1], color2[2])
    return pattern