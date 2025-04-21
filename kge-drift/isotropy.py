
delta_1_heads = []
delta_1_tails = []
delta_1_rels = []

delta_2_heads = []
delta_2_tails =[]
delta_2_rels = []

delta_3_heads = []
delta_3_tails = []
delta_3_rels = []    
    
def load_drift_distances(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        triples = ijson.kvitems(f, '')
        
        for triple_key, triple_data in triples:
            try:
                
                # grab head
                head237 = triple_data['dataset_237']["head"]
                head238 = triple_data['dataset_238']["head"]
                head239 = triple_data['dataset_239']["head"]
                
                # grab tail
                tail237 = triple_data['dataset_237']["tail"]
                tail238 = triple_data['dataset_238']["tail"]
                tail239 = triple_data['dataset_239']["tail"]
                
                #grab relation
                rel237 = triple_data['dataset_237']["relation"]
                rel238 = triple_data['dataset_238']["relation"]
                rel239 = triple_data['dataset_239']["relation"]
                
                # push pairwise distance to distances array per SPO term per comparison
                delta_1_heads.append((label, euclidean(head237, head238)))
                delta_2_heads.append((label, euclidean(head237, head239)))
                delta_3_heads.append((label, euclidean(head238, head239)))
                
                # tails
                delta_1_tails.append((label, euclidean(tail237, tail238)))
                delta_2_tails.append((label, euclidean(tail237, tail239)))
                delta_3_tails.append((label, euclidean(tail238, tail239)))
                
                # relationships
                delta_1_rels.append((label, euclidean(rel237, rel238)))
                delta_2_rels.append((label, euclidean(rel237, rel239)))
                delta_3_rels.append((label, euclidean(rel238, rel239)))
                
            except (KeyError, IndexError) as e:
                print(f"Skipping {triple_key} due to missing key or bad format: {e}")