import datetime

from alphaman.feed import DailyInstrumentData, DailyFeed, Feed


start_date = datetime.datetime(2017,1,1)
end_date = datetime.datetime(2017,2,23)
feed = Feed(start_date, end_date)
daily_feed = feed.getDailyFeed(end_date)

print daily_feed.getIsTradable()