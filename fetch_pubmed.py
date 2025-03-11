import argparse
import os
from metapub import PubMedFetcher
import pandas as pd
from functools import reduce

# Set NCBI API key for PubMed
os.environ["NCBI_API_KEY"] = "09e2dda3eb8513799f06d2c9fc69c886c309"

fetch = PubMedFetcher()

# Keywords to identify company affiliations and exclude academic institutions
COMPANY_KEYWORDS = ["Inc.", "Ltd.", "Pharma", "Biotech", "Corporation", "Technologies", "Research"]
ACADEMIC_KEYWORDS = ["University", "College", "Institute", "Hospital", "School", "Academy", "Lab"]

# Function to handle command-line arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers based on a query.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", help="Output filename for CSV results.", default="results.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    return parser.parse_args()

# Function to check if an author is non-academic
def extract_non_academic_authors(authors, affiliations):
    non_academic_authors = []
    company_affiliations = []

    for author, affiliation in zip(authors, affiliations):
        if any(keyword in affiliation for keyword in COMPANY_KEYWORDS) and not any(keyword in affiliation for keyword in ACADEMIC_KEYWORDS):
            non_academic_authors.append(author)
            company_affiliations.append(affiliation)

    return ", ".join(non_academic_authors) if non_academic_authors else "N/A", ", ".join(company_affiliations) if company_affiliations else "N/A"

# Function to fetch papers
def fetch_papers(query, num_of_articles=5, debug=False):
    if debug:
        print(f"Fetching papers for query: {query}")

    pmids = fetch.pmids_for_query(query, retmax=num_of_articles)

    if debug:
        print(f"Found PMIDs: {pmids}")

    articles = {}
    titles = {}
    abstracts = {}
    authors = {}
    years = {}
    volumes = {}
    issues = {}
    journals = {}
    citations = {}
    links = {}
    non_academic_authors_dict = {}
    company_affiliations_dict = {}
    corresponding_emails_dict = {}


    for pmid in pmids:
        article = fetch.article_by_pmid(pmid)
        articles[pmid] = article  

        titles[pmid] = article.title if article.title else "N/A"
        abstracts[pmid] = article.abstract if article.abstract else "N/A"
        authors[pmid] = ", ".join(article.authors) if article.authors else "N/A"
        years[pmid] = article.year if article.year else "N/A"
        volumes[pmid] = article.volume if article.volume else "N/A"
        issues[pmid] = article.issue if article.issue else "N/A"
        journals[pmid] = article.journal if article.journal else "N/A"
        citations[pmid] = article.citation if article.citation else "N/A"
        links[pmid] = article.url if article.url else "N/A"

        # Extract affiliations properly
        author_affiliations = article.author_affiliations if hasattr(article, 'author_affiliations') else []

        # Extract non-academic authors and company affiliations
        if article.authors and author_affiliations:
            non_academic_authors, company_affiliations = extract_non_academic_authors(article.authors, author_affiliations)
        else:
            non_academic_authors, company_affiliations = "N/A", "N/A"

        non_academic_authors_dict[pmid] = non_academic_authors
        company_affiliations_dict[pmid] = company_affiliations

        # Extract corresponding author email
        corresponding_email = article.corresponding_author_email if hasattr(article, 'corresponding_author_email') else "N/A"
        corresponding_emails_dict[pmid] = corresponding_email

    return (articles, titles, abstracts, authors, years, volumes, issues, journals, citations, links, 
            non_academic_authors_dict, company_affiliations_dict, corresponding_emails_dict)
# Function to save data to CSV
def save_to_csv(filename, articles, titles, abstracts, authors, years, volumes, issues, journals, citations, links, non_academic_authors, company_affiliations, corresponding_emails):
    df_title = pd.DataFrame(list(titles.items()), columns=["pmid", "Title"])
    df_abstract = pd.DataFrame(list(abstracts.items()), columns=["pmid", "Abstract"])
    df_author = pd.DataFrame(list(authors.items()), columns=["pmid", "Author"])
    df_year = pd.DataFrame(list(years.items()), columns=["pmid", "Year"])
    df_volume = pd.DataFrame(list(volumes.items()), columns=["pmid", "Volume"])
    df_issue = pd.DataFrame(list(issues.items()), columns=["pmid", "Issue"])
    df_journal = pd.DataFrame(list(journals.items()), columns=["pmid", "Journal"])
    df_citation = pd.DataFrame(list(citations.items()), columns=["pmid", "Citation"])
    df_link = pd.DataFrame(list(links.items()), columns=["pmid", "Link"])
    df_non_academic = pd.DataFrame(list(non_academic_authors.items()), columns=["pmid", "Non-academic Authors"])
    df_company = pd.DataFrame(list(company_affiliations.items()), columns=["pmid", "Company Affiliations"])
    df_email = pd.DataFrame(list(corresponding_emails.items()), columns=["pmid", "Corresponding Author Email"])

    data_frames = [
        df_title, df_abstract, df_author, df_year, df_volume, df_issue, df_journal, df_citation, df_link,
        df_non_academic, df_company, df_email
    ]
    
    df_merged = reduce(lambda left, right: pd.merge(left, right, on="pmid", how="outer"), data_frames)

    df_merged.to_csv(filename, index=False)
    print(f"Merged CSV file saved as '{filename}'")

# Main function
def main():
    args = get_arguments()
    
    (articles, titles, abstracts, authors, years, volumes, issues, journals, citations, links, 
     non_academic_authors, company_affiliations, corresponding_emails) = fetch_papers(
        args.query, num_of_articles=5, debug=args.debug
    )
    
    save_to_csv(args.file, articles, titles, abstracts, authors, years, volumes, issues, journals, citations, links, non_academic_authors, company_affiliations, corresponding_emails)

# Run the script
if __name__ == "__main__":
    main()
