import os

# Get the path of the entire project
# os.path.dirname gets location of the passed path (and therefore
# doesn't include the file name.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print(BASE_DIR)
