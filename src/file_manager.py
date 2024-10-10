import os
from datetime import datetime
from moviepy.editor import VideoFileClip

class FileManager:
    def __init__(self, root_path):
        self.root_path = root_path
        self.files_to_delete = []

    def scan_folders(self):
        folders = {}
        for root, dirs, files in os.walk(self.root_path):
            relative_path = os.path.relpath(root, self.root_path)
            if relative_path != '.':
                folders[relative_path] = [
                    os.path.join(root, file) for file in files
                    if file.lower().endswith(('.mp4', '.avi', '.mov', '.wmv'))
                ]
        return folders

    def get_file_metadata(self, file_path):
        stat = os.stat(file_path)
        clip = VideoFileClip(file_path)
        return {
            'filename': os.path.basename(file_path),
            'path': os.path.relpath(file_path, self.root_path),
            'size': stat.st_size,
            'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'fps': clip.fps,
            'duration': clip.duration,
        }

    def add_to_delete_list(self, file_path):
        self.files_to_delete.append(file_path)

    def get_delete_list(self):
        return self.files_to_delete

    def delete_uploaded_files(self):
        for file_path in self.files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
