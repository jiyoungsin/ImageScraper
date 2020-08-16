import csv
import logging
from datetime import datetime
from google_images_download import google_images_download
from time import sleep

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


file = 'data.csv'
field_name = 'site_number'
structure_field = 'structure_name'
output_file = "./data/{}.csv".format(dateTimeObj.strftime("%m_%d_%H-%M-%S"))
number_of_images = 100
time_to_sleep = 90

with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    header = next(reader)
    site_id_index = header.index(field_name)
    structure_index = header.index(structure_field)
    for row in reader:
        try:
            site_id = row[site_id_index]
            bridge_name = row[structure_index]
            cleaned_bridge_name = bridge_name.replace(',', ' ')  # replaced commas to avoid multiple keywords when searching
            result = get_urls(cleaned_bridge_name, number_of_images)  # fetching image urls
            images = result[0][cleaned_bridge_name]  # list of image urls
            for image in images:
                write_to_file(output_file, [site_id, bridge_name, image])
        except Exception as err:
            logger.error("FAILED FOR {}: {}".format(bridge_name, err))
        sleep(time_to_sleep)
