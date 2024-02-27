import os
import time

"""Funcion para abrir un archivo html y leerlo"""
def open_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file.read()

"""Funcion que es un loop que abre todos los archivos html y los lee"""   
def loop_through_html_files():
    process_start_time = time.time()
    main_path = os.getcwd()
    full_path = os.path.join(main_path, 'src/html')
    result_path = os.path.join(main_path, 'src/results/times', 'a1_al02883272.txt')
    # Obtener todos los archivos
    files = sorted(os.listdir(full_path))
    with open(result_path, 'w', encoding='utf-8') as f:
        total_time = 0
        for file in files:
            print(f"Se encontraron {file} archivos")
            # Medir tiempo de abrir el archivo
            start_time = time.time()
            try:
                open_file(os.path.join(full_path, file)) # Abrimos el archivo
            except UnicodeDecodeError:
                f.write(f"{file}\t\t\tNo se pudo leer el archivo ARCHIVO CORRUPTO\n")
            end_time = time.time()
            execution_time = end_time - start_time
            f.write(f"{file}\t\t\t{execution_time:.20f}\n")
            total_time += execution_time
        f.write(f"\n\nTiempo total en abrir todos los archivos: {total_time:.20f} segundos")
        process_end_time = time.time()
        f.write(f"\n\nTiempo total de ejecución: {(process_end_time - process_start_time):.20f} segundos")

if __name__ == "__main__":
    loop_through_html_files()