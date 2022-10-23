import json

def main(src = 'res.json'):
    cnt = 1
    with open(src, 'r') as f:
        data = json.load(f)
        for entry in data:
            print(f"ENTRY #{cnt}")
            cnt += 1
            for key, value in entry.items():
                print(f"\tkey={key}, value={value}")

if __name__ == '__main__':
    main()