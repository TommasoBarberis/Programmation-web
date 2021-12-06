from flask import Flask, render_template, make_response, abort, jsonify, request, url_for
import os
import matplotlib.pyplot as plt
from io import BytesIO
from utils import *
import json

app = Flask(__name__, template_folder="tp4/templates", static_folder="tp4/static")
app_dir = os.getcwd()

db_ensembl = "tp4/data/ensembl_hs63_simple.sqlite"

@app.route("/")
def cover_page():
    atlas = get_atlas(db_ensembl)
    return render_template("cover_page.html", atlas_list=atlas)

@app.route("/parts/<part>/genes")
def genes_by_part(part):
    genes = get_genes(db_ensembl, part)
    return render_template("genes_list.html", part=part, genes=genes)

@app.route("/genes/<gene_id>")
def gene_page(gene_id):
    gene_data = get_gene_data(db_ensembl, gene_id)
    data_transcript = get_transcipts_data(db_ensembl, gene_id)
    data_part = get_part_by_gene(db_ensembl, gene_id)
    return render_template("gene_page.html", gene_data=gene_data, data_transcript=data_transcript, data_part=data_part)

@app.route("/genes/<gene_id>/parts.png")
def build_hist(gene_id):
    data_part = get_part_by_gene(db_ensembl, gene_id)
    count_dict = {}

    for part in data_part:
        transcript_count = get_transcipts_count(db_ensembl, gene_id, part)
        count_dict[part] = transcript_count[0][0]

    bins = list(count_dict.keys())
    values = list(count_dict.values())

    fig, ax = plt.subplots()  
    ax = plt.bar(bins, values)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()


    b = BytesIO()
    fig.savefig(b, format="png")

    # fig.savefig("/TP_flask/tp4/tmp/hist.png", format="png")

    resp = make_response(b.getvalue())
    resp.headers['content-type'] = 'image/png'
    return resp

@app.route("/api/genes/<gene_id>", methods=["GET"])
def gene_json(gene_id):
    try:
        gene = unwrap_gene(gene_id)
        transcripts_array = unwrap_transcript(db_ensembl, gene_id)
        gene["transcripts"] = transcripts_array
        return jsonify(gene), 200
    except:
        error = {"error": "Ce gène n'existe pas"}          
        return jsonify(error), 404        
        

@app.route("/api/genes/", methods=["GET"])
def genes_list():
    all_genes = get_all_genes(db_ensembl)
    offset = request.args.get('offset')
    if offset:
        all_genes = all_genes[int(offset):]
    try:
        all_genes = all_genes[:100]
    except:
        pass
    
    gene_list = []
    for gene in all_genes:
        gene_id = gene[0]
        gene_dict = unwrap_gene(db_ensembl, gene_id)
        transcripts_array = unwrap_transcript(db_ensembl, gene_id)
        gene_dict["transcript_count"] = int(len(transcripts_array))
        gene_dict["href"] = url_for("gene_json", gene_id=gene_id)
        gene_list.append(gene_dict)

    return jsonify(gene_list), 

@app.route("/api/genes/", methods=["POST"])
def gene_post():
    req = request.get_json()
    keys = [  "Ensembl_Gene_ID", "Associated_Gene_Name", "Chromosome_Name", "Band", "Strand", "Gene_End", "Gene_Start"]
    for key in req.keys():
        if key in keys:
            pass
        else:
            error = {"error": "la clé {key} n'existe pas".format(key=key)}          
            return jsonify(error), 404 

    # try:
    # if type(req["Ensembl_Gene_ID"]) == str and type(req["Chromosome_Name"]) == str and type(req["Band"]) == str and type(req["Associated_Gene_Name"]) == str:
    #         pass
    #     if type(req["Gene_Start"]) == int and type(req["Gene_End"]) == int and type(req["Strand"]) == int:
    #         pass
        
        

    # except:
    #     error = {"error": "Ce gène n'existe pas"}          
    #     return jsonify(error), 404 

    # print(req)
    return str("test")
    