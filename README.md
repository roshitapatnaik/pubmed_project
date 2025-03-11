# PubMed Project

This project fetches PubMed research papers using the PubMed API.The PubMed Research Paper Fetcher is a command-line tool that allows users to fetch academic research papers from PubMed based on a given search query. The tool extracts key details such as titles, authors, publication dates, affiliations, and corresponding author emails and exports them to a structured CSV file.
This project is implemented using Python, Metapub, Pandas, and Poetry for dependency management.

## Installation
Prerequisites
Before installing, ensure you have:

Python 3.10+ installed (Download Python)
Git installed (Download Git)
Poetry for dependency management (Install Poetry)

## Usage

Run the script with:
poetry run python fetch_pubmed.py "diabetes treatment" -f diabetes_results.csv -d

## Command-Line Options
Option	Description
query	Required. The search term for PubMed.
-f, --file	Output CSV file name (default: results.csv).
-d, --debug	Enable debug mode to print extra details.
query or help: Display usage instructions.
-d or --debug: Print debug information during execution.
-f or --file: Specify the filename to save the results. I
