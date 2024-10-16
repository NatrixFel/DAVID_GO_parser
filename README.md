This scripts can be used for prepare study, background and assotiation goatools tables. 
# DAVID GO-parser
``DAVID_Go_parser.py``

Simple parser of GO-enrichment for DAVID functional annotation table. Process gene GO enrichment from a given file.

usage: 

    DAVID_GO_parser2.py [-h] input_file output_file

positional arguments:
  
    input_file   Path to the DAVID input file (e.g., all_gene_GO.txt)
    output_file  Path to the output TSV file (e.g., association_background.tsv)

    options:
    -h, --help   show this help message and exit

# .gaf GO-parser
``gaf_GO_parser.py``

Simple parser of GO-enrichment for .gaf table. Process gene GO enrichment from a given file.

usage:

    gaf_GO_parser.py [-h] input_file output_file

positional arguments:

    input_file   Path to the gaf input file (e.g., all_gene_GO.gaf)
    output_file  Path to the output TSV file (e.g., collapsed_go_terms.tsv)

    options:
    -h, --help   show this help message and exit
