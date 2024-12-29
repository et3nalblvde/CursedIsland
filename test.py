import os

def count_lines_in_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except (UnicodeDecodeError, FileNotFoundError):

        return 0

def count_lines_in_directory(directory):

    total_lines = 0

    for root, dirs, files in os.walk(directory):

        if '.venv' in dirs:
            dirs.remove('.venv')

        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith('.py'):
                total_lines += count_lines_in_file(file_path)

    return total_lines

directory = '.'
total_lines = count_lines_in_directory(directory)
print(f"Общее количество строк в Python-файлах: {total_lines}")
