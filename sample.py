import click
from pathlib import Path

from facecutter import cut_portrait


@click.command(help='facecutter')
@click.argument('data_folder')
@click.option('--force', is_flag=True)
def cli(data_folder, force):
    # find all 'photo.png' files underneath this folder
    found_photos = Path(data_folder).resolve().glob('**/photo.png')
    for photo_path in found_photos:
        portrait_path = photo_path.parent / 'portrait.png'
        if force or not portrait_path.exists():
            print(f'generating portrait for {photo_path}')
            portrait_image = cut_portrait(photo_path, '200x300')
            portrait_image.save(portrait_path)
            print(f'generated {portrait_path}')


if __name__ == '__main__':
    cli()
