import click
import pathlib
import os

from kneejerk.image_server import score_images_in_dir
from kneejerk.data.saver import persist_scores, persist_metadata
from kneejerk.data.loader import segment_data_from_csv


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = dict()


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
@click.option('--file_name', '-f', help='Name of .csv file', required=True)
@click.option('--consider_size', '-c', help='Consider the size of the images',
              default=0)
@click.option('--rescale_len', '-r', help='Height/width to rescale the data to',
              default=200)
@click.option('--trainpct', help='Percentage of data to train on',
              default=.70)
@click.option('--testpct', help='Percentage of data to test on',
              default=.20)
@click.option('--valpct', help='Percentage of data to validate on',
              default=.10)
@click.pass_context
def transfer(ctx, file_name, consider_size, rescale_len, trainpct, testpct, valpct):
    ctx.obj['file_name'] = file_name
    ctx.obj['dirname'] = file_name[:-4]

    persist_metadata()


if __name__ == '__main__':
    main()
