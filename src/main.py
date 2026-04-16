from pathlib import Path
import sys
import shutil
import config

"""
- finds extracted folders and deletes zip files for those folders
- places images audio documents and video in their respective folders in the
downloads folder
- places unidentified files in the unclassified_files folder
- places unidentified folders in the unclassified_folders folder

TODO list
- What to do when file to move already exists in destination (Currently, we overwrite destination)
- Dry run: Currently, script at times moves what it doesnt have to and I have to manually reset the movements
- Add wait time: Currently runs  immediately when there is a change, might delete half downloads
- Inferring file type from its contents: Currently reliant on file exensions
"""
image_extensions = '.png .jpeg .gif .img .dmg .jpg'.split()
video_extensions = '.mkv .mp4'.split()
document_extensions = '.docx .org .txt .rtf .pdf .html'.split()
audio_extensions = '.mp3 .wav .opus .m4a'.split()
software_file_extensions = '.iso .deb .appimage'.split()
db_json_csv_file_extensions = '.csv .db .json'.split()
archives_and_compressed_file_extensions = '.zip .z .rar .xz'.split()
folder_suffix = "files"
valid_folders = "images videos documents audios unclassified_files unclassified_folders archives_and_compressed_files software_files db_json_csv_files app_downloads".split()
target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/keith/Downloads")
print(len(sys.argv))


unclassified_files = []
unclassified_folders = []
images = []
videos = []
documents = []
audios = []
archives_and_compressed_files = []
software_files = []
db_json_csv_files = []

for path in target_path.iterdir():
    if path.is_dir():
        if path.stem not in valid_folders:
            print(path.stem)
            unclassified_folders.append(path)
        continue
    
    path_suffix = path.suffix.lower()
    
    if path_suffix in image_extensions:
        images.append(path)
    elif path_suffix in video_extensions:
        videos.append(path)
    elif path_suffix in audio_extensions:
        audios.append(path)
    elif path_suffix in document_extensions:
        documents.append(path)
    elif path_suffix in archives_and_compressed_file_extensions:
        archives_and_compressed_files.append(path)
    elif path_suffix in software_file_extensions:
        software_files.append(path)
    elif path_suffix in db_json_csv_file_extensions:
        db_json_csv_files.append(path)
    else:
        unclassified_files.append(path)

# Create directories if they don't exist and move files to corresponding folders
category_map = {
    'images': images,
    'videos': videos,
    'documents': documents,
    'audios': audios,
    'archives_and_compressed_files': archives_and_compressed_files,
    'software_files': software_files,
    'db_json_csv_files':db_json_csv_files,
    'unclassified_files': unclassified_files
}

for folder_name, file_list in category_map.items():
    if file_list:  # Only create folder if there are files to move
        folder_path = target_path / folder_name
        folder_path.mkdir(exist_ok=True)
        
        for file in file_list:
            file_path =  folder_path / file.name
            try:
                if file_path.exists() and config.overwrite_existing_files:
                    file_path.unlink()
                file.rename(folder_path / file.name)
                print(f"Moved: {file.name} → {folder_name}/")
            except Exception as e:
                print(f"Error moving {file.name}: {e}")

# Handle unclassified folders
if unclassified_folders:
    unclassified_folder_path = target_path / 'unclassified_folders'
    unclassified_folder_path.mkdir(exist_ok=True) # skip if exists (don't throw error)
    
    for folder in unclassified_folders:
        # Skip the newly created category folders
        if folder.name:
            try:
                # Move folder into unclassified_folders
                new_location = unclassified_folder_path / folder.name
                if new_location.exists() and config.overwrite_existing_folders:
                    shutil.rmtree(new_location)
                folder.rename(new_location)
                print(f"Moved folder: {folder.name} → unclassified_folders/")
            except Exception as e:
                print(f"Error moving folder {folder.name}: {e}")

print("\nOrganization complete!")
print(f"Images: {len(images)}")
print(f"Videos: {len(videos)}")
print(f"Documents: {len(documents)}")
print(f"Audios: {len(audios)}")
print(f"Software files: {len(software_files)}")
print(f"Db_json_csv_files: {len(db_json_csv_files)}")
print(f"Unclassified files: {len(unclassified_files)}")
print(f"Unclassified folders: {len(unclassified_folders)}")
