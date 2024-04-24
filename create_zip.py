import zipfile
import os

def create_zip_archive():
    # List of files and directories to include in the ZIP archive
    files_to_zip = ['Analysis.py']
    pandas_dir = 'C:/Users/rmart/AppData/Local/Programs/Python/Python311/Lib/site-packages/pandas'
    pandas_dist_info = 'C:/Users/rmart/AppData/Local/Programs/Python/Python311/Lib/site-packages/pandas-2.2.2.dist-info'

    # Path to the ZIP file to create
    zip_file_path = 'lambda_function.zip'

    # Create a new ZIP archive
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        # Add Analysis.py to the ZIP archive
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
            else:
                print(f"Warning: File '{file}' not found.")

        # Add pandas library files to the ZIP archive
        if os.path.exists(pandas_dir):
            for root, dirs, files in os.walk(pandas_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, pandas_dir))

        # Add pandas dist-info directory to the ZIP archive
        if os.path.exists(pandas_dist_info):
            for root, dirs, files in os.walk(pandas_dist_info):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, pandas_dist_info))

    print(f"ZIP archive '{zip_file_path}' created successfully.")

if __name__ == "__main__":
    create_zip_archive()
