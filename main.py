import requests
import threading
import time
import sys
import click
counter = 0

# Здесь мы извлекаем из url последнее имя - имя файла,
# далее получаем ответ на get запрос, response.iter_content - итератор, который возвращает на 1 итерацию 256 байт
# открытие контекстным менеджером для записи в файл и обновление счетчика
# запись в файл если итератор вернул не пустое значение
def download(url=""):
    name = url.split("/")[-1]
    global counter
    response = requests.get(url=url, stream=True)
    with open(str(name), mode='wb') as file:
        for i in response.iter_content(chunk_size=256):
            if i:
                counter += 256
                file.write(i)
    print(f"Successfully uploaded {counter} bytes")

# Счетчик с бесконечным циклом, слипает поток на 1 печатает значение переменной и очищает буфер вывода
def check_bytes():
    while True:
        time.sleep(1)
        print(f"Loaded: |{counter}| bytes")
        sys.stdout.flush()


# 2 декоратора нужные для работы в консольном режиме. 2 декоратор подставляет аргумент "ссылки" из консоли
# в аргумент функции
@click.command()
@click.argument("url")
def main(url):
    thread1 = threading.Thread(target=download, args=(str(url),))   # Основной поток выполнения программы
    thread2 = threading.Thread(target=check_bytes, daemon=True)     # Демон - счетчик
    thread1.start()
    thread2.start()

# Точка входа в программу
if __name__ == '__main__':
    main()








# See PyCharm help at https://www.jetbrains.com/help/pycharm/
