import os
import io
import service
import pandas as pd
from zipfile import ZipFile
from os.path import basename
from biom import load_table
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)

bp = Blueprint('/', __name__, url_prefix='/')

APP_PATH = 'app'
STATIC_PATH = 'static/'

@bp.route('/Home', methods=('GET', 'POST'))
def home_page():
    error = None
    if request.method == 'POST':
        try:
            os.remove(STATIC_PATH + "Correlation_between_each_component_and_the_label_prognosis_task.svg")
        except:
            print("")
        finally:
            pass
        otu_csv = request.files['otu_csv']
        otu_table = request.files['otu_table']
        taxonomy_file = request.files['taxonomy_file']
        tag_file = request.files['tag_file']
        taxonomy_level = request.form['taxonomy_level']
        taxnomy_group = request.form['taxnomy_group']
        tax_level_plot = request.form["taxonomy_level_for_frequency_plot"]
        epsilon = request.form['epsilon']
        z_scoring = request.form['z_scoring']
        PCA = request.form['PCA']
        comp = request.form['comp']
        normalization = request.form['normalization']
        norm_after_rel = request.form['norm_after_rel']
        alpha_div = request.form['alpha_div']
        beta_div = request.form['beta_div']

        if not otu_csv:
            if not otu_table:
                error = "OTU table is missing."
            elif not taxonomy_file:
                error = "Taxnomy file is missing."
        if not otu_table and not taxonomy_file:
            if not otu_csv:
                error = "Input files are missing."
        if int(comp) == 0:
            error = "The number of components should be -1 or positive integer (not 0)."
        if not error:
            table_path = "table.biom"
            taxonomy_path = "taxonomy.tsv"
            otu_path = "OTU.csv"

            if otu_csv:
                otu_csv.save(otu_path)
            else:
                otu_table.save(table_path)
                taxonomy_file.save(taxonomy_path)
                biom_to_otu(biom_path=table_path, taxonomy_path=taxonomy_path, otu_dest_path=otu_path)

            tag_flag = True
            if tag_file:
                tag_flag = False
                tag_file.save("TAG.csv")
            params = params_dict(taxonomy_level, taxnomy_group, tax_level_plot, epsilon, z_scoring, PCA, int(comp), normalization,
                                 norm_after_rel, alpha_div, beta_div)
            with open("templates/params.txt", "w") as f:
                f.truncate(0)
                f.write(json.dumps(params))
            service.evaluate(params, tag_flag)
            # create a ZipFile object
            with ZipFile('sampleDir.zip', 'w') as zipObj:
                # Iterate over all the files in directory
                for folderName, subfolders, filenames in os.walk("Mucositis"):
                    for filename in filenames:
                        # create complete filepath of file in directory
                        filePath = os.path.join(folderName, filename)
                        # Add file to zip
                        zipObj.write(filePath, basename(filePath))
                for folderName, subfolders, filenames in os.walk(STATIC_PATH):
                    for filename in filenames:
                        if "example" not in filename:
                            # create complete filepath of file in directory
                            filePath = os.path.join(folderName, filename)
                            # Add file to zip
                            zipObj.write(filePath, basename(filePath))
            images_names = [
                STATIC_PATH + 'correlation_heatmap_bacteria.png',
                STATIC_PATH + 'correlation_heatmap_patient.png',
                STATIC_PATH + 'standard_heatmap.png',
                STATIC_PATH + 'samples_variance.png',
                STATIC_PATH + 'density_of_samples.png',
                STATIC_PATH + 'relative_frequency_stacked.png',
                STATIC_PATH + 'beta_diversity.png'
            ]

            if not tag_flag:
                images_names.append(STATIC_PATH + 'Correlation_between_each_component_and_the_label_prognosis_task.png')

            try:
                os.remove("TAG.csv")
            except:
                print("")
            finally:
                pass

        # input validation
        if error:
            flash(error)
        if not error:
            with open("templates/im_name.txt", "w") as f:
                f.truncate(0)
                f.write(json.dumps(images_names))
            return render_template('home.html', active='Home', otu_table=otu_table, tag_file=tag_file,
                                   taxonomy_level=taxonomy_level,
                                   taxnomy_group=taxnomy_group, taxonomy_level_for_frequency_plot=tax_level_plot,
                                   epsilon=epsilon, z_scoring=z_scoring, PCA=PCA,
                                   normalization=normalization,
                                   norm_after_rel=norm_after_rel,
                                   images_names=images_names)

    return render_template('home.html', active='Home', taxonomy_level='Specie',
                           taxnomy_group='Sub-PCA', PCA='None')


