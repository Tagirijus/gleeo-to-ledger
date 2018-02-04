import argparse
import csv
import datetime
import os


ARGS = argparse.ArgumentParser(
    description=(
        'A Gleeo Timetracker to ledger-cli timetracing format converter.'
    )
)

ARGS.add_argument(
    'file',
    nargs='?',
    default='None',
    help='The input .csv file.'
)

ARGS.add_argument(
    '-o',
    '--output',
    default='output.journal',
    help='The output file. Default is "output.journal".'
)

ARGS.add_argument(
    '-a',
    '--append',
    action='store_true',
    help=(
        'Enable the append mode. Tries to append to the output file, instead of '
        're-writing it completely.'
    )
)

ARGS.add_argument(
    '-F',
    '--force',
    action='store_true',
    help=(
        'Overwrites the output file. Attention: default file is "output.journal"! '
        'If this file exists, it will be overwritten!'
    )
)

ARGS.add_argument(
    '--seperator',
    default=',',
    help='The CSV seperator. Default is ",".'
)

ARGS.add_argument(
    '--super-account',
    default='All',
    help=(
        'The string for the super-account. Means the first account of the ledger-cli '
        'format. E.g. All:Client:Project:Task, where "All" is the super-account. '
        'Default is "All".'
    )
)

ARGS = ARGS.parse_args()


# index of the column for the format of the Gleeo Time Tracker CSV
ROW_DOMAIN = 0
ROW_PROJECT = 1
ROW_TASK = 2
ROW_DETAILS = 3
ROW_START_DATE = 4
ROW_START_TIME = 5
ROW_END_DATE = 6
ROW_END_TIME = 7
ROW_DURATION = 8
ROW_DURATION_DEC = 9
ROW_PROJECT_XTRA1 = 10
ROW_PROJECT_XTRA2 = 11
ROW_TASK_XTRA1 = 12
ROW_TASK_XTRA2 = 13


# format of the ledger output - the indexes of the CSV columns
# basically it generates the accounts of the ledger-cli format like:
#       ARGS.super_account:LED_A:LED_B:LED_C:LED_D
LED_A = ROW_DOMAIN
LED_B = ROW_PROJECT
LED_C = ROW_TASK
LED_D = ROW_DETAILS


def csv_to_ledger(data=None, superacc='All'):
    """Output the input CSV object as ledger-cli format data."""
    if type(data) is not list:
        print('Attention: no data given in csv_to_ledger()!')
        return ''

    final_output = ''
    for index, row in enumerate(data[1:]):

        tmp_time_format_start = '{} {}'.format(
            row[ROW_START_DATE],
            row[ROW_START_TIME]
        )

        tmp_time_format_end = '{} {}'.format(
            row[ROW_END_DATE],
            row[ROW_END_TIME]
        )

        # reformat the input time into a new string with datetime,
        # to get the correct dates and time, which have to be valid
        tmp_start = datetime.datetime.strptime(
            tmp_time_format_start, '%Y-%m-%d %H:%M'
        ).strftime('%Y/%m/%d %H:%M:00')

        tmp_ende = datetime.datetime.strptime(
            tmp_time_format_end, '%Y-%m-%d %H:%M'
        ).strftime('%Y/%m/%d %H:%M:00')

        tmp_a = row[LED_A] if row[LED_A] else row[LED_B] if row[LED_B] else 'Account'
        tmp_b = ':' + row[LED_B] if (row[LED_B] and row[LED_A]) else ''
        tmp_c = ':' + row[LED_C] if row[LED_C] else ''
        tmp_d = ':' + row[LED_D] if row[LED_D] else ''

        final_output += 'i {} {}:{}{}{}{}\no {}'.format(
            tmp_start, superacc, tmp_a, tmp_b, tmp_c, tmp_d, tmp_ende
        )

        if index != len(data) - 1:
            final_output += '\n\n'

    return final_output.strip()


if __name__ == '__main__':
    if not os.path.isfile(ARGS.file):
        print('No valid file.')
        exit()

    # the file loading here
    with open(ARGS.file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=ARGS.seperator, quotechar='"')
        data = []
        for row in spamreader:
            data.append(row)

    # the conversion here
    converted_data = csv_to_ledger(data=data, superacc=ARGS.super_account)

    # output file exists and not overwrite and not append
    if not ARGS.force and not ARGS.append and os.path.isfile(ARGS.output):
        print('"{}" does alread exists. Use -F or --force to overwrite it.'.format(
            ARGS.output
        ))
        exit()

    # append it
    if ARGS.append:
        with open(ARGS.output, 'a') as file:
            file.write('\n\n')
            file.write(converted_data)
            print('Appended to "{}"!'.format(ARGS.output))

    # write or even overwrite it without append
    else:
        with open(ARGS.output, 'w') as file:
            file.write(converted_data)
            print('Written to "{}"!'.format(ARGS.output))
