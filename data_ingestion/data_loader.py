import pandas as pd
import logging

# configuring logging operations
logging.basicConfig(filename='development_logs.log', level=logging.INFO,
                    format='%(levelname)s:%(asctime)s:%(message)s')


class DataLoad:
    """ This class is used to fetch data for the training.
    Author: NAMBAKKAM ARAVIND RAKESH
    """

    def __init__(
            self, dataset):

        self.dataset = dataset

    def fetch_data(self):

        logging.info('Entered the "fetch_data" method of the "DataLoad" class.')  # logging operation

        try:
            df = pd.read_csv(self.dataset)  # reading the dataset
            logging.info(f'Data loaded successfully. Shape of the data is {df.shape}')  # logging operation
            logging.info('Exited the "fetch_data" method of the "DataLoad" class.')

            return df

        except Exception as e:
            # logging operation
            logging.error('Exception occurred in fetch_data method of the DataLoad class. Exception message:' + str(
                e))
            logging.info(
                'Data fetching unsuccessful.Exited the "fetch_data" method of the "DataLoad" class.')
