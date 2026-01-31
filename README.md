# convert-tif

Converts TIF files to multiple formats. Originals are never modified.

## Usage

```
uv run convert_tif.py /path/to/tif
```

With custom output directory:

```
uv run convert_tif.py /path/to/tif /path/to/output
```

## Output structure

By default, outputs are created inside the input directory:

```
/path/to/tifs/
├── scan1.tif        (untouched)
├── scan2.tif        (untouched)
├── lossless/
│   ├── scan1.png
│   └── scan2.png
├── quality/
│   ├── scan1.jpg
│   └── scan2.jpg
└── compact/
    ├── scan1.jpg
    └── scan2.jpg
```

## Output folders

- `lossless/` - Editing, printing, no generation loss (PNG)
- `quality/` - Sharing, Google Photos (JPEG 95%)
- `compact/` - WhatsApp, Discord, quick shares (JPEG 70%, max 2400px)
