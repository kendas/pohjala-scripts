from argparse import ArgumentParser


def main():
    args = parse_args()


def parse_args():
    parser = ArgumentParser(description="Võtab Google Spreatsheet'i tabelist liikmete "
                                        "nimekirja ja vormindab selle wiki formaati.")
    parser.add_argument('spreadsheet',
                        help="Link Google Spreatsheet'ini")
    return parser.parse_args()


if __name__ == '__main__':
    main()
