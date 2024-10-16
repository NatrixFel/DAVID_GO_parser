import re
import csv
import argparse

# Function to extract gene IDs and GO terms
def extract_gene_go_terms(file_path):
    gene_go_dict = {}
    
    with open(file_path, 'r') as file:
        # Skip the header
        next(file)
        for line in file:
            columns = line.strip().split('\t')
            # Extract the gene ID from the first column
            gene_id = columns[0]
            # Extract all GO terms from the relevant columns (GOTERM_BP_DIRECT, GOTERM_CC_DIRECT, GOTERM_MF_DIRECT)
            go_terms = re.findall(r'GO:\d+', ''.join(columns[3:6]))
            # Join GO terms with ';' and store in the dictionary
            if go_terms:
                gene_go_dict[gene_id] = ';'.join(go_terms)
    
    return gene_go_dict

# Function to save the results to a TSV file
def save_gene_go_data_to_tsv(gene_go_data, output_path):
    with open(output_path, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        for gene_id, go_terms in gene_go_data.items():
            writer.writerow([gene_id, go_terms])

def main():
    parser = argparse.ArgumentParser(description='Process gene GO enrichment from a given file.')
    parser.add_argument('input_file', type=str, help='Path to the input file (e.g., all_gene_GO.txt)')
    parser.add_argument('output_file', type=str, help='Path to the output TSV file (e.g., association_background.tsv)')

    args = parser.parse_args()

    # Extract the gene GO data from the input file
    gene_go_data = extract_gene_go_terms(args.input_file)

    # Save the extracted data to the output TSV file
    save_gene_go_data_to_tsv(gene_go_data, args.output_file)

# Call the main function if this script is executed directly
if __name__ == '__main__':
    main()
