import time
import os
import re
from HashTable import hashtable

def get_unique_words(file_path: str, default_hashtable: hashtable[str, int] = hashtable[str, int](379)) -> list[dict[str, any]]:
    """Get every unique word of a file.
    Args:
        file_path (str): path of the file.
        default_hashtable (hashtable[str, int]): default hashtable where unique words will be added.
    Returns:
        list[dict[str, int]]: an array with every word of the file.
    """
    # Read file content
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    separated_words = re.split('\n', content) # Separate the words of the files
    filtered_words = [word for word in separated_words if word.isalnum()] # Remove any word with special symbols
    word_hash_table = add_words_to_hash_table(default_hashtable, filtered_words) # Return every unique word
    return [{ 'word': word, 'file': file_path.split('/')[-1], 'frec': word_hash_table.get(word) } for word in word_hash_table.keys()]

def get_unique_words_hash_table(file_path: str, default_hashtable: hashtable[str, int] = hashtable[str, int](379)) -> hashtable[str, int]:
    """Get every unique word of a file.
    Args:
        file_path (str): path of the file.
        default_hashtable (hashtable[str, int]): default hashtable where unique words will be added.
    Returns:
        hashtable[str, int]: a hashtable with every word of the file.
    """
    # Read file content
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    separated_words = re.split('\n', content) # Separate the words of the files
    filtered_words = [word for word in separated_words if word.isalnum()] # Remove any word with special symbols
    return add_words_to_hash_table(default_hashtable, filtered_words) # Return every unique word

def add_words_to_hash_table(hashtable: hashtable[str, int], words: list[str]) -> hashtable[str, int]:
    """Add words to a hash table, and set word count.
    Args:
        dictionary (dict[str, int]): The dictionary that will be modified.
        words (list[str]): The words that will be added to the count.
    Returns:
        dict[str, int]: The dictionary with the new word count.
    """
    new_hash_table = hashtable.clone()
    for word in words:
        if new_hash_table.haskey(word):
            new_hash_table.add(word, new_hash_table.get(word) + 1)
        else:
            new_hash_table.add(word, 1)
    return new_hash_table

def get_loading_bar(actual_number: int, total_number: int, bar_size: int) -> str:
    """Generate a loading bar.
    Args:
        actual_number (int): Actual number of the process.
        total_number (int): Total nomber of the process.
        bar_size (int): The character length of the loading bar.
    Returns:
        str: The loading bar as a string
    """
    loading_percent = float(bar_size * actual_number) / float(total_number)
    loading_bar = '['
    for i in range(bar_size):
        loading_bar += '-' if loading_percent >= i else ' '
    return loading_bar + ']'


def tokenize(output_path: str, input_path: str = None, input_paths: list[str] = None):
    if input_path == None and input_paths == None:
        raise Exception('There is no input')
    if input_paths == None:
        files = sorted(os.listdir(input_path))
        input_paths = [os.path.join(input_path, file) for file in files]
    words_hashtable = hashtable[str, int](73369)
    for input_file in input_paths:
        words_hashtable = get_unique_words_hash_table(file_path=input_file, default_hashtable=words_hashtable)
    with open(output_path, 'w', encoding='utf-8', errors='replace') as file:
        file.write(words_hashtable.tostring())
            
def index(output_path: str, input_path: str = None, input_paths: list[str] = None):
    if input_path == None and input_paths == None:
        raise Exception('There is no input')
    if input_paths == None:
        files = sorted(os.listdir(input_path))
        input_paths = [os.path.join(input_path, file) for file in files]
    posting_records: list[dict[str, any]] = [] # list with the word in each file and the num of times they appear
    # Get the word count of each file in the doc
    for file_path in input_paths:
        file_records = get_unique_words(file_path)
        posting_records.extend(file_records)
    posting_records = sorted(posting_records, key=lambda x: x['word']) # Sort alphabetically by the word
    with open(output_path, 'w', encoding='utf-8', errors='replace') as file:
        for posting in posting_records:
            file.write(f"{posting['word']};{posting['file']};{posting['frec']}\n")
    


def main():
    # Take time of the process
    process_start_time = time.time()
    
    # Get paths
    main_path = os.getcwd()
    input_folder = os.path.join(main_path, 'src/results/alphabetically')
    output_folder = os.path.join(main_path, 'src/results/e1/')
    output_file_token_times = os.path.join(main_path, 'src/results/times/e1_token_al02883272.txt')
    output_file_index_times = os.path.join(main_path, 'src/results/times/e1_index_al02883272.txt')
    
    # Get input files
    files = sorted(os.listdir(input_folder))
    
    tokenize_times: list[dict[str, int]] = []
    index_times: list[dict[str, int]] = []
    
    for doc_quant in range(10, 51, 10):
        input_paths = [os.path.join(input_folder, file) for file in files[:doc_quant]]
        tokenize_start = time.time()
        tokenize(
            input_paths=input_paths,
            output_path=os.path.join(output_folder, f"token_{doc_quant}.txt")
        )
        index_start = time.time()
        index(
            input_paths=input_paths,
            output_path=os.path.join(output_folder, f"index_{doc_quant}.txt")
        )
        process_end = time.time()
        # Store times
        tokenize_times.append({
            'doc_quant': doc_quant,
            'time': index_start - tokenize_start
        })
        index_times.append({
            'doc_quant': doc_quant,
            'time': process_end - index_start
        })
        
    # Store time results
    with open(output_file_token_times, 'w', encoding='utf-8', errors='replace') as file:
        for tok_time in tokenize_times:
            file.write(f"Doc#: {tok_time['doc_quant']}\tTime: {tok_time['time']} sec\n")
    with open(output_file_index_times, 'w', encoding='utf-8', errors='replace') as file:
        for ind_time in index_times:
            file.write(f"Doc#: {ind_time['doc_quant']}\tTime: {ind_time['time']} sec\n")
    
    

if __name__ == "__main__":
    main()
