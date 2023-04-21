# text-to-chunks

Turn text from a URL into files, each containing a chunk of no more than N characters. This is useful for services like ChatGPT which have a maximum number of allowed characters per post.

## Installation

```bash
git clone <this repo's clone url>
cd text-to-chunks
```

## Activating the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Configuring the virtual environment

```bash
pip install -r requirements.txt
```

## Running the project

```bash
python split_text.py <url_or_local_file_path>
```

This will create files in the chunks directory which can be copied to the clipboard one at a time and pasted into ChatGPT without exceeding its character limits.

## Deactivating the virtual environment

```bash
deactivate
```
