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


def make_nice_width_markdown_table(header, rows, justification="<"):
    """
    A minimal tool to make a text table in markdown format
    https://daringfireball.net/projects/markdown/

    :param header: Column names
    :param rows: Data rows
    :param justification: justification character, "<" = left, "^"=center, ">"= right
    :return: table text in markdown format
    """
    rows = tuple(rows)  # might be a generator, so put is in memory
    lrs = [len(str(_)) for _ in header]
    for row in rows:
        lrs =[max(len(str(_)), len_) for _, len_ in zip(row, lrs)]
    text = "|".join([f"{str(_):{justification}{len_}}" for len_, _ in zip(lrs, header)]) + "\n"
    text += "|".join(["-"*len_ for len_ in lrs]) + "\n"
    for row in rows:
        text += "|".join([f"{str(_):{justification}{len_}}" for _, len_ in zip(row, lrs)]) + "\n"
    return text


if __name__ == "__main__":
    header = "Furlongs", "Fortnights"
    columns = [1, 2, 3], [1.003956, 42, 11]
    rows = zip(*columns)
    text = make_nice_width_markdown_table(header, rows)
    print(text)
    print()
    rows = zip(*columns)
    text = make_nice_width_markdown_table(header, rows, "^")
    print(text)
    print()
    rows = zip(*columns)
    text = make_nice_width_markdown_table(header, rows, ">")
    print(text)
    print()
    with open("example_markdown_table.md", "w") as fd:
        fd.writelines(text)
    """
Furlongs|Fortnights
---|---
1|1
2|42
3|11

"""
