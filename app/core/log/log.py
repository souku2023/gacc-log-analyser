# app/models/log.py

import pandas as pd
from app._base.base_class import BaseClass
from app.utils.logger import Logger

log = Logger(__name__)

class Log(BaseClass):

    def __init__(self, file_path):
        super().__init__()  # Initialize BaseClass
        """
        Initializes the Log object by loading and parsing the log file.
        """
        self.__file_path = file_path
        self.__master_df = self.__load_log_file()
        self.__mission_info_df = self.__get_logs_by_type('MISSION_INFO', drop_first_row=True).reset_index(drop=True)
        self.__spray_info_df = self.__get_logs_by_type('SPRAY_INFO', drop_first_row=True).reset_index(drop=True)

        # Process data frames
        self.__process_mission_info()
        self.__process_spray_info()

        # Add location info to spray_info_df
        self.__add_location_info_to_spray_dataframe()

    def __load_log_file(self):
        """
        Reads and parses the log file into a master DataFrame.
        """
        try:
            # Read the file line by line
            with open(self.__file_path, 'r') as file:
                lines = file.readlines()

            # Prepare lists to store each column
            timestamps = []
            modules = []
            severities = []
            log_types = []
            log_infos = []

            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue

                # Split the line into at most 5 parts
                parts = line.strip().split(',', 4)

                # Ensure the line has at least 4 commas
                if len(parts) >= 4:
                    timestamp = parts[0].strip()
                    module = parts[1].strip()
                    severity = parts[2].strip()
                    log_type = parts[3].strip()
                    log_info = parts[4].strip() if len(parts) > 4 else ''

                    timestamps.append(timestamp)
                    modules.append(module)
                    severities.append(severity)
                    log_types.append(log_type)
                    log_infos.append(log_info)
                else:
                    # Handle lines that don't match the expected format
                    continue

            # Create the DataFrame
            data = {
                'timestamp': timestamps,
                'module': modules,
                'severity': severities,
                'log_type': log_types,
                'log_info': log_infos
            }

            df = pd.DataFrame(data)
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            return df.reset_index(drop=True)

        except Exception as e:
            log.e(f"Error loading log file: {e}")
            return pd.DataFrame(columns=['timestamp', 'module', 'severity', 'log_type', 'log_info'])

    def __get_logs_by_type(self, log_type: str, drop_first_row: bool = False):
        """
        Returns a DataFrame filtered by log_type.

        Parameters:
            log_type (str): The type of log to filter.
            drop_first_row (bool): If True, drops the first row of the DataFrame.
        """
        if self.__master_df is not None:
            df = self.__master_df[self.__master_df['log_type'] == log_type].copy()
            if drop_first_row and not df.empty:
                # Drop the first row
                df = df.iloc[1:].reset_index(drop=True)
            return df.reset_index(drop=True)
        else:
            return pd.DataFrame()

    def __process_mission_info(self):
        """
        Processes the `MISSION_INFO` logs by splitting `log_info` into separate
        columns and retaining only rows that meet specified conditions.
        """
        if not self.__mission_info_df.empty:
            mission_info_columns = [
                'flight_mode', 'arm_status', 'flight_status',
                'height', 'speed', 'climb_rate', 'heading', 'latitude',
                'longitude'
            ]

            # Split 'log_info' into columns
            self.__mission_info_df[mission_info_columns] = \
                self.__mission_info_df['log_info'].str.split(',', expand=True)

            # Strip whitespace from new columns
            for col in mission_info_columns:
                self.__mission_info_df[col] = \
                    self.__mission_info_df[col].str.strip()

            # Convert numeric columns
            numeric_columns = [
                'height', 'speed', 'climb_rate', 'heading', 'latitude',
                'longitude'
            ]
            for col in numeric_columns:
                self.__mission_info_df[col] = pd.to_numeric(self.__mission_info_df[col], errors='coerce')

            # Apply filtering conditions
            self.__mission_info_df = self.__mission_info_df[
                (self.__mission_info_df['height'] != -100.0) &
                (self.__mission_info_df['speed'] != -100.0) &
                (self.__mission_info_df['climb_rate'] != -100.0) &
                (self.__mission_info_df['heading'] != -100.0) &
                (self.__mission_info_df['latitude'] != -200) &
                (self.__mission_info_df['longitude'] != -200)
            ]

            # Drop 'log_info' column after parsing and reset index
            self.__mission_info_df = self.__mission_info_df.drop(columns=['log_info']).reset_index(drop=True)
        else:
            log.w("No MISSION_INFO logs to process.")

    def __process_spray_info(self):
        """
        Processes the `SPRAY_INFO` logs by splitting `log_info` into separate columns.
        """
        if not self.__spray_info_df.empty:
            spray_columns = [
                'spray_status', 'pump_pwm', 'nozzle_pwm', 'req_flowrate',
                'actual_flowrate', 'flowmeter_pulse', 'payload_rem',
                'area_sprayed', 'req_dosage', 'actual_dosage', 'prv_wp',
                'next_wp'
            ]

            # Split 'log_info' into columns
            self.__spray_info_df[spray_columns] = \
                self.__spray_info_df['log_info'].str.split(',', expand=True)

            # Strip whitespace from new columns
            for col in spray_columns:
                self.__spray_info_df[col] = self.__spray_info_df[col].str.strip()

            # Convert numeric columns
            for col in spray_columns:
                self.__spray_info_df[col] = pd.to_numeric(self.__spray_info_df[col], errors='coerce')

            # Drop 'log_info' column after parsing and reset index
            self.__spray_info_df = self.__spray_info_df.drop(columns=['log_info']).reset_index(drop=True)
        else:
            log.w("No SPRAY_INFO logs to process.")

    def __add_location_info_to_spray_dataframe(self):
        """
        Appends latitude, longitude, and height from the closest mission_info entry to spray_info_df.
        """
        try:
            if self.__mission_info_df.empty or self.__spray_info_df.empty:
                log.w("Either mission_info_df or spray_info_df is empty. Cannot add location info.")
                return

            # Ensure required columns are present
            required_columns = ['timestamp', 'latitude', 'longitude', 'height']
            for col in required_columns:
                if col not in self.__mission_info_df.columns:
                    log.w(f"Column '{col}' not found in mission_info_df.")
                    return

            # Ensure timestamp columns are datetime and data is sorted
            self.__mission_info_df['timestamp'] = pd.to_datetime(self.__mission_info_df['timestamp'])
            self.__mission_info_df.sort_values('timestamp', inplace=True)

            self.__spray_info_df['timestamp'] = pd.to_datetime(self.__spray_info_df['timestamp'])
            self.__spray_info_df.sort_values('timestamp', inplace=True)

            # Use merge_asof to merge on timestamp
            merged_df = pd.merge_asof(
                self.__spray_info_df,
                self.__mission_info_df[['timestamp', 'latitude', 'longitude', 'height']],
                on='timestamp',
                direction='nearest',
                tolerance=pd.Timedelta('1s')  # Adjust tolerance as needed
            )

            # Update __spray_info_df with the merged data
            self.__spray_info_df = merged_df.reset_index(drop=True)

            log.i("Location info added to spray_info_df successfully.")

        except Exception as e:
            log.e(f"Error adding location info to spray_info_df: {e}")

    @property
    def master_df(self):
        """
        Returns the master DataFrame containing all logs.
        """
        return self.__master_df

    @property
    def mission_info_df(self):
        """
        Returns the processed DataFrame containing MISSION_INFO logs.
        """
        return self.__mission_info_df

    @property
    def spray_info_df(self):
        """
        Returns the processed DataFrame containing SPRAY_INFO logs.
        """
        return self.__spray_info_df
