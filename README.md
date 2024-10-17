This scripts can be used for GO enrichment analysis. DAVID and GAF GO-parsers make assotiation goatools table and heatmap-script makes illustration of GO enrichment. 
# DAVID GO-parser
``DAVID_Go_parser.py``

Simple parser of GO-enrichment for DAVID functional annotation table. Process gene GO enrichment from a given file.

https://david.ncifcrf.gov/

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

https://geneontology.org/docs/download-ontology/

usage:

    gaf_GO_parser.py [-h] input_file output_file

positional arguments:

    input_file   Path to the gaf input file (e.g., all_gene_GO.gaf)
    output_file  Path to the output TSV file (e.g., collapsed_go_terms.tsv)

    options:
    -h, --help   show this help message and exit

# Make GO heatmap

``heatmap_GO.py``

Create GO Term Enrichment Heatmap from multiple files. Input file(s) must look like goatools table:

https://github.com/tanghaibao/goatools

| GO | NS | enrichment | name | ratio_in_study | ratio_in_pop | p_uncorrected | depth | study_count | p_bonferroni | p_sidak | p_holm | p_fdr_bh | study_items |
| -- | -- | ---------- |------|----------------|--------------|---------------|-------|-------------|--------------|---------|--------|----------|-------------|
| GO:0005829 | CC | p | cytosol | 2/88 | 735/4013 | 0.001 | 1 | 2 | 0.001 | 0.001 | 0.001 | 0.001 | Gene1, Gene2, Gene3 |

![heat_GO](https://github.com/user-attachments/assets/ceb0f9b4-4745-467c-af68-f53dffb9177e)

usage: 

    GO_heatmap_up.py [-h] [--output OUTPUT] input_files [input_files ...]

positional arguments:
    
    input_files      Paths to GO enrichment files.

    options:
    -h, --help       show this help message and exit
    --output OUTPUT  Output image file name (default: go_enrichment_heatmap.png).

Another script ``heatmap_GO_fit.py`` create three GO Term Enrichment Heatmap for BP, MF and CC from multiple files. 
![CC_full](https://github.com/user-attachments/assets/0c7e4bb2-b1fd-409d-ad23-954a4a5e08b3)
![BP_full](https://github.com/user-attachments/assets/c81179c8-6004-4fa1-b821-96d6ca4b3246)
![MF_full](https://github.com/user-attachments/assets/fc6e3250-8b3d-4364-b4e8-5ce5d1d78495)


