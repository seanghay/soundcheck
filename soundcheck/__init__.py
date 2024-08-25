from tqdm import tqdm
from multiprocessing import Pool
from dataclasses import dataclass
from pathlib import Path
from typing import List
import audioread


@dataclass
class AudioInfo:
  file: str
  channels: int
  sample_rate: int
  duration: float


def audio_info(file):
  with audioread.audio_open(file) as audio:
    return AudioInfo(
      channels=audio.channels,
      sample_rate=audio.samplerate,
      duration=audio.duration,
      file=file,
    )


def audio_directory(
  path: str, globs: List[str], recursive: bool = False, progress=True, n_proc=None
):
  path = Path(path)
  filelist = []

  for glob_pattern in globs:
    glob_iter = path.rglob(glob_pattern) if recursive else path.glob(glob_pattern)
    for file in glob_iter:
      filelist.append(file)

  filelist_info = []
  with tqdm(
    total=len(filelist), disable=not progress or len(filelist) == 0, ascii=True
  ) as pbar:
    with Pool(n_proc) as pool:
      for info in pool.imap_unordered(audio_info, filelist):
        filelist_info.append(info)
        pbar.set_description(info.file.name)
        pbar.update()
  return filelist_info
