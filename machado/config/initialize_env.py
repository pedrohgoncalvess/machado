import os
import shutil
from importlib import resources


def main(migration_path: str) -> None:
    current_dir = os.path.abspath('.')
    project_name = os.path.basename(current_dir)
    
    config_file = os.path.join(current_dir, 'machado.conf')
    
    if os.path.exists(config_file):
        raise FileExistsError("Config file already exists.")
    
    try:
        with resources.path('machado.templates', 'machado.conf') as config_template:
            shutil.copy2(str(config_template), config_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Template file 'machado.conf' not found in package. "
            "Please ensure the file exists in the machado/templates directory."
        )
    
    migration_dir = os.path.join(migration_path, 'migration')
    
    if os.path.exists(migration_dir):
        raise FileExistsError("Migration directory already exists.")
    
    os.makedirs(migration_dir)
    
    try:
        with open(config_file, 'r') as file:
            file_content = file.read()
        
        file_content = file_content.replace("$project_name$", project_name)
        file_content = file_content.replace("$migration_path$", migration_dir)
        
        with open(config_file, 'w') as file:
            file.write(file_content)
            
        print(f"Configuration file created at")
        print(f"Migration directory created at")
            
    except Exception as e:
        if os.path.exists(config_file):
            os.remove(config_file)
        if os.path.exists(migration_dir):
            shutil.rmtree(migration_dir)
        raise e