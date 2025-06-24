<h2 align="center">The Purge</h2>

<p align="center">
  <img src="https://github.com/user-attachments/assets/189500a7-e58a-48c9-85b5-51b77e323327" width="300" alt="The Purge logo" />
</p>

<p align="center">
  A fast and simple tool to find and remove duplicate files from any directory tree.<br>
  Reclaim space and keep your folders clean with ease.
</p>

---

### Usage

```
 Usage: thepurge.py [OPTIONS] [FOLDER_PATH] [EXTENSIONS]

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   folder_path      [FOLDER_PATH]  The folder to performe duplicated purge [default: .]                                                 │
│   extensions       [EXTENSIONS]   Only target files with provided extensions. Example: jpg,png,gif [default: None]                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --strategy         TEXT     Deduplicate strategy. print, csv. [default: PRINT]                                                         │
│ --processes        INTEGER  Number of processes. [default: 1]                                                                          │
│ --help                      Show this message and exit.                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Example

#### Remove duplicate photos and videos

To purge duplicate image and video files from a specific folder, run:

```sh
thepurge ./path/to/files \
  jpg,jpeg,gif,heic,png,tiff,bmp,raw,webp,mov,mp4,mpeg,avi,wmv,flv,mkv,cr2 \
  --strategy=csv \
  --processes=1
```

This will scan the `./path/to/files` directory for duplicate files with the specified extensions and remove redundant copies.






⚠️ **The Purge is a work in progress**
