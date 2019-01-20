import click
import pathlib
import os

from .image_server import do_all_processing
from .data.saver import persist_data


@click.command()
@click.option('--shuffle', '-s', help='Shuffle served image order', default=1)
@click.option('--file-name', '-f', help='Name of .csv file')
@click.option('--input-dir', '-i', help='Location of the images.')
@click.option('--output-dir', '-o', help='Location to output .csv file.')
def main(output_dir, input_dir, file_name, shuffle):
    if not input_dir:
        input_dir = '.'

    if not output_dir:
        output_dir = '.'

    if not file_name:
        file_name = 'labels.csv'

    if file_name[-4:] != '.csv':
        file_name += '.csv'

    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()

    click.echo(f'Input dir {input_dir}')
    click.echo(f'Output dir {output_dir}')

    output_path = output_dir.joinpath(file_name)

    fpaths, scores = do_all_processing(input_dir, shuffle_files=shuffle)


    # bit of helpful error handling if user doesn't provide any images
    for val in os.listdir('.'):
        if val[-3:].lower() in ['png', 'jpg']:
            print('found image')
            break
    else:
        print("\n\nDidn't find image at directory:", input_dir)

    persist_data(fpaths, scores, output_path)
