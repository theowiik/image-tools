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
├── compatible/
│   ├── scan1.jpg
│   └── scan2.jpg
├── balanced/
│   ├── scan1.webp
│   └── scan2.webp
└── compact/
    ├── scan1.avif
    └── scan2.avif
```

## Output folders

- `lossless/` - Perfect quality (PNG)
- `compatible/` - Works everywhere (JPEG 95%)
- `balanced/` - Good quality + small size (WebP 90%)
- `compact/` - Smallest, for uploads (AVIF 85%)

