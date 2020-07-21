import csv
import logging
from datetime import datetime
from google_images_download import google_images_download


logger = logging.getLogger("imagescraper-bot")
logger.setLevel(level=logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
dateTimeObj = datetime.now()
file_handler = logging.FileHandler("./logs/{}.txt".format(dateTimeObj.strftime("%m_%d_%H-%M-%S")))
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)
logger.info("@@@@@@@@@@@ NEW INSTANCE @@@@@@@@@@")


def get_urls(keyword, limit=1):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keyword,
        "limit": limit,
        "no_download": True
    }
    return response.download(arguments)


def write_to_file(output_file, data):
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)


file = 'bridge_data_sample.csv'
field_name = 'structure_name'
output_file = 'result.csv'
number_of_images = 5

with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    header = next(reader)
    index = header.index(field_name)
    for row in reader:
        try:
            bridge_name = row[index]
            cleaned_bridge_name = bridge_name.replace(',', ' ')  # replaced commas to avoid multiple keywords when searching
            result = get_urls(cleaned_bridge_name, number_of_images)  # fetching image urls
            images = result[0][cleaned_bridge_name]  # list of image urls
            for image in images:
                write_to_file(output_file, [bridge_name, image])
        except Exception as err:
            logger.error("FAILED FOR {}: {}".format(row[index], err))
