import sys


def get_mean_size():
    """
    Reads the output of the 'ls -l' command from stdin and calculates the average file size in the directory.
    """
    lines = sys.stdin.readlines()[1:]  # Skip header line
    file_sizes = []

    for line in lines:
        columns = line.split()
        if len(columns) < 5:
            continue  # Skip invalid lines
        try:
            file_size = int(columns[4])  # File size is in the 5th column
            file_sizes.append(file_size)
        except ValueError:
            continue  # Ignore lines with non-numeric file sizes

    if not file_sizes:
        print("No valid file sizes found.")
        return

    mean_size = sum(file_sizes) / len(file_sizes)
    print(f"Average file size: {mean_size:.2f} bytes")


if __name__ == "__main__":
    get_mean_size()

# ls -l | python3 get_mean_size.py
# Average file size: 14799.83 bytes
