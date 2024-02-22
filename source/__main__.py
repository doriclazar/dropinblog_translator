import logging
from controller import Controller


if __name__ == '__main__':
    controller = Controller(data_path='C:\\Users\doric\\blog_posts\\')
    controller.update_file()