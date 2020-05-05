
def lane_view_pixel(y, x, h, w, y_cut):
    ### Evaluates whether pixel is in the area of the image where lines are expected ###
    # y_cut is level of the top corner of visibility triangle
    x_mid = int(w / 2)

    if x <= x_mid:
        # y_cut = h + m * x_mid
        # m = (y_cut - h) / x_mid

        m = - y_cut / w * 2
        y_0 = h + m * x
        return y > y_0

    if x > x_mid:
        # y_cut = m * x_mid
        # m = y_cut / x_mid

        m = 2 * y_cut / w
        b = h - 2 * y_cut
        y_0 = m * x + b
        return y > y_0

def limit_view(image, color=0):
    assert (len(image.shape) == 2), "Only grey scale images are supported"
    img = image.copy()
    height, width = img.shape

    y_cut = int(0.45 * height)
    print(y_cut)
    for x in range(0, width):
        for y in range(0, height):
            if not lane_view_pixel(y, x, height, width, y_cut):
                img[y, x] = color

    return img
