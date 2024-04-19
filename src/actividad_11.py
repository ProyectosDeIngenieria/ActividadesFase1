import os
import re
import time

def get_total_token_count(file_path: str) -> float:
    """Get the total token count of a file.
    Args:
        file_path (str): path of the file.
    Returns:
        number: the total number of tokens in the file.
    """
    # Read file content
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    separated_words = re.split('[\n|,| |.|:|;|(|)]', content) # Separate the words of the files
    filtered_words = [word for word in separated_words if word.isalnum()] # Remove any word with special symbols
    return float(len(filtered_words)) # return token count

def create_posting_file(files_path: str, output_file: str, document_ids: dict):
    """Create a posting file for all HTML files in the given directory.
    Args:
        files_path (str): Path to the directory containing HTML files.
        output_file (str): Path to the output posting file.
        document_ids (dict): Dictionary containing document IDs.
    """
    posting = {}
    html_files = [file for file in os.listdir(files_path) if file.endswith('.html')]
    for file_name in html_files:
        file_path = os.path.join(files_path, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
            words = re.findall(r'\w+', content.lower())  # Extract words
            total_tokens = len(words)
            token_count = {}
            for word in words:
                if word in token_count:
                    token_count[word] += 1
                else:
                    token_count[word] = 1
            
            for word, count in token_count.items():
                if word in posting:
                    if document_ids[file_name] in posting[word]:
                        posting[word][document_ids[file_name]] += count / total_tokens
                    else:
                        posting[word][document_ids[file_name]] = count / total_tokens
                else:
                    posting[word] = {document_ids[file_name]: count / total_tokens}
    
    with open(output_file, 'w') as file:
        for word, doc_weights in posting.items():
            file.write(word + ':\n')
            for doc_id, weight in doc_weights.items():
                file.write(f"    Document ID: {doc_id}, Weight: {weight}\n")

def main():
    # Take time of the process
    process_start_time = time.time()
    
    # Get paths
    main_path = os.getcwd()
    files_path = os.path.join(main_path, 'html')  # Update the path to html directory
    posting_file = os.path.join(main_path, 'results/token_posting.txt')
    output_file_times = os.path.join(main_path, 'results/times/a10_al02883272.txt')
    document_index_file = os.path.join(main_path, 'Documents.txt')  # New index file for documents
    posting_txt_file = os.path.join(main_path, 'results/posting.txt')  # Posting file for all HTML documents
    
    # Generate document IDs for all HTML files in the directory
    document_ids = {}
    with open(document_index_file, 'r') as index_file:
        for line in index_file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                document_ids[parts[1]] = parts[0]
    
    # Create posting file
    create_posting_file(files_path, posting_txt_file, document_ids)
    print('Posting file created:', posting_txt_file)
    
    # Get posting contents
    with open(posting_file, 'r', encoding='utf-8', errors='replace') as file:
        posting_content = file.read()
    posting_rows = posting_content.split('\n')
    posting_data = []
    for row in posting_rows:
        row_data = row.split(';')
        if len(row_data) < 2: continue
        document_name = row_data[0]
        if document_name in document_ids:  # Check if the document exists in the index
            doc_id = document_ids[document_name]
            posting_data.append({
                'doc_id': doc_id,  # Add doc_id to the posting data
                'file': document_name,
                'token_count': float(row_data[1])
            })
    
    process_end_time = time.time()
    print('Finished process.')
    
    # Write time result
    with open(output_file_times, 'w', encoding='utf-8', errors='replace') as file:
        file.write(f"Tiempo total de ejecución del programa: {process_end_time - process_start_time} segundos")
    
    print('Document index file created:', document_index_file)

if __name__ == '__main__':
    main()

