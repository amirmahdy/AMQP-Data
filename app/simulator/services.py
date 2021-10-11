from datetime import datetime


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

    def write_to_csv(self, content):
        date = datetime.now()
        unix = int(datetime.now().timestamp())
        date = "-".join([str(date.year), str(date.month), str(date.day)])
        with open("media/" + date + ".csv", "a+") as output:
            output.write(f"{unix}, {content}")
            output.write("\n")
