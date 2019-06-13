import click

from facecutter import cut_portrait


@click.command(help='facecutter')
@click.argument('source_file')
@click.option('-o', '--output-file')
@click.option('--portrait-size', default='400x600')
def cli(source_file, output_file, portrait_size):
    portrait_image = cut_portrait(source_file, portrait_size)

    # save or show
    if output_file:
        portrait_image.save(output_file)
    else:
        portrait_image.show()
