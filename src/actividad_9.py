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

    separated_words = re.findall(r'\b(?![a-zA-Z]*\d)\w+(?:-\w+)*\b', content) # Separate the words of the files

    word_dictionary = add_words_to_dictionary({}, separated_words) # Return every unique word
    return [{ 'word': word, 'file': file_name, 'frec': word_dictionary[word] } for word in list(word_dictionary.keys())]

def add_words_to_dictionary(dictionary: dict[str, int], words: str) -> dict[str, int]:
    """Add words to a dictionary, and set word count.
    Args:
        dictionary (dict[str, int]): The dictionary that will be modified.
        words (str): The words that will be added to the count.
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

def filter_words(word_dict: dict[str, int], stop_list_path: str) -> dict[str, int]:
    """Filter out words based on stop list, frequency, and length criteria.
    Args:
        word_dict (dict[str, int]): Dictionary containing words and their frequencies.
        stop_list_path (str): Path to the stop list file.
    Returns:
        dict[str, int]: Filtered dictionary.
    """
    # Read stop list
    with open(stop_list_path, 'r', encoding='utf-8') as stop_file:
        stop_list = stop_file.read().splitlines()

    # Filter words
    filtered_dict = {}
    for word, freq in word_dict.items():
        if word not in stop_list and freq >= 2 and not len(word) == 1:
            filtered_dict[word] = freq
    return filtered_dict

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
    output_file_times = os.path.join(main_path, 'src/results/times/a9_al02870266.txt')
    output_file_filtered = os.path.join(main_path, 'src/results/words_filtered.txt')
    stop_list_path = os.path.join(main_path, 'src/results/stop_list.txt')
    
    # Get input files
    files = sorted(os.listdir(input_path))
    
    doc_dictionary = {} # dictionary with the words and the num of documents they appear
    posting_records: list[dict[str, any]] = [] # list with the word in each file and the num of times they appear
    file_times_records: list[dict[str, any]] = [] # list with the time it took to process each file
    
    # Get the word count of each file in the doc
    for index, file in enumerate(files):
        print(f'Processing file {index + 1} of {len(files)} {get_loading_bar(index + 1, len(files), 20)}', end='\r', flush=True)
        file_start_time = time.time() # Start to take time
        file_records = get_unique_words(input_path, file)
        file_words = map(lambda x: x['word'], file_records)
        doc_dictionary = add_words_to_dictionary(doc_dictionary, file_words)
        posting_records.extend(file_records)
        file_end_time = time.time() # Finish to take time
        file_times_records.append({
            'file': file,
            'time': file_end_time - file_start_time
        })
            
    # Filter words
    filtered_dictionary = filter_words(doc_dictionary, stop_list_path)
    
    # Create token document records from dictionary
    doc_records: list[dict[str, any]] = []
    posting_sum = 0
    for word in sorted(list(filtered_dictionary.keys())):
        doc_records.append({
            'word': word,
            '#doc': filtered_dictionary[word],
            'posting': posting_sum
        })
        posting_sum += filtered_dictionary[word]
        
    # Sort alphabetically by the word
    posting_records = sorted(posting_records, key=lambda x: x['word']) 
    
    process_end_time = time.time()
    print('Finished process.')
    
    # Write filtered words to file
    with open(output_file_filtered, 'w', encoding='utf-8', errors='replace') as file:
        for word, freq in filtered_dictionary.items():
            file.write(f"{word};{freq}\n")
    
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