import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse

def process_go_table(file_path):
    # check all goatools outputs
    data = pd.read_csv(file_path, header=None, skiprows=1, sep='\t', names=['GO', 'NS', 'enrichment', 'name',
                                                                            'ratio_in_study', 'ratio_in_pop',
                                                                            'p_uncorrected', 'depth', 'study_count',
                                                                            'p_bonferroni', 'p_sidak', 'p_holm', 'p_fdr_bh',
                                                                            'study_items'])
    
    data['GO'] = data['GO'].str.lstrip('.')  # delete dots from first column
    data['p_fdr_bh'] = pd.to_numeric(data['p_fdr_bh'], errors='coerce')
    # FDR <= 0.05
    data = data[data['p_fdr_bh'] <= 0.05]
    # calc -log10(FDR)
    data['-log10(FDR)'] = -np.log10(data['p_fdr_bh'])
    data['GO_with_name'] = data['GO'] + ' ' + data['name']
    return data[['GO_with_name', '-log10(FDR)']]

def create_go_heatmap(input_files, output_image):
    combined_data = pd.DataFrame()

    for file in input_files:
        sample_name = os.path.splitext(os.path.basename(file))[0]
        go_data = process_go_table(file) 
        
        go_data = go_data.rename(columns={'-log10(FDR)': sample_name})
        
        if combined_data.empty:
            combined_data = go_data
        else:
            combined_data = pd.merge(combined_data, go_data, on='GO_with_name', how='outer')
        
    combined_data.set_index('GO_with_name', inplace=True)
  
    # fill 0 missing GO terms
    combined_data.fillna(0, inplace=True)
    # make mask for zero-cells
    mask = combined_data == 0

    plt.figure(figsize=(10,20))
    cmap = sns.color_palette("Reds", as_cmap=True) # or Blues for down-regulated GO
    
    ax = sns.heatmap(combined_data, mask=mask, cmap=cmap, linewidths=0.5, linecolor='black',
                     cbar_kws={'orientation': 'horizontal'}, annot=False, cbar=True)
    
    # make gray cells with zero value
    ax.set_facecolor('dimgrey')

    # colorbar up
    colorbar = ax.collections[0].colorbar
    colorbar.ax.set_position([0.1, 0.9, 0.8, 0.03]) 
    colorbar.set_label('Enrichment Score (-log10(FDR))', fontsize=14, weight='bold') 
    colorbar.ax.yaxis.label.set_fontweight('bold')  
    colorbar.ax.tick_params(labelsize=13)  
    colorbar.ax.yaxis.set_ticks_position('left') 
    colorbar.ax.yaxis.set_ticks([]) 
    colorbar.ax.xaxis.set_ticks_position('top')
    colorbar.ax.xaxis.set_label_position('top') 
    colorbar.ax.xaxis.set_tick_params(pad=3) 
    colorbar.ax.xaxis.set_tick_params(size=14)
    
    # move GO to the right part
    ax.yaxis.tick_right() 
    ax.yaxis.set_label_position("right")
    ax.set_yticklabels(combined_data.index, rotation=0, horizontalalignment='left', fontsize=14, weight='bold') 
  
    ax.set_xticklabels(combined_data.columns, rotation=0, fontsize=16)
    
    ax.set_xlabel('')
    ax.set_ylabel('') 
  
    plt.savefig(output_image, bbox_inches='tight')
    plt.show()


# Использование argparse для обработки командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create GO Term Enrichment Heatmap from multiple files.')
    parser.add_argument('input_files', nargs='+', help='Paths to GO enrichment files.')
    parser.add_argument('--output', default='go_enrichment_heatmap.png', help='Output image file name.')

    args = parser.parse_args()
  
    create_go_heatmap(args.input_files, args.output)
