def get_y(skin, eyes, hair):
    """
    if warm ; y +
    if cold ; y -

    if hair is light ; x +
    if hair is dark; x -
    """

    print("skin", skin, "eyes", eyes, "hair", hair)
    hairshift = abs(hair) - 6

    # Calculating warmth
    # Determines season quadrant (positive is warm, negative is cold)
    warmth = ((skin * 2) + (eyes * 0.1) + (hair * 0.5)) / 3

    # Calculating contrast
    # Determines degree of season (light, dark, soft, bold...)
    if skin < 0:
        contrastskin = 6 - abs(skin)
    else:
        contrastskin = abs(skin)
    contrasthair = 11 - abs(hair)
    print("contrasthair", contrasthair, "contrastskin", contrastskin)
    contrast = abs(abs(contrasthair) - abs(contrastskin)) * 2.7

    if warmth < 0:
        y = contrast * -1
    else:
        y = contrast
    print("hairshift", hairshift)
    if hairshift < 0:
        y *= -1
    print("warmth", warmth, "contrast", contrast, "y", y)
    return(y)

def get_season(n1, n2):
    y = "True"
    if n1 == 0:
        n1 = 0.1
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
