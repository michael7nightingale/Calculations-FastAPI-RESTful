import sys

from app.db.dumpdata.dump_data import dump_data


if __name__ == '__main__':
    args = sys.argv[1:]
    match args:
        case ['dumpdata']:
            dump_data()




