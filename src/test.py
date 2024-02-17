import os
import re
import time


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


def main():
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
    # Initialize list to store combined text
    combined_text = []
    total_time = 0
    # Read content of all HTML files
    for file in files:
        try:
            # Calculate time to process file
            start_time = time.time()
            text_content = get_html_file_text(os.path.join(html_path, file))
            combined_text.append(text_content)
        except Exception as e:
            print(f"Error processing {file}: {e}")
        end_time = time.time()
        execution_time = end_time - start_time
        total_time += execution_time

    # Combine all text and sort alphabetically
    combined_text = '\n'.join(combined_text)
    combined_words = sorted(re.findall(r'\b[a-zA-Z]+\b', combined_text.lower()))

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
    main()
