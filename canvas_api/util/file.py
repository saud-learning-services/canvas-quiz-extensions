import logging
import csv

def read_from_csv(csv_file, headers, input_has_header=False):
    '''Turns a CSV file into a list.'''
    csv_file = csv_file.replace('"', '')
    try:
        return_list = []
        with open(csv_file) as csvfile:
            if input_has_header:
                reader = csv.DictReader(csvfile)
            else:
                reader = csv.DictReader(csvfile, fieldnames=headers)
            for row in reader:
                return_list.append(row)
            return return_list
    except IOError as e:
        logging.error("I/O error({0} : {1})".format(e.errno, e))
    except UnicodeDecodeError as e:
        logging.error("UnicodeDecodeError: {0}".format(e))
    finally:
        return return_list


def write_to_csv(filename, content):
    '''Turns a list into a CSV file.'''
    keep_trying = True
    while keep_trying:
        logging.info("writing content to file '{filename}'...".format(filename=filename))
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in content:
                    writer.writerow(row)
            logging.info("completed writing content to file.")
            keep_trying = False
        except Exception as e:
            logging.error("could not write content to file: {}".format(e))
            if input("try again? (y/n): ") != "y":
                keep_trying = False
