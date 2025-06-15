<h2 align="center">The Purge</h2>

<p align="center">
  <img src="https://github.com/user-attachments/assets/189500a7-e58a-48c9-85b5-51b77e323327" width="300" alt="The Purge logo" />
</p>

<p align="center">
  A fast and simple tool to find and remove duplicate files from any directory tree.<br>
  Reclaim space and keep your folders clean with ease.
</p>

---

### Examples

#### Remove duplicate photos and videos

To purge duplicate image and video files from a specific folder, run:

```sh
thepurge ./path/to/files jpg,jpeg,gif,heic,png,tiff,bmp,raw,webp,mov,mp4,mpeg,avi,wmv,flv,mkv

```

This will scan the `./path/to/files` directory for duplicate files with the specified extensions and remove redundant copies.

#### Remove duplicate documents

For cleaning up duplicate documents (e.g., PDFs and text files):

```sh
thepurge ./documents pdf,docx,doc,txt
```

#### Target all files in a folder

If you want to remove duplicates without filtering by extension:

```sh
thepurge ./downloads
```





⚠️ **The Purge is a work in progress**
