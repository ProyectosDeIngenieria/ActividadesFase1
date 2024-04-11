import time
import os
import re

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
    separated_words = re.split('\n', content) # Separate the words of the files
    filtered_words = [word for word in separated_words if word.isalnum()] # Remove any word with special symbols
    word_dictionary = add_words_to_dictionary({}, filtered_words) # Return every unique word
    # return word_dictionary
    return [{ 'word': word, 'file': file_name, 'frec': word_dictionary[word] } for word in list(word_dictionary.keys())]

def add_words_to_dictionary(dictionary: dict[str, int], words: list[str]) -> dict[str, int]:
    """Add words to a dictionary, and set word count.
    Args:
        dictionary (dict[str, int]): The dictionary that will be modified.
        words (list[str]): The words that will be added to the count.
    Returns:
        dict[str, int]: The dictionary with the new word count.
    """
    new_dictionary = dictionary.copy()
    dictionary_words = list(dictionary.keys())
    for word in words:
        if word in dictionary_words:
            new_dictionary[word] = new_dictionary[word] + 1
        else:
            new_dictionary[word] = 1
            dictionary_words.append(word)
    return new_dictionary

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
    


def main():
    # Take time of the process
    process_start_time = time.time()
    
    # Get paths
    main_path = os.getcwd()
    input_path = os.path.join(main_path, 'src/results/alphabetically')
    output_file_dictionary = os.path.join(main_path, 'src/results/token_dictionary.txt')
    output_file_posting = os.path.join(main_path, 'src/results/token_posting.txt')
    output_file_times = os.path.join(main_path, 'src/results/times/a7_al02883272.txt')
    
    # Get input files
    files = sorted(os.listdir(input_path))
    
    posting_records: list[dict[str, any]] = [] # list with the word in each file and the num of times they appear
    file_times_records: list[dict[str, any]] = [] # list with the time it took to process each file
    # Get the word count of each file in the doc
    for index, file in enumerate(files):
        print(f'Processing file {index + 1} of {len(files)} {get_loading_bar(index + 1, len(files), 20)}', end='\r', flush=True)
        file_start_time = time.time() # Start to take time
        
        file_records = get_unique_words(input_path, file)
        
        posting_records.extend(file_records)
        file_end_time = time.time() # Finish to take time
        file_times_records.append({
            'file': file,
            'time': file_end_time - file_start_time
        })
        
    # Sort alphabetically by the word
    posting_records = sorted(posting_records, key=lambda x: x['word']) 
    
    # Create token document records from posting records
    doc_records: list[dict[str, any]] = []
    last_posting_word = ''
    posting_num = 0
    for posting_row in posting_records:
        if posting_row['word'] != last_posting_word:
            last_posting_word = posting_row['word']
            doc_records.append({
                'word': last_posting_word,
                '#doc': 1,
                'posting': posting_num
            })
        else:
            doc_records[-1]['#doc'] += 1
        posting_num += 1
    
    process_end_time = time.time()
    print('\nFinished process.')
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
    

if __name__ == '__main__':
    main()
