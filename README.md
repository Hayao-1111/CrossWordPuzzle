# CrossWordPuzzle
A simple Crossword Puzzle game with Python, Python Homework for summer 2023.

## Usage of Basic Version

```bash
python3 main_basic_version.py [-h] [--path PATH] [--article ARTICLE]
```

arguments list:
```
  -h, --help         show this help message and exit
  --path PATH        set path of data JSON file
  --article ARTICLE  set the name of article
```

the default `PATH` of JSON file is `data.json`, and the default `ARTICLE` is `random`, which means the program will select an article **randomly** from the existing articles in the JSON file.


## NOTE

All the text files are encoded with `utf-8`, End-of-Line-Sequence is `LF`.