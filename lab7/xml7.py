from xml_to_dict import XMLtoDict


def main(src="res.xml"):
    xmlparser = XMLtoDict()
    cnt = 1
    with open(src, 'r') as f:
        data = xmlparser.parse(f.read())['root']['result']
        for entry in data:
            print(f"ENTRY #{cnt}")
            cnt += 1
            for key, value in entry.items():
                print(f"\tkey={key}, value={value}")

if __name__ == '__main__':
    main()