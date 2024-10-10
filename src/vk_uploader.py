import os
import time
import vk_api
from vk_api import VkUpload
from vk_api.exceptions import AuthError, Captcha

class VKUploader:
    def __init__(self, auth_data):
        self.auth_data = auth_data
        self.vk_session = None
        self.vk = None
        self.upload = None
        self.authenticate()

    def format_metadata(self, metadata):
        return f"Filename: {metadata['filename']}\n" \
               f"Path: {metadata['path']}\n" \
               f"Size: {metadata['size']} bytes\n" \
               f"Created: {metadata['created_at']}\n" \
               f"Modified: {metadata['modified_at']}\n" \
               f"FPS: {metadata['fps']}\n" \
               f"Duration: {metadata['duration']} seconds"

    def authenticate(self):
        try:
            if 'token' in self.auth_data:
                self.vk_session = vk_api.VkApi(token=self.auth_data['token'])
                self.vk = self.vk_session.get_api()
            else:
                self.vk_session = vk_api.VkApi(
                    login=self.auth_data['login'],
                    password=self.auth_data['password'],
                    app_id=int(self.auth_data['app_id']),
                    auth_handler=self.auth_handler,
                    captcha_handler=self.captcha_handler
                )
                self.vk_session.auth()
                self.vk = self.vk_session.get_api()

            self.upload = VkUpload(self.vk_session)

            # Проверка аутентификации
            self.vk.users.get()

        except AuthError as e:
            print(f"Authentication error: {e}")
            raise
        except Captcha as captcha:
            code = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
            try:
                captcha.try_again(code)
            except Captcha as captcha:
                print(f"Captcha error: {captcha}")
                raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def auth_handler(self):
        code = input("Enter 2FA code: ")
        remember_device = True
        return code, remember_device

    def captcha_handler(self, captcha):
        key = input(f"Enter captcha code {captcha.get_url()}: ")
        return captcha.try_again(key)

    def create_playlist(self, title):
        response = self.vk.video.addAlbum(title=title)
        return response['album_id']

    def upload_video(self, file_path, album_id, name, description):
        file_size = os.path.getsize(file_path)
        start_time = time.time()
        print(f"Starting upload of {name} (Size: {file_size / (1024 * 1024):.2f} MB)")

        try:
            video = self.upload.video(
                video_file=file_path,
                album_id=album_id,
                name=name,
                description=description
            )
            end_time = time.time()
            print(f"\nUpload of {name} completed in {end_time - start_time:.2f} seconds")
            return video
        except Exception as e:
            print(f"\nError uploading {name}: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            if hasattr(e, 'error_data'):
                print(f"Error data: {e.error_data}")
            raise

