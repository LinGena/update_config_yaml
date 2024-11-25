import schedule
from parse.parse import Parse
from parse.update_yaml import update_config
import subprocess


def main():
    tokens = Parse().run()
    if tokens:     
        try:
            update_config(tokens)
            subprocess.run(["sudo", "systemctl", "restart", "tenderduty"], check=True)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    main()
    schedule.every(3).seconds.do(main)
    while True:
        schedule.run_pending()
