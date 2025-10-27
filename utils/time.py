from datetime import datetime
from datetime import timedelta

class DateWindow:
    @staticmethod
    def today():
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = datetime.now()
        return {
            'start_time': start_time,
            'end_time': end_time
        }

    @staticmethod
    def yesterday ():
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        return {
            'start_time': start_time,
            'end_time': end_time
        }
    
    @staticmethod
    def month ():
        start_time = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_time = datetime.now()
        return {
            'start_time': start_time,
            'end_time': end_time
        }
        
    @staticmethod
    def year ():
        start_time = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_time = datetime.now()
        return {
            'start_time': start_time,
            'end_time': end_time
        }
    