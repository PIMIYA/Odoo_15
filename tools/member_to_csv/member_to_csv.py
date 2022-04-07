import argparse
from multiprocessing.dummy import Array
from urllib.request import Request, urlopen
import json
import csv


class Member(object):
    def __init__(self, SellerName: str = "", SellerId: str = "", Region: str = "", AuxId: str = "") -> None:
        self.SellerName = SellerName
        self.SellerId = SellerId
        self.Region = Region
        self.AuxId = AuxId


def get_members_from_api(url_path: str):
    req = Request(url_path, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as response:
        data = json.loads(
            response.read(), object_hook=lambda d: Member(**d))
        return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser("member_to_csv")
    parser.add_argument('url', help='Url of member api.', type=str)
    parser.add_argument(
        'output_file', help='File path of output file.', type=str)
    args = parser.parse_args()

    url = args.url
    res = get_members_from_api(url)

    outputFile = args.output_file
    with open(outputFile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # write header
        writer.writerow(Member().__dict__.keys())
        for x in res:
            writer.writerow(x.__dict__.values())
