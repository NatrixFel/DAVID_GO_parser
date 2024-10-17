import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse
from matplotlib import gridspec

def process_go_table(file_path):
    data = pd.read_csv(file_path, header=None, skiprows=1, sep='\t', names=['GO', 'NS', 'enrichment', 'name',
                                                                            'ratio_in_study', 'ratio_in_pop',
                                                                            'p_uncorrected', 'depth', 'study_count',
                                                                            'p_bonferroni', 'p_sidak', 'p_holm', 'p_fdr_bh',
                                                                            'study_items'])
    
    data['GO'] = data['GO'].str.lstrip('.')  # del excess dots in the first column
    data['p_fdr_bh'] = pd.to_numeric(data['p_fdr_bh'], errors='coerce')
    # FDR <= 0.05
    data = data[data['p_fdr_bh'] <= 0.05]
    # calc -log10(FDR)
    data['-log10(FDR)'] = -np.log10(data['p_fdr_bh'])
    data['GO_with_name'] = data['GO'] + ' ' + data['name']
    return data[['GO_with_name', 'NS', '-log10(FDR)']]

def create_go_heatmap(data, output_image, title):
    data.set_index('GO_with_name', inplace=True)
    
    # fill 0 missing GO terms
    data.fillna(0, inplace=True)
    # make mask for zero-cells
    mask = data == 0
    
    num_rows, num_cols = data.shape
    fig_width = max(10, num_cols * 1.5)
    fig_height = max(10, num_rows * 0.4)
    
    plt.figure(figsize=(fig_width, fig_height))
    cmap = sns.color_palette("Reds", as_cmap=True) #or Blues if down-regulated
    
    ax = sns.heatmap(data, mask=mask, cmap=cmap, linewidths=0.5, linecolor='black',
                     cbar_kws={'orientation': 'horizontal', 'pad': 0.05, 
                                                          'shrink': 0.5, 'aspect': 20}, annot=False)
    
    ax.set_facecolor('dimgrey')
    
    fig = plt.gcf()
    fig_width, fig_height = fig.get_size_inches()
    colorbar = ax.collections[0].colorbar
  
    heatmap_height = ax.get_position().y1 - ax.get_position().y0
    padding = heatmap_height * 0.1 
    colorbar.ax.set_position([ax.get_position().x0, ax.get_position().y1 + padding, ax.get_position().width, 0.03])
  
    colorbar.ax.tick_params(labelsize=14)  
    colorbar.ax.yaxis.set_ticks_position('left') 
    colorbar.ax.yaxis.set_ticks([]) 
    colorbar.ax.xaxis.set_ticks_position('bottom')  
    colorbar.ax.xaxis.set_label_position('bottom') 
    colorbar.ax.xaxis.set_tick_params(pad=3)  
    colorbar.ax.xaxis.set_tick_params(size=14)
    cbar_title = f'{title}\nEnrichment Score (-log10(FDR))'
    colorbar.ax.text(0.5, 1.6, cbar_title, fontsize=14, weight='bold', 
                     ha='center', va='center', transform=colorbar.ax.transAxes)
    
    ax.yaxis.tick_right() 
    ax.yaxis.set_label_position("right")
    
    ax.set_xticklabels(data.columns, rotation=0, fontsize=16)
    ax.set_yticklabels(data.index, rotation=0, horizontalalignment='left', fontsize=14, weight='bold')
    
    ax.set_xlabel('') 
    ax.set_ylabel('') 
   
    plt.savefig(output_image, bbox_inches='tight')
    plt.show()

def create_go_heatmaps_by_ns(input_files, output_prefix):
    combined_data = pd.DataFrame()

   
    for file in input_files:
        sample_name = os.path.splitext(os.path.basename(file))[0]  
        go_data = process_go_table(file)  O
        
        go_data = go_data.rename(columns={'-log10(FDR)': sample_name})
        
        if combined_data.empty:
            combined_data = go_data
        else:
            combined_data = pd.merge(combined_data, go_data, on=['GO_with_name', 'NS'], how='outer')

    for ns_type, ns_label in zip(['CC', 'BP', 'MF'], ['Cellular Component', 'Biological Process', 'Molecular Function']):
        ns_data = combined_data[combined_data['NS'] == ns_type].drop(columns=['NS'])
        
        if not ns_data.empty:
            output_image = f"{output_prefix}_{ns_label}.png"
            create_go_heatmap(ns_data, output_image, ns_label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create GO Term Enrichment Heatmap from multiple files for CC, BP, and MF.')
    parser.add_argument('input_files', nargs='+', help='Paths to GO enrichment files.')
    parser.add_argument('--output_prefix', default='go_enrichment_heatmap', help='Prefix for output image file names.')

    args = parser.parse_args()
    
    create_go_heatmaps_by_ns(args.input_files, args.output_prefix)
