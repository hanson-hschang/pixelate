<div align=center>

# `PIXELATE`

[![Test](https://github.com/hanson-hschang/pixelate/actions/workflows/test.yml/badge.svg)](https://github.com/hanson-hschang/pixelate/actions/workflows/test.yml)
[![Quality](https://github.com/hanson-hschang/pixelate/actions/workflows/quality.yml/badge.svg)](https://github.com/hanson-hschang/pixelate/actions/workflows/quality.yml)
[![Security](https://github.com/hanson-hschang/pixelate/actions/workflows/security.yml/badge.svg)](https://github.com/hanson-hschang/pixelate/actions/workflows/security.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow)](https://opensource.org/licenses/MIT)

[![package: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://docs.astral.sh/uv/)
[![CI/CD: pre-commit](https://img.shields.io/badge/CI/CD-pre--commit-FAB040?logo=pre-commit)](https://pre-commit.com/)
[![syntax: pyupgrade](https://img.shields.io/badge/syntax-pyupgrade-blue?logo=pyupgrade)](https://github.com/pyupgrade/pyupgrade)
[![unit test: pytest](https://img.shields.io/badge/unit_test-pytest-0A9EDC?logo=pytest)](https://docs.pytest.org/)
[![lint & format:Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![static type: mypy](https://img.shields.io/badge/static_type-mypy-blue)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow)](https://bandit.readthedocs.io/)


**a Command Line Interface (CLI) tool that generates pixel art images**

[Installation](#-installation) • [Usage](#-usage) • [Format](#-format)

</div>


## 📦 Installation

Install directly from GitHub using pip (ensure `git` and `python >= 3.11` are installed):

```bash
pip install git+https://github.com/hanson-hschang/pixelate.git
```

## 📝 Usage

### Single file usage
```bash
pixelate filename.md
```
This generates `filename.png` in the same directory as the markdown file.

### Folder usage
```bash
pixelate foldername
```
This processes all `.md` files in the `foldername` folder and generates corresponding PNG files with the same names (e.g., `pixelate.md` -> `pixelate.png`) in the same folder.

### Optional arguments
- `--pixel-size SIZE`: Size of each pixel in the output image (default: 10)
- `--format FORMAT`: Output image format (default: png)

### Examples
```bash
pixelate examples/bird.md
pixelate examples/
pixelate myfile.md --pixel-size 20 --format png
```

## 🎨 Format

### The Markdown File

The input markdown file consists of two parts:
  1. a TOML front-matter section defining colors (both hex color codes and named color palettes), and
  2. a CSV-like pixel grid where each value corresponds to a color defined in the front-matter.

```markdown
+++
# TOML front-matter with color definitions
+++
"1" = "#80808080"      # Gray with transparency
"2" = "base:m"         # Base magenta color
"3" = "tableau:blue"   # Tableau blue color
"4" = "css4:coral"     # CSS4 coral color
"5" = "xkcd:drab"      # XKCD drab color
"0" = "#00000000"      # Transparent (empty pixels)
+++

# CSV-like pixel grid (position indicates row/column)
3,5,2,5,3,0,1,1,1,1,0,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,1,0,1,1,1,1,1
5,4,5,4,5,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0
2,5,2,5,2,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1
5,4,5,4,5,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,0
3,5,2,5,3,0,1,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1
```
<div align=center>

  ![pixelate.png](examples/pixelate.png)

</div>

**Supported Palettes:**

- **Base colors** (8 colors): `base:r` (red), `base:g` (green), `base:b` (blue), `base:c` (cyan), `base:m` (magenta), `base:y` (yellow), `base:k` (black), `base:w` (white)

- **Tableau colors** (10 colors): `tableau:blue`, `tableau:orange`, `tableau:green`, `tableau:red`, `tableau:purple`, `tableau:brown`, `tableau:pink`, `tableau:gray`, `tableau:olive`, `tableau:cyan`

- **CSS4 colors** (139 colors): `css4:red`, `css4:blue`, `css4:green`, `css4:aliceblue`, `css4:antiquewhite`, `css4:aqua (cyan)`, `css4:beige`, `css4:coral`, `css4:gold`, and many more standard web colors

- **XKCD colors** (949 colors): `xkcd:red`, `xkcd:drab`, `xkcd:navy`, `xkcd:lime`, `xkcd:coral`, `xkcd:gold`, `xkcd:azure`, and hundreds more from the XKCD color survey

---

<div align="center">

**[⭐ Star this repository](https://github.com/hanson-hschang/pixelate) if you find it helpful!**

</div>
