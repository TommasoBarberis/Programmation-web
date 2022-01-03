import sqlite3

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

def get_part_by_gene(db, gene_id):
    gene_data = get_gene_data(db, gene_id)
    data_transcript = get_transcipts_data(db, gene_id)
    data_part= []
    for transcript in data_transcript:
        transcript_id = transcript[0]
        new_part = get_part(db, transcript_id)
        for part in new_part:
            if part[0] is not None:
                data_part.append(part[0])
    
    return list(set(data_part))

def get_transcipts_count(db, gene_id, part):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*) FROM Expression
        WHERE Atlas_Organism_Part = '{part}' AND Ensembl_Transcript_id IN (
            SELECT Ensembl_Transcript_id FROM Transcripts
            WHERE Ensembl_Gene_id = '{gene_id}'
        ) 
        """.format(gene_id=gene_id, part=part))
    return cur.fetchall()

def get_all_genes(db):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM Genes
        ORDER BY Ensembl_Gene_id
        """)
    return cur.fetchall()

def unwrap_gene(db, gene_id):
    gene = get_gene_data(db, gene_id)
    gene = {"Ensembl_Gene_ID": gene["id"], "Associated_Gene_Name": gene["name"], \
    "Chromosome_Name": gene["chr"], "Band": gene["band"], "Strand": gene["strand"], \
    "Gene_End": gene["gene_end"], "Gene_Start": gene["gene_end"]}
    return gene

def unwrap_transcript(db, gene_id):
    transcripts = get_transcipts_data(db, gene_id)
    transcripts_array = []
    for transcript in transcripts:
        transcript_dict = {"Ensembl_Transcript_ID": transcript[0], "Transcript_Start": transcript[1], "Transcript_End": transcript[1]}
        transcripts_array.append(transcript_dict)
    return transcripts_array

def insert_gene(db):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        sql = ''' INSERT INTO projects(name,begin_date,end_date)
        VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()