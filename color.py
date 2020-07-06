def get_y(skin, hair, eyes): #calculates y value where positive is warm, negative is cold, and the extremes of y are more or less contrasting
    if hair < 0:
        y *= -1
        return(y)

def get_season(n1, n2):
    y = "True"
    if n2 >= 20:
        y = "Bold"
    elif n2 <= -20:
        y = "Soft"
    if n1 < 0:
        if abs(n2) < 10:
            y = "Dark"
        if n2 < 0:
            return(y, "Autumn")
        elif n2 > 0:
            return(y, "Winter")
        else:
            return(y, "Autumn or Winter")
    if n1 > 0:
        if abs(n2) < 10:
            y = "Light"
        if n2 < 0:
            return(y, "Summer")
        if n2 > 0:
            return(y, "Spring")
        if n2 == 0:
            return(y, "Summer or Spring")
