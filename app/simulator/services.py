from datetime import datetime
import pytz
from mobility.settings import TIME_ZONE


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if "Instance" not in instances:
            instances["Instance"] = class_(*args, **kwargs)
        return instances["Instance"]

    return get_instance


@singleton
class ToCSV:
    __shared_instance = None
    LCL = pytz.timezone(TIME_ZONE)

    def write_to_csv(self, content):
        date = datetime.now(self.LCL)
        unix = int(datetime.now(self.LCL).timestamp())
        date = "-".join([str(date.year), str(date.month), str(date.day)])
        with open("media/" + date + ".csv", "a+") as output:
            output.write(f"{unix}, {content}")
            output.write("\n")
