import os
import re
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import markdown


MAX_LENGTH = 14999
APPEND_MESSAGE = '\n----\nReply with "READ"'
APPEND_MESSAGE_LENGTH = len(APPEND_MESSAGE)
TOKEN_REGEX = r'\b\w+\b'


def get_page_content(url):
    is_local_file = not url.startswith('http')
    if url.endswith('.md'):
        if is_local_file:
            with open(url, 'r') as file:
                md_content = file.read()
        else:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch content from {url}")
                sys.exit(1)
            md_content = response.text
        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, "html.parser")
        return ' '.join(tag.text.strip() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']))
    else:
        if is_local_file:
            with open(url, 'r') as file:
                content = file.read()
        else:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch content from {url}")
                sys.exit(1)
            content = response.text
        return content.replace('\n', ' \n ')


def split_markdown_text(md_content):
    chunks = []
    current_chunk = []
    current_length = 0

    for line in md_content.splitlines():
        line_length = len(line) + 1
        is_heading = re.match(r'^\s*(#{1,6})\s', line)

        if is_heading and current_length + line_length + APPEND_MESSAGE_LENGTH > MAX_LENGTH:
            if current_chunk:
                chunks.append('\n'.join(current_chunk) + f" {APPEND_MESSAGE}")
                current_chunk = []
                current_length = 0

        current_chunk.append(line)
        current_length += line_length

    if current_chunk:
        chunks.append('\n'.join(current_chunk) + f" {APPEND_MESSAGE}")

    return chunks


def split_text(text, max_length=MAX_LENGTH, message=APPEND_MESSAGE):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk) + " " + word) + len(message) + 1 > max_length:
            chunks.append(" ".join(current_chunk) + " " + message)
            current_chunk = []

        current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk) + " " + message)

    return chunks


def create_directory_for_chunks():
    output_directory = "chunks"
    if os.path.exists(output_directory):
        os.system(f"rm -r {output_directory}")
    os.makedirs(output_directory, exist_ok=True)
    return output_directory


def main(url):
    content = get_page_content(url)

    file_extension = os.path.splitext(url)[-1].lower()
    if file_extension == '.md':
        chunks = split_markdown_text(content)
    else:
        chunks = split_text(content)

    # Create a directory for the chunks
    output_directory = create_directory_for_chunks()

    # Save the chunks as separate files
    for i, chunk in enumerate(chunks):
        chunk_tokens = len(re.findall(TOKEN_REGEX, chunk))
        chunk_file_name = f"chunk_{i + 1}_{chunk_tokens}_tks.txt"
        chunk_path = os.path.join(output_directory, chunk_file_name)
        with open(os.path.join(output_directory, chunk_file_name), "w") as file:
            file.write(chunk)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_text.py <url_or_md_file>")
        sys.exit(1)
    main(sys.argv[1])
