import argparse

import download
import sixmonth


def main():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(required=True)

    download_parser = sub_parsers.add_parser("download")
    download_parser.set_defaults(func=call_download)

    sixmonth_parser = sub_parsers.add_parser("sixmonth")
    sixmonth_parser.set_defaults(func=call_sixmonth)

    args = parser.parse_args()
    args.func(args)


def call_download(*args):
    download.download()


def call_sixmonth(*args):
    sixmonth.sixmonth()


if __name__ == "__main__":
    main()
