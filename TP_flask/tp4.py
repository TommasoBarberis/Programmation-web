from flask import Flask, render_template
import sqlite3, os

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
    data_part = []
    for transcript in data_transcript:
        transcript_id = transcript[0]
        new_part = get_part(db_ensembl, transcript_id)
        data_part.append(new_part)
    return render_template("gene_page.html", gene_data=gene_data, data_transcript=data_transcript, data_part=data_part)

def get_atlas(db):            
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT atlas_organism_part FROM Expression WHERE atlas_organism_part != "None" ORDER BY atlas_organism_part ')
        return cur.fetchall()

def get_genes(db, part):
     with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT DISTINCT g.ensembl_gene_id, associated_gene_name
            FROM Genes as g
            NATURAL JOIN Transcripts as t
            NATURAL JOIN Expression as e
            WHERE atlas_organism_part = '{part}'
            ORDER BY g.ensembl_gene_id""".format(part=part))
        return cur.fetchall()     
        
def get_gene_data(db, gene_id):
    gene_dict = {}
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute("""
        SELECT DISTINCT ensembl_gene_id FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["id"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT chromosome_name FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["chr"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT band FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["band"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT strand FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["strand"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT gene_start FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["gene_start"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT gene_end FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["gene_end"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT associated_gene_name FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["name"] = cur.fetchall()[0][0]

        cur.execute("""
        SELECT DISTINCT transcript_count FROM Genes
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
        gene_dict["count"] = cur.fetchall()[0][0]

    return gene_dict

def get_transcipts_data(db, gene_id):
    transcript_dict = {}
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute("""
        SELECT DISTINCT ensembl_transcript_id, transcript_start, transcript_end FROM Transcripts
            WHERE Ensembl_Gene_id = '{gene_id}'
        """.format(gene_id=gene_id))
    return cur.fetchall()

def get_part(db, transcript_id):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute("""
        SELECT DISTINCT atlas_organism_part FROM Expression
            WHERE Ensembl_Transcript_id = '{transcript_id}'
        """.format(transcript_id=transcript_id))
    return cur.fetchall()    