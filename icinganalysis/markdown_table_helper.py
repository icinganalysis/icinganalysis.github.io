def make_markdown_table(header, rows):
    """
    A minimal tool to make a text table in markdown format
    https://daringfireball.net/projects/markdown/

    :param header: Column names
    :param rows: Data rows
    :return: table text in markdown format
    """
    text = "|".join(header) + "\n"
    text += "|".join(["---"] * len(header)) + "\n"
    for row in rows:
        text += "|".join([str(_) for _ in row]) + "\n"
    return text


if __name__ == "__main__":
    header = "Furlongs", "Fortnights"
    columns = [1, 2, 3], [1, 42, 11]
    rows = zip(*columns)
    text = make_markdown_table(header, rows)
    print(text)
    with open("example_markdown_table.md", "w") as fd:
        fd.writelines(text)
    """
Furlongs|Fortnights
---|---
1|1
2|42
3|11

"""
