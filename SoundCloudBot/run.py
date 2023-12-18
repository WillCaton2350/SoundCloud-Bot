from Bot.src import web_driver
from datetime import datetime

if __name__ == "__main__":
    counter = 100
    func = web_driver()
    start_time = datetime.now()
    print(f'Start Time: {start_time.strftime("%H:%M:%S")}')
    for i in range(counter):
        func.start_driver()
        func.start_browser()
        func.auto_play()
        elapsed_time = datetime.now() - start_time
        formatted_time = str(elapsed_time).split(".")[0]
        print(f'Elapsed Time: {formatted_time}, Plays: {counter}\n')
        counter += 1
    end_time = datetime.now()
    print(f'End Time: {end_time.strftime("%H:%M:%S")}')
    func.close_browser()