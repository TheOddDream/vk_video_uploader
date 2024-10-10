# VK Video Uploader

Это утилита для загрузки видео в плейлисты ВКонтакте. Она сканирует указанную папку на наличие подпапок с видеофайлами, создает плейлисты в ВК и загружает видео в соответствующие плейлисты.

## Требования

- Python 3.7+
- Windows, macOS, Linux

## Установка

1. Клонируйте репозиторий:
  

```
git clone https://github.com/your-username/vk-video-uploader.git

cd vk-video-uploader
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

## Настройка

1. Получите токен доступа ВКонтакте:
   - Перейдите по ссылке [https://vkhost.github.io/](https://vkhost.github.io/)
   - Выберите вкладку "KateMobile"
   - Следуйте инструкциям для получения токена
   - Скопируйте полученный токен

2. Скопируйте файл `.env.template` и переименуйте копию в `.env`:
   ```
   cp .env.template .env
   ```

3. Откройте файл `.env` и вставьте ваш токен доступа:
   ```
   VK_ACCESS_TOKEN=ваш_токен_доступа
   ```

Если вы не хотите сохранять токен в файле, вы можете оставить это поле пустым и вводить токен при каждом запуске программы.

## Использование

1. Запустите скрипт:

```
python src/main.py
```

2. Следуйте инструкциям в командной строке:
   - Введите токен доступа (если не указан в .env)
   - Укажите путь к папке с подпапками с видео
   - Подтвердите загрузку
   - После завершения загрузки, вам будет предложено удалить загруженные файлы

Примечания

- Убедитесь, что у вас есть необходимые разрешения для работы с видео в вашем приложении ВКонтакте.
- Загрузка больших видеофайлов может занять значительное время.