# Chapter 7: Learning from Data

This guide covers the code and concepts related to Chapter 7 of "Deep Learning and the Game of Go," focusing on generating and processing game data.

## Downloading human games data

The human data is downloaded from the KGS (formerly known as the Kiseido Go Server)

```bash
poetry run python src/dlgo/data/index_processor.py
```

This will download the data to the `data` folder and it will create the file `kgs_index.html` in the main folder.
