import schedule
from parse.parse import Parse
from parse.update_yaml import update_config

def main():
    tokens = Parse().run()
    if tokens:     
        try:
            update_config(tokens)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    main()
    schedule.every(10).minutes.do(main)
    while True:
        schedule.run_pending()
    