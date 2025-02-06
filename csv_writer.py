import csv
from collections import OrderedDict
import logging

class CSVWriter:
    def __init__(self):
        logging.debug("Initializing CSVWriter class")
        pass

    def write_to_csv(self, data, output_file):
        logging.debug(f"Writing data to CSV file: {output_file}")
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Scenarios'])
            scenarios = self.extract_scenarios(data)
            self.write_scenarios(writer, scenarios)
            writer.writerow(['Feature', 'Test Case/Scenario', 'Test Step'])
            self.write_features_and_steps(writer, data)

    def extract_scenarios(self, data):
        logging.debug("Extracting scenarios from data")
        seen = OrderedDict()
        scenarios = []
        for row in data:
            scenario = row[1]
            if scenario and scenario not in seen:
                scenarios.append(scenario)
                seen[scenario] = None
        return scenarios

    def write_scenarios(self, writer, scenarios):
        logging.debug("Writing scenarios to CSV")
        for scenario in scenarios:
            writer.writerow([scenario])

    def write_features_and_steps(self, writer, data):
        logging.debug("Writing features and steps to CSV")
        last_feature = None
        last_scenario = None

        for i, (feature, scenario, step) in enumerate(data):
            if feature == last_feature:
                feature = ''
            else:
                last_feature = feature

            if scenario == last_scenario:
                scenario = ''
            else:
                last_scenario = scenario

            writer.writerow([feature, scenario, step])

            if i + 1 < len(data) and data[i + 1][1] != last_scenario:
                writer.writerow(['', '', ''])
            elif i + 1 == len(data):
                writer.writerow(['', '', ''])
