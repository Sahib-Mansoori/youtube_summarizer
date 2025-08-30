def read_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            x = f.read()
            if x:
                return x
            else:
                return None
    except:
        print(f"Could not read file: {file}")


def main():
    pass


if __name__ == '__main__':
    main()
