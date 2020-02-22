import click

from facecutter import (
    load_image,
    find_face,
    frame_face,
    crop_face,
    cut_portrait)
from pathlib import Path


@click.command()
@click.argument('source_file')
@click.option('-o', '--output-file')
@click.option('--portrait-size', default='400x600', show_default=True)
@click.option('--fallback-bounds', help=(
    'bounds to fall back to if a face cannot be auto-detected with the deep '
    'learning model. This should be given in the form of a comma-separate '
    'list of 4 integers, representing pixel values for {top},'
    '{right},{bottom},{left} bounds of the portrait'))
def facecutter(source_file, output_file, portrait_size, fallback_bounds):
    '''
    `facecutter` is a tool that cuts out the portrait of a face that appears in
    a given photo. You provide the photo and a portrait size. Facecutter will
    run a deep learning model for face recognition on the photo, and cut out
    a portrait of the given size using the biggest face it found. It's possible
    that the biggest face it found is not an actual face, and it's possible that
    it will not find a face even when one exists. After all, deep learning
    models are not perfect, but it should work fairly well for most cases.

    If you already know roughly where the face probably is and can provide a
    set of fallback bounds, you can provide it, and it will use the fallback
    bounds to crop out a face if a face cannot be detected via the deep
    learning model.

    The cropped face will by default be displayed on screen, but you can of
    course give it an output file for it to save to.
    '''
    if fallback_bounds:
        try:
            fallback_bounds = [int(part) for part in fallback_bounds.split(',')]
            assert len(fallback_bounds) == 4
        except Exception:
            print(
                'Error: fallback bounds must be given as a comma-separate list '
                'of 4 integers, representing pixel values of (portrait_top, '
                'portrait_right, portrait_bottom, portrait_left)')
            raise

    portrait_image, portrait_bounds = cut_portrait(
        source_file, portrait_size, fallback_bounds=fallback_bounds)

    # on success, print the portrait bounds in the format expected by
    # --fallback-bounds
    print(','.join(f'{bound}' for bound in portrait_bounds))

    # save or show
    if output_file:
        portrait_image.save(output_file)
    else:
        portrait_image.show()


@click.command()
@click.argument('source_folder')
@click.argument('file_name')
@click.argument('output_file_name')
@click.option('--portrait-size', default='400x600', show_default=True)
@click.option('--fallback', is_flag=True)
@click.option('--force', is_flag=True)
def facecutter_batch(
        source_folder,
        file_name,
        output_file_name,
        portrait_size,
        fallback,
        force):
    '''
    `facecutter-batch` is a tool that batch-cuts portraits from photos
    underneath some top-level SOURCE_FOLDER.

    For each photo of the given FILE_NAME found somewhere underneath the
    SOURCE_FOLDER, the tool will attempt to cut out a portrait and save it
    at the sibling location as OUTPUT_FILE_NAME. To do this, the tool will
    run a deep learning model for face recognition on the photo, and cut out
    a portrait of the given size using the biggest face it finds. It's possible
    that the biggest face it found is not an actual face, and it's possible that
    it will not find a face even when one exists. After all, deep learning
    models are not perfect, but it should work fairly well for most cases.

    If `--fallback` is provided, then each successful attempt to detect a face
    will have the resulting portrait bounds saved as a fallback set of portrait
    bounds to be reused for photos where a face cannot be detected. The
    assumption is that all such photos are similar so if a face was detected
    in one photo, then the bounds would roughly frame a similar face in another
    photo even if a face cannot be detected in that other photo.

    By default, a FILE_NAME will be skipped if its corresponding
    OUTPUT_FILE_NAME already exists as a file. `--force` can be provided to
    instead override the OUTPUT_FILE_NAME that already exists.

    The size of the portrait to cut out can be modified via `--portrait-size`
    '''
    deferred = []
    fallback_portrait_bounds = None

    found_photos = Path(source_folder).resolve().glob('**/{file_name}')
    for photo_path in found_photos:
        portrait_path = photo_path.parent / output_file_name

        short_photo_path = photo_path.relative_to(source_folder)
        short_portrait_path = portrait_path.relative_to(source_folder)

        if force or not portrait_path.exists():
            print(f'generating portrait for {short_photo_path}')
            photo_image = load_image(photo_path)
            portrait_bounds = None

            face_bounds = find_face(photo_image)
            if face_bounds:
                portrait_bounds = frame_face(face_bounds, '400x600')
                fallback_portrait_bounds = portrait_bounds
                print(f'  determined bounds {portrait_bounds}')
            elif fallback:
                if fallback_portrait_bounds:
                    portrait_bounds = fallback_portrait_bounds
                    print(f'  using fallback bounds {portrait_bounds}')
                else:
                    deferred.append(photo_path, photo_image, portrait_path)
                    print(
                        f'  failed to determine bounds, no fallback bounds, '
                        f'deferring to later')
                    continue
            else:
                print(f'  FAILED TO GENERATE PORTRAIT FOR {short_photo_path}')
                continue

            portrait_image = crop_face(photo_image, portrait_bounds)
            portrait_image.save(portrait_path)
            print(f'  cropped portrait saved to {short_portrait_path}')

    if fallback:
        for photo_path, photo_image, portrait_path in deferred:
            short_photo_path = photo_path.relative_to(source_folder)
            short_portrait_path = portrait_path.relative_to(source_folder)

            print(f're-trying previously failed attempt on {short_photo_path}')
            if fallback_portrait_bounds:
                print(f'  using fallback bounds {fallback_portrait_bounds}')
                portrait_image = crop_face(
                    photo_image, fallback_portrait_bounds)
                portrait_image.save(portrait_path)
                print(f'  cropped portrait saved to {short_portrait_path}')
            else:
                print(f'  FAILED TO GENERATE PORTRAIT FOR {short_photo_path}')
