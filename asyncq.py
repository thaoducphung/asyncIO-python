import asyncio
import itertools as it
import os
import random
import time

async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()

async def randsleep(a: int = 1, b: int = 5, caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)

async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")

async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()

async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    producers = [loop.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [loop.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()
    # asyncio.run(main(**ns.__dict__))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(**ns.__dict__))

    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")

# import pandas as pd 
# import datetime
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# df = pd.read_csv(r'D:\Cocoon\DataSQL\result\userUpdates\userUpdates.csv')
# print(df.head())

# years_fmt = mdates.DateFormatter('%d-%m')
# fig, ax = plt.subplots()
# # format the ticks
# # ax.xaxis.set_major_locator(years)
# ax.xaxis.set_major_formatter(years_fmt)
# # ax.xaxis.set_minor_locator(months)

# numdays = 7
# base = datetime.datetime.today()
# date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
# print(date_list)

# from dateutil.rrule import rrule, MONTHLY,WEEKLY
# from datetime import datetime
# start_date = datetime(2014, 12, 31)
# a = list(rrule(freq=MONTHLY, count=4, dtstart=start_date))
# print(a)


# import datetime
# import isoweek 
# import random
# import matplotlib.dates as mdates
# myFmt = mdates.DateFormatter('%d-%m')
# ax.xaxis.set_major_formatter(myFmt)

# def get_start_and_end_date_from_calendar_week(year, calendar_week):       
#     return [datetime.datetime.strptime(f'{year}-{week}-1', "%Y-%W-%w").date() for week in [calendar_week,isoweek.Week.last_week_of_year(year).week]]
    
# start_date = get_start_and_end_date_from_calendar_week(2020,1)
# print(start_date)
# x = list(rrule(freq=WEEKLY, dtstart=start_date[0],until=start_date[1]))
# print(x)
# y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

# plt.bar(x,y)
# plt.xlim(pd.Timestamp('2020-01-01'), pd.Timestamp('2020-12-31'))

# # Format the date into months & days
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) 
# # lims = [(np.datetime64('2005-02'), np.datetime64('2005-04')),
# #         (np.datetime64('2005-02-03'), np.datetime64('2005-02-15')),
# #         (np.datetime64('2005-02-03 11:00'), np.datetime64('2005-02-04 13:20'))]
# # # Change the tick interval
# # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
# # Ensure a major tick for each week using (interval=1) 

# plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
# plt.xticks(x[::4])
# # # Ensure a major tick for each week using (interval=1) 
# # ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

# # Puts x-axis labels on an angle
# # plt.gca().xaxis.set_tick_params(rotation = 30) 
# #rotates the tick labels automatically
# fig.autofmt_xdate()

# plt.xlabel('Date - Week Starting')
# plt.show()