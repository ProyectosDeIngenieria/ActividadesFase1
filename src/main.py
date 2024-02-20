import os
import re
import time
import sys

def get_html_file_text(file_path: str) -> str:
    """Gets the content of an html file without the tags
    Args:
        file_path (str): Path to the html file.
    Raises:
        Exception: The path does not lead to an html file.
    Returns:
        str: The contents of the html file without the tags.
    """
    if not file_path.endswith('.html'):
        raise Exception('File must be html')
    # Read file contents
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    text_content = re.sub(r'<(\S?\d+)[^>]>(.?)|<.*?\>', '', content, flags=re.S)
    return text_content


def order_words(file_path: str) -> list:
    """Orders the words alphabetically from the text content of an html file
    Args:
        file_path (str): Path to the html file.
    Raises:
        Exception: The path does not lead to an html file.
    Returns:
        list: List of words ordered alphabetically.
    """
    text_content = get_html_file_text(file_path)
    # Split the content into words
    words = text_content.split()
    # Order the words alphabetically
    words.sort()
    return words

def validate_paths(input_directory: str, output_directory: str):
    if not os.path.exists(input_directory):
        raise Exception('La carpeta de entrada no existe')
    if not os.path.exists(output_directory):
        print('La carpeta de salida no existe, se creará una nueva')
        os.makedirs(output_directory)   

def main(input_directory, output_directory):
    validate_paths(input_directory, output_directory)
    
    process_start_time = time.time()
    # Generate folder path
    main_path = os.getcwd()
    html_path = os.path.join(main_path, 'html')
    result_path = os.path.join(main_path, 'results')
    alphabetically = os.path.join(main_path, 'alphabetically')
    # Ensure 'alphabetically' directory exists
    if not os.path.exists(alphabetically):
        os.makedirs(alphabetically)
    # Get files names
    files = sorted(os.listdir(html_path))
    # For each file create a new one with the words ordered alphabetically
    combined_words = []
    total_time = 0
    for file in files:
        try:
            # Calculate time to process file
            start_time = time.time()
            words_file = order_words(os.path.join(html_path, file))
            combined_words.extend(words_file)
        except Exception as e:
            print(f"Error processing {file}: {e}")
        end_time = time.time()
        execution_time = end_time - start_time
        total_time += execution_time

    # Write combined words to a single file
    combined_file_path = os.path.join(alphabetically, 'combined.txt')
    with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
        combined_file.write('\n'.join(combined_words))

    # Write the total processing time
    with open(combined_file_path, 'a', encoding='utf-8') as combined_file:
        combined_file.write(f"\n\nTotal time to process all files: {total_time:.20f} seconds")
        process_end_time = time.time()
        combined_file.write(f"\n\nTotal execution time: {(process_end_time - process_start_time):.20f} seconds")

    print("Proceso completado. Se ha creado el archivo combined.txt en la carpeta 'alphabetically'.")


if __name__ == '__main__':
    arg_names = ['input_directory', 'output_directory']
    args = dict(zip(arg_names, sys.argv[1:]))

    if (len(args) != 2):
        print("Se requieren dos argumentos: input_directory y output_directory.")
        sys.exit(1)

    input_directory = str(args['input_directory'])
    output_directory = str(args['output_directory'])    
    main(input_directory, output_directory)