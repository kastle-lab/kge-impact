'''
fb15k237-classifying.py

Uses API GET requests to query on Freebase MID to WikiData's repository.

WikiData is not a complete reflection of Freebase MID and thus some topics may be lost in translation.
WikiData is used to apply explicit typing of entities and classification of types.

WikiData properties:
    P646: Freebase MID
    P31:  Instance Of
    P279: Subclass
'''

import os
import requests
import json

#  Directory pathing, might need modifications pending where script is ran
home_dir = os.getcwd()
dataset="kastle_FB15k237"
data_path = os.path.join(home_dir,f"datasets/{dataset}")

FILES = ["train.txt", "test.txt", "valid.txt"]
isSco = False # being lazy between two dataset variants

def generate_mid2qid_dict():
    global mid2qid_dict
    mid2qid_dict = dict()
    with open(os.path.join(data_path, "decoded_entity_mids.txt"), "r") as inp:
        lines = [line.strip() for line in inp.readlines()]
    for line in lines:
        mid, _, qid = line.split("\t")
        mid2qid_dict[mid] = qid

def bind_mid2relation(file):
    '''
    bind_mid2relation  

    Pre-conditions:
    - The variable data_path is defined and points to a valid directory.
    - The FILES variable is defined and contains a list of existing filenames.

    Post-conditions:
    - Creates a new file named "{name}-entities.txt" to store unique MID values
    - Appends "{name}-bound.txt" with FB15k-237's existing Entity-to-Entity relationship
      with a simplified Granular Predicate
    '''
    filename = file.replace(".txt","")
    name = filename        
    if(not isSco):
        name = f"{filename}-typed"

    with open(os.path.join(data_path, file), "r") as dataFile:
        dataLines = [line for line in dataFile.readlines()]
        entities = set()
        preds = set()
        for line in dataLines:
            lhs, p, rhs = line.strip().split("\t")
            preds.add(p)
            entities.add(lhs)
            entities.add(rhs)
            tokens = p.split("/")
            # granular_pred = tokens[-1]
            output.write(f"{lhs}\t{p}\t{rhs}\n") # re-write data file with granular predicate
    with open(os.path.join(data_path, f"{name}-entities.txt"), "w") as outputF:
        for entity in entities:
            outputF.write(f"{entity.strip()}\n") # create list of unique entities

def bind_entityType(file):
    '''
    bind_entityType

    Pre-conditions:
    - The variable data_path is defined and points to a valid directory.
    - The FILES variable is defined and contains a list of existing filenames.

    Post-conditions:
    - Creates a new file named "{name}-log.txt" to store any error in the function process
    - Appends "{name}-bound.txt" with WikiData's QID property to explicitly describe
      Entity Types and the Type's respective Subclass relationships
    '''
    filename = file.replace(".txt","")
    name = filename
    if(not isSco):
        name = f"{filename}-typed"
    err = open(os.path.join(data_path,f"{name}-log.txt"), "w")
    with open(os.path.join(data_path, f"{name}-entities.txt"), "r") as entityFile:
        entityMIDs = [ line.strip() for line in entityFile.readlines()]
    
    res = set() # avoids duplicate triples
    dataEntered = False
    for mid in entityMIDs:
        qid = ""
        try:
            qid = mid2qid_dict[mid]
        except KeyError:
            print(f"{mid} not queryable")
            continue
        try:
            query='''PREFIX wikibase: <http://wikiba.se/ontology#>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            '''

            if(isSco):
                query +='''
                Select ?e ?iOf ?sco
                '''
            else:
                query +='''
                Select ?e ?iOf
                '''
            query+='''WHERE{'''
            query+=f"?e wdt:P646 \'{mid}\' ."
            query+='''
            ?e wdt:P31 ?iOf .
            '''
            # unify-typing vs subclass addition to typing
            if(isSco):
                query+='''
                ?iOf wdt:P279 ?sco . 
                '''
            
            
            query+='''} 
            '''   

            query = query.replace("\n","")
            # User-Agent_Policy compliance: https://meta.wikimedia.org/wiki/User-Agent_policy
            headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0'} 

            url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
            data =requests.get(url, params={'query': query, 'format': 'json'}, headers=headers).json()
            dataEntered = False
            
            for item in data['results']['bindings']:
                dataEntered = True
                entity = item['e']['value'].split("/")[-1]
                type = item['iOf']['value'].split("/")[-1]

                res.add(f"{mid}\tinstanceOf\t{type}\n")
                
                if(isSco):
                    sco = item['sco']['value'].split("/")[-1]
                    res.add(f"{type}\tsubclassOf\t{sco}\n")
            

        except:
            try:
                if(isSco):  #  MID attempt for Type-subClassOf-SCO
                    query='''PREFIX wikibase: <http://wikiba.se/ontology#>
                    PREFIX wd: <http://www.wikidata.org/entity/>
                    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    '''

                    query +='''
                    Select ?type ?sco
                    '''

                    query+='''WHERE{'''
                    query+=f"?type wdt:P646 \'{mid}\' ."
                    query+='''
                    ?type wdt:P279 ?sco .
                    '''

                    query+='''} 
                    '''   

                    query = query.replace("\n","")
                    # User-Agent_Policy compliance: https://meta.wikimedia.org/wiki/User-Agent_policy
                    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0'} 

                    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
                    data = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers).json()
                    
                    dataEntered = False
                    for item in data['results']['bindings']:
                        dataEntered = True
                        type = item['type']['value'].split("/")[-1]     
                        sco = item['sco']['value'].split("/")[-1]
                        res.add(f"{type}\tsubclassOf\t{sco}\n")

                    if(not dataEntered):
                        err.write(f"{mid}\n")

            except:
                err.write(f"{mid}\n")                
        if(not dataEntered):
            err.write(f"{mid}\n")     
    for r in res:
        output.write(r)

import datetime 
def main():
    for f in FILES:
        filename = f.replace(".txt","")
        name = filename        
        if(not isSco):
            name = f"{filename}-typed"
        generate_mid2qid_dict()
        global output
        output = open(os.path.join(data_path, f"{name}-bound.txt"), "w") 
        bind_mid2relation(f)
        start = datetime.datetime.now() 
        bind_entityType(f)
        end = datetime.datetime.now()
        t = end-start
        print(f"Total run: {t}")

main()
