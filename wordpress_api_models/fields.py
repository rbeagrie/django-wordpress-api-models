import json_models
import iso8601
from datetime import datetime

class DateField(json_models.DateField):

    def parse(self, json_data):
        date_string = self._parse(json_data)
        date_object = iso8601.parse_date( date_string )
        milliseconds_from_epoch = int(date_object.strftime("%s"))
        return date_object
        #return milliseconds_from_epoch and datetime.utcfromtimestamp(milliseconds_from_epoch / 1000.0) or None

