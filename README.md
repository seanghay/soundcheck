## SoundCheck

A multi-processing audio check


```shell
pip install soundcheck
```

### Basic example

```shell
soundcheck -i audio-dir/wavs
```

Result

```
+-------------+----------------+---------------+---------------+---------------+
| Total Files | Total Duration | Avg. Duration | Min. Duration | Max. Duration |
+-------------+----------------+---------------+---------------+---------------+
|    6,032    |  19 h, 44 m    |      11 s     |     0.6300    |    145.0200   |
+-------------+----------------+---------------+---------------+---------------+
```

### Advanced Usage

```shell
soundcheck -q -r -i audio-dir -e "*.mp3" -e "*.aac" -j 4 -o filelist.tsv
```

### CLI Reference

```
Usage: soundcheck [OPTIONS]

Options:
  -i, --input PATH      [required]
  -e, --extension TEXT  File extension to scan for. e.g. *.mp3
  -o, --output PATH     Output tsv file
  -r, --recursive       Recursive
  -q, --quiet           Silent
  -j, --jobs TEXT       Number of jobs
  --help                Show this message and exit.
```