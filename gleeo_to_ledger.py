import argparse
import datetime


ARGS = argparse.ArgumentParser(
    description=(
        'A Gleeo Timetracker to ledger-cli timetracing format converter.'
    )
)

ARGS.add_argument(
    'file',
    nargs='?',
    default=None,
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


def csv_to_ledger(data=None):
    """Output the input CSV as ledger-cli format data."""
    pass


# big loop for each file
for single_file in csv_files:

    # load the file
    print 'Loading \'' + single_file[single_file.rfind('/') + 1:] + '\' ...'
    f = open(single_file, 'r')
    origin_raw = f.read().splitlines()
    if not first_line:
        origin_raw = origin_raw[1:]
    f.close()

    # generate the master variable
    origin = []
    for x in origin_raw:
        origin.append(x.split(seperator))

    # convert the entries to ledger format
    print 'Converting to ledger format ...'
    final_output = ''
    for y, x in enumerate(origin):
        tmp_start = datetime.datetime.strptime(
            x[row_start_date] + ' ' + x[row_start_time], '%Y-%m-%d %H:%M').strftime('%Y/%m/%d %H:%M:00')
        tmp_ende = datetime.datetime.strptime(
            x[row_end_date] + ' ' + x[row_end_time], '%Y-%m-%d %H:%M').strftime('%Y/%m/%d %H:%M:00')
        tmp_a = x[LED_A] if x[LED_A] else x[LED_B] if x[LED_B] else 'Account'
        tmp_b = ':' + x[LED_B] if (x[LED_B] and x[LED_A]) else ''
        tmp_c = ':' + x[LED_C] if x[LED_C] else ''
        tmp_d = ':' + x[LED_D] if x[LED_D] else ''
        final_output += 'i ' + tmp_start + ' ' + superacc + \
            ':' + tmp_a + tmp_b + tmp_c + tmp_d + '\n'
        final_output += 'o ' + tmp_ende
        if not y == len(origin) - 1:
            final_output += '\n\n'

    if append_it:
        # appending output to archive_file
        print 'Appending ...'
        f = open(archive_file, 'a')
        f.write('\n\n' + final_output)
        f.close()
        print 'Appended to \'' + archive_file + '\''
        print 'Deleting appended original data ...'
        f = open(single_file[0:single_file.rfind('.')] + '.journal', 'w')
        f.write('')
        f.close()
    else:
        # saving output to file
        print 'Saving ...'
        output_file = single_file[0:single_file.rfind('.')] + '.journal'
        output_file_name = output_file[output_file.rfind('/') + 1:]
        f = open(output_file, 'w')
        f.write(final_output)
        f.close()
        print 'Saved to \'' + output_file_name + '\''
