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
    html_path = os.path.join(main_path, 'src/html')
    result_path = os.path.join(main_path, 'src/results/texts')
    time_result_path = os.path.join(main_path, 'src/results/times', 'a2_al02883272.txt')
    # Get files names
    files = sorted(os.listdir(html_path))
    # For each file create a new one without 
    with open(time_result_path, 'w', encoding='utf-8') as f:
        total_time = 0
        for file in files:
            try:
                # Calculate time to open file
                start_time = time.time()
                content = get_html_file_text(os.path.join(html_path, file))
                # Write the content in a new .txt file
                with open(os.path.join(result_path, re.sub(r'\.[^.]+$', '.txt', file)), 'w', encoding='utf-8') as file_result:
                    file_result.write(content)
            except:
                pass
            end_time = time.time()
            execution_time = end_time - start_time
            # Write the time in the file
            f.write(f"{file}\t\t\t{execution_time:.20f}\n")
            total_time += execution_time
        # Write the total time in the file
        f.write(f"\n\nTiempo total en abrir todos los archivos: {total_time:.20f} segundos")
        process_end_time = time.time()
        f.write(f"\n\nTiempo total de ejecución: {(process_end_time - process_start_time):.20f} segundos")

if __name__ == '__main__':
    main()