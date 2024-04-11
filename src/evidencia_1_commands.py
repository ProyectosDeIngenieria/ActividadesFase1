import argparse
from evidencia_1_times import tokenize, index

def main():
    # Declare input parser
    parser = argparse.ArgumentParser(description='Process files to tokenize or index them')
    parser.add_argument('action', type=str, help='Process type (tokenize|index)')
    parser.add_argument('input_dir', type=str, help='Folder with the input files')
    parser.add_argument('output_dir', type=str, help='Output file')
    
    args = parser.parse_args()
    
    # Get parser input variables
    action = args.action
    input_dir = args.input_dir
    output_dir = args.output_dir
    if action != 'tokenize' and action != 'index':
        raise Exception('The action has to be "tokenize" or "index"')
    
    if action == 'tokenize':
        tokenize(
            input_path=input_dir,
            output_path=output_dir
        )
    else:
        index(
            input_path=input_dir,
            output_path=output_dir
        )

if __name__ == "__main__":
    main()
