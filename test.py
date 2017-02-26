import datetime
import pandas_datareader.data as web
import pandas as pd
from alphaman.feed import DailyInstrumentData, DailyFeed, Feed


start_date = datetime.datetime(2016,1,1)
end_date = datetime.datetime(2016,12,31)

instrument = "000660"

df = web.DataReader(instrument+".KS", "yahoo", start_date, end_date)

feed = Feed(start_date, end_date)

feed.addDailyFeed(df, instrument)
feed.trimDailyFeed()
dates = feed.getTradableDates()
print dates
daily_feed = feed.getDailyFeed(0)
daily_instrument_data = daily_feed.getDailyInstrumentData(instrument)

print daily_instrument_data.getBarData()