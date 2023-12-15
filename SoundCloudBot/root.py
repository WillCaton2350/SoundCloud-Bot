from Bot.main import web_driver

if __name__ == "__main__":
    counter = 10
    func = web_driver()
    for i in range(counter):
        func.start_driver()
        func.start_browser()
        func.search_bar()
        func.artist()
        func.auto_play()
        counter +=1
    func.close_browser()