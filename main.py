import time

from schedule import Schedule
from bot import Bot

def main():
    schedule = Schedule()
    schedule.setCurrentWeek()
    bot = Bot(schedule)

    while True:
        schedule.readingSheets()
        updateDays = schedule.checkUpdate()
        if schedule.isFirstLaunch:
            schedule.isFirstLaunch = False
        elif updateDays:
            bot.sendMessage(updateDays)
        if not bot.isPostedSchedule:
            bot.posting()
        schedule.resetToZeroUpdateDays()
        time.sleep(600)

if __name__ == '__main__':
    main()