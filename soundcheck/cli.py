import csv
from pathlib import Path
from soundcheck import audio_directory, audio_info
from prettytable import PrettyTable
from format_duration import format_duration, DurationLimit
from datetime import timedelta
import click


@click.command()
@click.option(
  "-i",
  "--input",
  type=click.Path(exists=True, dir_okay=True, file_okay=True),
  required=True,
  multiple=True,
)
@click.option(
  "-e",
  "--extension",
  default=["*.wav", "*.mp3", "*.flac"],
  help="File extension to scan for. e.g. *.mp3",
  type=str,
  multiple=True,
)
@click.option(
  "-o",
  "--output",
  type=click.Path(writable=True),
  help="Output tsv file",
  required=False,
)
@click.option("-r", "--recursive", default=False, help="Recursive", is_flag=True)
@click.option("-q", "--quiet", default=False, help="Silent", is_flag=True)
@click.option("-j", "--jobs", default=None, help="Number of jobs")
def cli(extension, input, output, recursive, jobs, quiet):
  # handle single file
  if len(input) == 1 and Path(input[0]).is_file():
    info = audio_info(input[0])
    table = PrettyTable()
    table.field_names = ["Sample Rate(Hz)", "Duration(s)", "Channels"]
    table.add_rows([[info.sample_rate, info.duration, info.channels]])
    print(table)
    return

  collections = []
  for input_path in input:
    input_path = Path(input_path)

    if input_path.is_file():
      info = audio_info(input_path)
      collections.append(info)
      continue

    for info in audio_directory(
      input_path,
      globs=list(extension),
      n_proc=jobs,
      recursive=recursive,
      progress=not quiet,
    ):
      collections.append(info)

  if len(collections) == 0:
    print("No audio found.")
    return

  # print stats
  total_duration = sum([c.duration for c in collections])
  min_duration = min([c.duration for c in collections])
  max_duration = max([c.duration for c in collections])

  table = PrettyTable()
  table.field_names = [
    "Total Files",
    "Total Duration",
    "Avg. Duration",
    "Min. Duration",
    "Max. Duration",
  ]

  table.add_rows(
    [
      [
        f"{len(collections):,}",
        format_duration(timedelta(seconds=total_duration), True, DurationLimit.MINUTE),
        format_duration(
          timedelta(seconds=total_duration / len(collections)),
          True,
          DurationLimit.SECOND,
        ),
        f"{min_duration:.4f}",
        f"{max_duration:.4f}",
      ],
      [
        f"{len(collections):,}",
        f"{total_duration / 60 / 60:.4f} hrs",
        f"{total_duration / len(collections):.4f}",
        f"{min_duration:.4f}",
        f"{max_duration:.4f}",
      ]
    ]
  )

  print(table)

  if output is not None:
    output_path = Path(output)
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as outfile:
      writer = csv.writer(outfile, delimiter="\t")
      for info in collections:
        writer.writerow(
          [
            str(info.file),
            info.duration,
            info.sample_rate,
            info.channels,
          ]
        )
