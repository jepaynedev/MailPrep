import argparse
import glob
import os.path
import subprocess


def run_pyside2_uic(input_dir, output_dir):
    # Validate arguments
    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f'{input_dir} is not a valid directory')
    if not os.path.isdir(output_dir):
        raise NotADirectoryError(f'{output_dir} is not a valid directory')

    for path in glob.glob(os.path.join(input_dir, '*.ui')):
        result = subprocess.run(['pyside2-uic', path], capture_output=True)
        output_path = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(path))[0]}_ui.py')
        with open(output_path, 'w', newline='') as output_file:
            data = result.stdout.decode()
            output_file.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Directory containing source *.ui files', type=str)
    parser.add_argument('output_dir', help='Directory output *_ui.py files will be written to', type=str)
    args = parser.parse_args()

    run_pyside2_uic(args.input_dir, args.output_dir)
