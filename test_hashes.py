def assert_is_sorted(lst, key=lambda x: x):
    for i, el in enumerate(lst[1:]):
        assert key(el) >= key(lst[i]) # i is the index of the previous element

def test_hashes():
    from binascii import crc32

    with open("ParamLabels.csv") as f:
        csv = [line.rstrip('\n').split(',') for line in f.readlines() if not line.isspace()]

    assert_is_sorted(csv, key=lambda i: i[1])
    for line in csv:
        hashString = line[0]
        assert len(hashString) >= 12
        # Only the lower 32 bits are the hash (blame arthur), ensure the crc is legit
        # length - uppermost 8  bits
        # crc32  - lowermost 32 bits
        assert crc32(line[1].encode('utf-8')) == (int(line[0], 16) & 0xFFFFFFFF)

def main():
    from binascii import crc32

    with open("ParamLabels.csv") as f:
        csv = [line.rstrip('\n').split(',') for line in f.readlines() if not line.isspace()]

    try:
        assert_is_sorted(csv, key=lambda i: i[1])
    except AssertionError:
        print("ParamLabels.csv is not sorted, run remove_duplicates.py to fix")
    for i,line in enumerate(csv):
        hashString = line[0]
        if not len(hashString) >= 12:
            print(f"'{hashString}', line {i+1} is not properly padded to 12 chars.")
        # Only the lower 32 bits are the hash (blame arthur), ensure the crc is legit
        if not crc32(line[1].encode('utf-8')) == (int(line[0], 16) & 0xFFFFFFFF):
            print(f"'{hashString}', line {i+1} length or hash mismatch.")

# Note: Intended use is with pytest, this is
#       merely for printing out incorrect hashes
if __name__ == '__main__':
    main()

