import click
from pathlib import Path

from facecutter import load_image, find_face, frame_face, crop_face


@click.command(help='facecutter')
@click.argument('data_folder')
@click.option('--force', is_flag=True)
def cli(data_folder, force):
    # find all 'photo.png' files underneath this folder
    found_photos = Path(data_folder).resolve().glob('**/photo.png')
    portrait_bounds = None
    for photo_path in found_photos:
        portrait_path = photo_path.parent / 'portrait.png'
        if force or not portrait_path.exists():
            print(f'generating portrait for {photo_path}')
            photo_image = load_image(photo_path)

            face_bounds = find_face(photo_image)
            if face_bounds:
                portrait_bounds = frame_face(face_bounds, '400x600')

            portrait_image = crop_face(photo_image, portrait_bounds)
            portrait_image.save(portrait_path)
            print(f'generated {portrait_path}')


if __name__ == '__main__':
    cli()
