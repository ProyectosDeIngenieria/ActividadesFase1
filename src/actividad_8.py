import os
import re
import time

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            self.collisions += 1
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (k, value)
                    break
            else:
                self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def update(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (k, value)
                    break

def get_unique_words(folder_path: str, file_name: str) -> list[dict[str, any]]:
    """Get every unique word of a file.
    Args:
        folder_path (str): path of the folder where the file is.
        file_name (str): name of the file.
    Returns:
        dict[str, int]: an array with every word of the file.
    """
    # Read file content
    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    separated_words = re.split('[\n|,| |.|:|;|(|)]', content)  # Separate the words of the files
    filtered_words = [word for word in separated_words if word.isalnum()]  # Remove any word with special symbols
    word_dictionary = HashTable(10000)  # Initialize a new HashTable instance
    add_words_to_dictionary(word_dictionary, filtered_words)  # Add words to the HashTable
    return [{'word': word[0], 'file': file_name, 'frec': word[1]} for word_list in word_dictionary.table if word_list for word in word_list if word and len(word) >= 2]

def add_words_to_dictionary(dictionary: HashTable, words: list[str]) -> None:
    """Add words to a dictionary, and set word count.
    Args:
        dictionary (HashTable): The hash table that will be modified.
        words (list[str]): The words that will be added to the count.
    Returns:
        None
    """
    for word in words:
        if dictionary.search(word):
            dictionary.update(word, dictionary.search(word) + 1)
        else:
            dictionary.insert(word, 1)

def save_hash_table_to_file(hash_table: HashTable, file_path: str) -> None:
    """Save the hash table to a file.
    Args:
        hash_table (HashTable): The hash table to save.
        file_path (str): The path to the file where the hash table will be saved.
    Returns:
        None
    """
    with open(file_path, 'w', encoding='utf-8', errors='replace') as file:
        for index, item in enumerate(hash_table.table):
            file.write(f"Index {index}:\n")
            if item is not None:
                for key, value in item:
                    file.write(f"    {key}: {value}\n")
            file.write('\n')
        file.write(f"Total Collisions: {hash_table.collisions}\n")

def main():
    # Take time of the process
    process_start_time = time.time()
    
    # Get paths
    main_path = os.getcwd()
    input_path = os.path.join(main_path, 'results/alphabetically')
    output_file_dictionary = os.path.join(main_path, 'results/token_dictionary.txt')
    output_file_posting = os.path.join(main_path, 'results/token_posting.txt')
    output_file_times = os.path.join(main_path, 'results/times/a8_al02976943.txt')
    output_file_hash_table = os.path.join(main_path, 'results/hash_table.txt')
    
    # Get input files
    files = sorted(os.listdir(input_path))
    
    doc_dictionary = HashTable(10000) # dictionary with the words and the num of documents they appear
    posting_records: list[dict[str, any]] = [] # list with the word in each file and the num of times they appear
    file_times_records: list[dict[str, any]] = [] # list with the time it took to process each file
    # Get the word count of each file in the doc
    for index, file in enumerate(files):
        print(f'Processing file {index + 1} of {len(files)}', end='\r', flush=True)
        file_start_time = time.time() # Start to take time
        file_records = get_unique_words(input_path, file)
        file_words = map(lambda x: x['word'], file_records)
        add_words_to_dictionary(doc_dictionary, file_words)
        posting_records.extend(file_records)
        file_end_time = time.time() # Finish to take time
        file_times_records.append({
            'file': file,
            'time': file_end_time - file_start_time
        })
            
    # Create token document records from dictionary
    doc_records: list[dict[str, any]] = []
    posting_sum = 0
    for word_list in doc_dictionary.table:
        if word_list:
            for word in word_list:
                doc_records.append({
                    'word': word[0],
                    '#doc': word[1],
                    'posting': posting_sum
                })
                posting_sum += word[1]
        
    # Sort alphabetically by the word
    posting_records = sorted(posting_records, key=lambda x: x['word']) 
    
    process_end_time = time.time()
    print('Finished process.')
    # Write results in files
    with open(output_file_dictionary, 'w', encoding='utf-8', errors='replace') as file:
        for record in doc_records:
            file.write(f"{record['word']};{record['#doc']};{record['posting']}\n")
    with open(output_file_posting, 'w', encoding='utf-8', errors='replace') as file:
        for record in posting_records:
            file.write(f"{record['file']};{record['frec']}\n")
    with open(output_file_times, 'w', encoding='utf-8', errors='replace') as file:
        for record in file_times_records:
            file.write(f"{record['file']}\t{record['time']}\n")
        file.write(f"Tiempo total de ejecución del programa: {process_end_time - process_start_time} segundos")

    # Save hash table to file
    save_hash_table_to_file(doc_dictionary, output_file_hash_table)

if __name__ == '__main__':
    main()
