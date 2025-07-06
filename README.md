# Apple to Bitwarden Converter

This is a command-line tool to convert password exports from Apple's Keychain (.csv) into a Bitwarden-compatible JSON format for import.

It correctly handles entries with the same credentials across multiple URLs by merging them into a single Bitwarden item with all associated URIs.

## Requirements

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and resolver)

## Installation

1.  **Install `uv`**

    Follow the official installation instructions for `uv`: https://github.com/astral-sh/uv#installation

2.  **Create a virtual environment and install dependencies:**

    Clone this repository, navigate into the project directory, and then run the following `uv` command:

    ```bash
    uv venv
    uv sync
    ```

    This creates a virtual environment in a `.venv` directory and installs the necessary packages specified in `pyproject.toml`.

## Usage

To run the conversion script, use `uv run`. You need to provide the path to your Apple CSV export and a path for the output JSON file.

```bash
uv run apple-to-bitwarden <input-apple-csv> <output-bitwarden-json>
```

**Example:**

```bash
uv run apple-to-bitwarden examples/apple_example.csv bitwarden_import.json
```

This will read `examples/apple_example.csv` and create `bitwarden_import.json` in the project root.

### Options

-   `--folder <name>` / `-f <name>`:  
    Assigns all imported credentials to a specific folder in your Bitwarden vault.

    **Example with folder:**

    ```bash
    uv run apple-to-bitwarden examples/apple_example.csv bitwarden_import.json --folder "Apple Imports"
    ```

## Importing into Bitwarden

1.  Open your Bitwarden Web Vault.
2.  Go to **Tools** > **Import Data**.
3.  Select **Bitwarden (json)** as the file format.
4.  Choose the generated JSON file.
5.  Click **Import Data**.
