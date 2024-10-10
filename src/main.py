import os
import time
from file_manager import FileManager
from vk_uploader import VKUploader
from vk_api.exceptions import AuthError, Captcha, ApiError
import vk_api
from config import VK_ACCESS_TOKEN

def get_access_token():
    if VK_ACCESS_TOKEN:
        return VK_ACCESS_TOKEN
    return input("Enter your VK access token: ")

def get_video_folder_path():
    while True:
        path = input("Enter the path to the folder with videos: ")
        if os.path.isdir(path):
            return path
        print("Invalid path. Please enter a valid directory path.")

def confirm_upload(folders):
    print("\nFound the following folders and videos:")
    for folder, videos in folders.items():
        print(f"\nFolder: {folder}")
        for video in videos:
            print(f"  - {os.path.basename(video)}")

    while True:
        confirm = input("\nDo you want to proceed with the upload? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            return False
        print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    vk_uploader = None
    while True:
        try:
            token = get_access_token()
            vk_uploader = VKUploader({'token': token})
            print("Authentication successful!")
            break
        except AuthError as e:
            print(f"Authentication failed: {e}")
        except Captcha as captcha:
            print(f"Captcha required: {captcha.get_url()}")
        except ApiError as e:
            print(f"VK API error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        retry = input("Do you want to try again? (yes/no): ").lower()
        if retry not in ['yes', 'y']:
            return

    if not vk_uploader:
        print("Failed to authenticate. Exiting.")
        return

    root_path = get_video_folder_path()
    file_manager = FileManager(root_path)

    folders = file_manager.scan_folders()

    if not folders:
        print("No video folders found. Exiting.")
        return

    if not confirm_upload(folders):
        print("Upload cancelled.")
        return

    total_start_time = time.time()
    total_uploaded = 0
    total_failed = 0

    for folder, videos in folders.items():
        print(f"\nProcessing folder: {folder}")
        try:
            album_id = vk_uploader.create_playlist(folder)
            print(f"Created playlist: {folder}")
        except Exception as e:
            print(f"Error creating playlist {folder}: {str(e)}")
            continue

        for video_path in videos:
            try:
                metadata = file_manager.get_file_metadata(video_path)
                description = vk_uploader.format_metadata(metadata)

                print(f"\nStarting upload of {metadata['filename']}...")
                video = vk_uploader.upload_video(
                    file_path=video_path,
                    album_id=album_id,
                    name=metadata['filename'],
                    description=description
                )
                print(f"Successfully uploaded: {metadata['filename']}")
                file_manager.add_to_delete_list(video_path)
                total_uploaded += 1
            except ApiError as e:
                print(f"VK API Error when uploading {metadata['filename']}: {e}")
                total_failed += 1
            except Exception as e:
                print(f"Unexpected error when uploading {metadata['filename']}: {e}")
                total_failed += 1

    total_end_time = time.time()
    total_time = total_end_time - total_start_time

    print(f"\nUpload process completed in {total_time:.2f} seconds.")
    print(f"Total videos uploaded: {total_uploaded}")
    print(f"Total videos failed: {total_failed}")

    print("\nUploaded files (to be deleted):")
    for file in file_manager.get_delete_list():
        print(file)

    if file_manager.get_delete_list():
        confirm_delete = input("Do you want to delete uploaded files? (yes/no): ").lower()
        if confirm_delete in ['yes', 'y']:
            file_manager.delete_uploaded_files()
        else:
            print("Files were not deleted.")

if __name__ == "__main__":
    main()
