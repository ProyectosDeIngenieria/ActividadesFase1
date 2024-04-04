import time
import os
import re

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
    files_path = os.path.join(main_path, 'src/results/alphabetically')
    posting_file = os.path.join(main_path, 'src/results/token_posting.txt')
    output_posting_file = os.path.join(main_path, 'src/results/token_posting_weights.txt')
    output_file_times = os.path.join(main_path, 'src/results/times/a10_al02883272.txt')
    
    # Get posting contents
    with open(posting_file, 'r', encoding='utf-8', errors='replace') as file:
        posting_content = file.read()
    posting_rows = posting_content.split('\n')
    posting_data = []
    for row in posting_rows:
        row_data = row.split(';')
        if len(row_data) < 2: continue
        posting_data.append({
            'file': row_data[0],
            'token_count': float(row_data[1])
        })
    
    # Get the posting weights
    files_token_count: dict[str, float] = {}
    with open(output_posting_file, 'w', encoding='utf-8', errors='replace') as file:
        for index, posting in enumerate(posting_data):
            print(f'Processing row {index + 1} of {len(posting_data)} {get_loading_bar(index + 1, len(posting_data), 20)}', end='\r', flush=True)
            if posting['file'] in list(files_token_count.keys()):
                token_count = files_token_count[posting['file']]
            else:
                token_count = get_total_token_count(os.path.join(files_path, posting['file']))
                files_token_count[posting['file']] = token_count
            file.write(f"{posting['file']};{round((posting['token_count'] * 100.) / token_count, 2)}\n")
    
    process_end_time = time.time()
    print('Finished process.')
    
    # Write time result
    with open(output_file_times, 'w', encoding='utf-8', errors='replace') as file:
        file.write(f"Tiempo total de ejecución del programa: {process_end_time - process_start_time} segundos")
    
    


if __name__ == '__main__':
    main()
