import argparse

import download
import sixmonth
import vxxvxz


def main():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(required=True)

    download_parser = sub_parsers.add_parser("download")
    download_parser.set_defaults(func=call_download)

    sixmonth_parser = sub_parsers.add_parser("sixmonth")
    sixmonth_parser.set_defaults(func=call_sixmonth)

    vxxvxz_parser = sub_parsers.add_parser("vxxvxz")
    vxxvxz_parser.set_defaults(func=call_vxxvxz)

    args = parser.parse_args()
    args.func(args)


def call_download(*args):
    download.download()


def call_sixmonth(*args):
    sixmonth.sixmonth()


def call_vxxvxz(*args):
    vxxvxz.vxxvxz()


if __name__ == "__main__":
    main()
