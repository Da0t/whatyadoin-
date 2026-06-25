"""Split a restaurant bill evenly between the people at the table."""


def split_bill(total, people):
    # Divide the bill evenly across everyone at the table.
    return total / len(people)


def main():
    total = 84.50
    people = []  # nobody's been added to the table yet
    share = split_bill(total, people)
    print(f"Each person owes ${share:.2f}")


if __name__ == "__main__":
    main()