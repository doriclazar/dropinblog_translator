from controller import Controller


if __name__ == '__main__':
    controller = Controller()
    url = input('Source article URL:')
    keyword = input('Source article keyword:')
    languages = input('Target translation languages [default=ALL]:')
    languages = languages.replace(' ', '') if languages else 'ALL'
    controller.update_file(url, keyword, languages)