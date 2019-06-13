import face_recognition
from PIL import Image


def load_image(file_path):
    return face_recognition.load_image_file(file_path)


def find_face(image):
    face_locations = face_recognition.face_locations(image, model='hog')
    if not face_locations:
        return None

    # take the biggest one
    def area(bounds):
        top, right, bottom, left = bounds
        return (right - left) * (bottom - top)

    biggest_face = max(face_locations, key=area)
    return biggest_face


def frame_face(face_bounds, portrait_size):
    portrait_width, portrait_height = map(int, portrait_size.split('x'))

    # compute width and height
    top, right, bottom, left = face_bounds
    width = right - left
    height = bottom - top
    assert 0 < width < portrait_width
    assert 0 < height < portrait_height

    # determine portrait bounds
    portrait_left = int(left - (portrait_width - width) * 0.5)
    portrait_right = portrait_left + portrait_width

    portrait_top = int(top - (portrait_height - height) * 0.3)
    portrait_bottom = portrait_top + portrait_height

    return (portrait_top, portrait_right, portrait_bottom, portrait_left)


def crop_face(image, portrait_bounds):
    (portrait_top,
     portrait_right,
     portrait_bottom,
     portrait_left) = portrait_bounds

    # generate a portrait image
    portrait = image[portrait_top:portrait_bottom, portrait_left:portrait_right]
    return Image.fromarray(portrait)


def cut_portrait(file_path, portrait_size, fallback_bounds=None):
    image = load_image(file_path)
    face_bounds = find_face(image)

    if face_bounds:
        portrait_bounds = frame_face(face_bounds, portrait_size)
    elif fallback_bounds:
        portrait_bounds = fallback_bounds
    else:
        raise Exception(f'Could not find a face for {file_path}')

    return crop_face(image, portrait_bounds)
