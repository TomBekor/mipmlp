import sys, os
from create_otu_and_mapping_files import CreateOtuAndMappingFiles

preprocess_prms = {'taxonomy_level': 6, 'taxnomy_group': 'sub PCA', 'epsilon': 0.1,
                   'normalization': 'log', 'z_scoring': 'row', 'norm_after_rel': 'No',
                   'std_to_delete': 0, 'pca': (0, 'PCA')}
'''
taxonomy_level 4-7 , taxnomy_group : sub PCA, mean, sum , epsilon: 0-1 
z_scoring: row, col, both , 'pca': (0, 'PCA') second element always PCA. first is 0/1 
normalization: log, relative , norm_after_rel: No, relative
'''


# otu_file = sys.argv[1]
# tag_file = sys.argv[2]
# task_name = sys.argv[3] # Mucositis

def evaluate(params, tag_flag):
    if tag_flag:
        mapping_file = CreateOtuAndMappingFiles("OTU.csv", tags_file_path=None)
    else:
        mapping_file = CreateOtuAndMappingFiles("OTU.csv", "TAG.csv")
    mapping_file.preprocess(preprocess_params=params, visualize=True)
    # mapping_file.rhos_and_pca_calculation(main_task, preprocess_prms['taxonomy_level'], preprocess_prms['pca'],
    # rhos_folder, pca_folder)
    if not tag_flag:
        otu_path, mapping_path, pca_path = mapping_file.csv_to_learn("Mucositis", os.path.join(os.getcwd(), "Mucositis"),
                                                                 preprocess_prms['taxonomy_level'])
    else:
        otu_path, pca_path = mapping_file.csv_to_learn("Mucositis", os.path.join(os.getcwd(), "Mucositis"),
                                                                 preprocess_prms['taxonomy_level'])
    print('CSV files are ready after MIPMLP')
    print('OTU file', otu_path)
    if not tag_flag:
        print('mapping file', mapping_path)
    print('PCA object file', pca_path)
