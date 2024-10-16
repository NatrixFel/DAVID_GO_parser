import argparse
import csv
from collections import defaultdict

# Function to extract gene names and GO terms
def extract_gene_go_terms(file_path):
    gene_go_dict = defaultdict(set)
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')

        for row in reader:
            # Extract the gene name from the 3rd column
            gene_name = row[2]
            # Extract the GO term from the 5th column
            go_term = row[4]
            # Add the GO term to the set associated with the gene name
            gene_go_dict[gene_name].add(go_term)
    
    # Convert sets to semicolon-separated strings for each gene
    return {gene: ';'.join(sorted(go_terms)) for gene, go_terms in gene_go_dict.items()}

# Function to save the results to a TSV file
def save_gene_go_data_to_tsv(gene_go_data, output_path):
    with open(output_path, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        # Write the gene and associated GO terms
        for gene, go_terms in gene_go_data.items():
            writer.writerow([gene, go_terms])

# Main function to handle argument parsing
def main():
    parser = argparse.ArgumentParser(description='Process gene GO terms from a given file.')
    parser.add_argument('input_file', type=str, help='Path to the input file (e.g., all_gene_GO.gaf)')
    parser.add_argument('output_file', type=str, help='Path to the output TSV file (e.g., collapsed_go_terms.tsv)')

    args = parser.parse_args()

    # Extract the gene GO data from the input file
    gene_go_data = extract_gene_go_terms(args.input_file)

    # Save the extracted data to the output TSV file
    save_gene_go_data_to_tsv(gene_go_data, args.output_file)

# Call the main function if this script is executed directly
if __name__ == '__main__':
    main()
