from invoke import task
from pathlib import Path
import site


@task
def build(c):
    face_recognition_models_dir = None
    site_packages_dirs = site.getsitepackages()

    for site_packages_dir in site_packages_dirs:
        candidate = Path(site_packages_dir) / 'face_recognition_models'
        if candidate.is_dir():
            face_recognition_models_dir = candidate
            break
    else:
        raise Exception(
            f'Cannot find `face_recognition_models` under your site-packages '
            f'dirs {site_packages_dirs}. Are you sure you have required '
            f'libraries (specifically, `face-recognition`) installed?')

    c.run(
        f'pyinstaller main_script.py '
        f'--name facecutter '
        f'--onefile '
        f'--specpath build/facecutter '
        f'--add-data {face_recognition_models_dir};face_recognition_models')
    c.run(
        f'pyinstaller batch_script.py '
        f'--name facecutter-batch '
        f'--onefile '
        f'--specpath build/facecutter-batch '
        f'--add-data {face_recognition_models_dir};face_recognition_models')
