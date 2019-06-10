import face_recognition
from PIL import Image


def cut_portrait(file_path, portrait_size):
    portrait_width, portrait_height = map(int, portrait_size.split('x'))

    # find faces
    image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(image, model='hog')
    assert len(face_locations) > 0

    # take the biggest one
    def area(bounds):
        top, right, bottom, left = bounds
        return (right - left) * (bottom - top)

    biggest_face = max(face_locations, key=area)

    # compute width and height
    top, right, bottom, left = biggest_face
    width = right - left
    height = bottom - top
    assert 0 < width < portrait_width
    assert 0 < height < portrait_height

    # determine portrait bounds
    portrait_left = int(left - (portrait_width - width) * 0.5)
    portrait_right = portrait_left + portrait_width

    portrait_top = int(top - (portrait_height - height) * 0.3)
    portrait_bottom = portrait_top + portrait_height

    # generate a portrait image
    portrait = image[portrait_top:portrait_bottom, portrait_left:portrait_right]
    return Image.fromarray(portrait)
