import os
import time
import argparse
import hashlib
import linecache
from HashTable import hashtable

def generate_main_files(input_index_path: str, output_dict_path: str, output_post_path: str):
    with open(input_index_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
        
    content_rows = content.split("\n")
    actual_word = None
    file_quantity = 0
    posting_id = 0
    dict_hashtable = hashtable[str, dict[str, int]](73369)
    post_content = ""
    for index, row in enumerate(content_rows):
        row_data = row.split(";")
        if (len(row_data) < 3): 
            continue
        if row_data[0] != actual_word and actual_word != None:
            dict_hashtable.add(actual_word, {
                'file_quantity': file_quantity,
                'posting_id': posting_id
            })
            posting_id += file_quantity
            file_quantity = 0
        actual_word = row_data[0]
        file_quantity += 1
        
        post_content += f"{row_data[1]};{row_data[2]}\n"
    dict_hashtable.add(actual_word, {
        'file_quantity': file_quantity,
        'posting_id': posting_id
    })
    
    with open(output_dict_path, 'w', encoding='utf-8', errors='replace') as file:
        file.write(dict_hashtable.tostring())
    with open(output_post_path, 'w', encoding='utf-8', errors='replace') as file:
        file.write(post_content)


def get_dict_data(dict_path: str, post_path: str, token: str) -> list[dict[str, any]]:
    with open(dict_path, 'r', encoding='utf-8', errors='replase') as file:
        line_count = sum(1 for _ in file)
    tokenHash = hashlib.sha1(token.lower().encode()).hexdigest()
    hashKey = int(tokenHash, 16) % (line_count)
    
    token_data: list[dict[str, any]] = []
    
    row_data = linecache.getline(dict_path, hashKey + 1).split("$%i")
    if len(row_data) < 2: return token_data
    records = row_data[1].split("$%c")
    
    for rec in records:
        if rec.split("$%g")[0] == token:
            dict_data = eval(rec.split("$%g")[1])
            for index in range(dict_data["posting_id"] + 1, dict_data["posting_id"] + 1 + dict_data["file_quantity"]):
                posting_row = linecache.getline(post_path, index).split(";")
                token_data.append({
                    "name": posting_row[0],
                    "quant": int(posting_row[1])
                })
            break
    
    return token_data


def main():
    # Declare input parser
    parser = argparse.ArgumentParser(description='Search for files with the tokens of the input')
    parser.add_argument('inputs', nargs='+', type=str, help='Input tokens separated by spaces')
    args = parser.parse_args()
    input_tokens: list[str] = args.inputs
    
    # Get paths
    main_path = os.getcwd()
    index_tokens_path = os.path.join(main_path, 'src/results/data/indexed_tokens.txt')
    token_dict_path = os.path.join(main_path, 'src/results/data/token_dict.txt')
    token_post_path = os.path.join(main_path, 'src/results/data/token_post.txt')
    output_search_log_path = os.path.join(main_path, 'src/results/times/a13_al02883272.txt')
    # If main files don't exists, create them
    if (not os.path.exists(token_dict_path)) or (not os.path.exists(token_post_path)):
        generate_main_files(index_tokens_path, token_dict_path, token_post_path)
    
    # Take time of the process
    process_start_time = time.time()
    
    # Get the files data for each word
    token_data: dict[list[dict[str, any]]] = {}
    for token in input_tokens:
        token_data[token] = get_dict_data(token_dict_path, token_post_path, token)
    
    file_data: dict[str, dict[str, any]] = {}
    for token in list(token_data.keys()):
        for file in token_data[token]:
            if not file["name"] in file_data:
                file_data[file["name"]] = { "word_diversity": 0, "word_quantity": 0 }
            file_data[file["name"]]["word_diversity"] += 1
            file_data[file["name"]]["word_quantity"] += file["quant"]
    file_names = list(file_data.keys())
    files_sorted = sorted(file_names, key=lambda x: (file_data[x]["word_diversity"], file_data[x]["word_quantity"]), reverse=True)
    
    for index in range(0, min(len(files_sorted), 10)):
        print(f"{index + 1}. {files_sorted[index]} - diversity: {file_data[files_sorted[index]]['word_diversity']}  quantity: {file_data[files_sorted[index]]['word_quantity']}")
        
    # End time of the process
    process_end_time = time.time()
    
    with open(output_search_log_path, 'a', encoding='utf-8', errors='replace') as file:
        file.write(f"Búsqueda: \"{' '.join(input_tokens)}\"\t-\tTiempo: {process_end_time - process_start_time} segundos\n")
    
        
            

if __name__ == "__main__":
    main()