def biom_to_otu(biom_path, taxonomy_path, otu_dest_path, **kwargs):
    # Load the biom table and rename index.
    otu_table = load_table(biom_path).to_dataframe(True)
    # Load the taxonomy file and extract the taxonomy column.
    taxonomy = pd.read_csv(taxonomy_path, index_col=0, sep='\t', **kwargs).drop('Confidence', axis=1)
    otu_table = pd.merge(otu_table, taxonomy, right_index=True, left_index=True)
    otu_table.rename({'Taxon': 'taxonomy'}, inplace=True, axis=1)
    otu_table = otu_table.transpose()
    otu_table.index.name = 'ID'
    otu_table.to_csv(otu_dest_path)


@bp.route('/Help')
def help_page():
    return render_template('help.html', active='Help')


@bp.route('/Example')
def example_page():
    return render_template('example.html', active='Example')


@bp.route('/About')
def about_page():
    return render_template('about.html', active='About')

@bp.route('/Results', methods=('GET', 'POST'))
def results_page():
    images_names = None
    is_tag = False
    path = STATIC_PATH + 'Correlation_between_each_component_and_the_label_prognosis_task.svg'
    if os.stat("templates/im_name.txt").st_size != 0:
        with open("templates/im_name.txt", "r") as f:
            images_names = json.loads(f.read())
    if request.method == 'POST':
        tag_file = request.files['tag_file']
        tag_file.save("TAG.csv")
        with open("templates/params.txt", "r") as f:
            params = json.loads(f.read())
        if tag_file or os.path.exists(path):
            is_tag = True
            service.evaluate(params, False)
    if type(images_names) == list:
        if len(images_names) < 8:
            images_names.append("")
        images_names[7] = path
    return render_template('images.html', active='Results', images_names=images_names, is_tag=is_tag)



@bp.route('/download-outputs')
def download():
    return send_file("sampleDir.zip", mimetype='zip', as_attachment=True, )


@bp.route('/download-example-files')
def download_example():
    return send_file(STATIC_PATH + "example_input_files.zip", mimetype='zip', as_attachment=True, )


def params_dict(taxonomy_level, taxnomy_group, tax_level_plot, epsilon, z_scoring, pca, comp, normalization, norm_after_rel, alpha_div, beta_div):
    taxonomy_level_dict = {"Order": 4, "Family": 5, "Genus": 6, "Specie": 7}
    taxonomy_group_dict = {"Sub-PCA": 'sub PCA', "Mean": 'mean', "Sum": 'sum'}
    tax_level_plot_dict = {"Class": 3, "Phylum": 2, "Order": 4}
    z_scoring_dict = {"Row": 'row', "Column": 'col', "Both": 'both', "None": 'No'}
    normalization_dict = {"Log": 'log', "Relative": 'relative'}
    norm_after_rel_dict = {"No": 'No', "Yes": 'z_after_relative'}
    dimension_reduction_dict = {"PCA": (comp, 'PCA'), "ICA": (comp, 'ICA'), "None": (0, 'PCA')}
    alpha_div_dict = {"Shannon": "shannon", "Observed OTUs": "observed_otus", "Chao1": "chao1"}
    beta_div_dict = {"Unwieghted unifrac": "unwieghted_unifrac", "Weighted unifrac": "wieghted_unifrac", "Bray-Curtis": "braycurtis"}
    params = {
        'taxonomy_level': taxonomy_level_dict[taxonomy_level],
        'taxnomy_group': taxonomy_group_dict[taxnomy_group],
        'tax_level_plot': tax_level_plot_dict[tax_level_plot],
        'epsilon': epsilon,
        'normalization': normalization_dict[normalization],
        'z_scoring': z_scoring_dict[z_scoring],
        'norm_after_rel': norm_after_rel_dict[norm_after_rel],
        'std_to_delete': 0,
        'pca': dimension_reduction_dict[pca],
        'alpha_div': alpha_div_dict[alpha_div],
        'beta_div': beta_div_dict[beta_div]
    }
    print(params)
    return params
