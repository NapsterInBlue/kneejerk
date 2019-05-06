import click
import pathlib
import os

from kneejerk.image_server import score_images_in_dir
from kneejerk.data.saver import persist_scores


@click.group()
def main():
    pass


@main.command(help='Cycle through a directory and score images')
@click.option('--input_dir', '-i', help='Location of the images.',
              default='.')
@click.option('--output_dir', '-o', help='Location to output .csv file.',
              default='.')
@click.option('--shuffle', '-s', help='Shuffle served image order',
              default=1)
@click.option('--file-name', '-f', help='Name of .csv file',
              default='output.csv')
@click.option('--min', 'min_', help='Minimum acceptable score', default='0')
@click.option('--max', 'max_', help='Maximum acceptable score', default='1')
@click.pass_context
def score(ctx, output_dir, input_dir, file_name, shuffle, min_, max_):
    ctx.obj = dict()
    ctx.obj['min_val'] = min_
    ctx.obj['max_val'] = max_

    if file_name[-4:] != '.csv':
        file_name += '.csv'

    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()

    click.echo(f'Input dir {input_dir}')
    click.echo(f'Output dir {output_dir}')

    output_path = output_dir.joinpath(file_name)

    fpaths, scores = score_images_in_dir(input_dir, shuffle_files=shuffle)

    # bit of helpful error handling if user doesn't provide any images
    for val in os.listdir(input_dir):
        if val[-3:].lower() in ['png', 'jpg']:
            break
    else:
        print("\n\nDidn't find image at directory:", input_dir)

    persist_scores(fpaths, scores, output_path)


@main.command(help='Use a kneejerk-generated csv to organize your files')
@click.option('--file-name', '-f', help='Name of .csv file',
              default='output.csv')
@click.option('--input-dir', '-i', help='Location of the images.',
              default='.')
@click.option('--output-dir', '-o', help='Location to output .csv file.',
              default='.')
def transfer():
    pass


if __name__ == '__main__':
    main()
