def print_sudoku(sudoku):
    TOP_ROW_FORMAT = "╔═══════╤═══════╤═══════╗"
    MID_ROW_FORMAT = "╟───────┼───────┼───────╢"
    BOT_ROW_FORMAT = "╚═══════╧═══════╧═══════╝"
    ROW_FORMAT = "║ {} {} {} │ {} {} {} │ {} {} {} ║"

    sudoku_nums = []
    for idx in range(81):
        row = idx // 9
        col = idx % 9

        array_sum = 0
        for i, p in enumerate(sudoku[row][col]):
            array_sum += p
            if p == 1:
                value = str(i + 1)

        if array_sum != 1:
            value = "_"

        sudoku_nums.append(value)

    print(TOP_ROW_FORMAT)
    for j in [0, 9, 18]:
        print(ROW_FORMAT.format(*sudoku_nums[j : j + 9]))
    print(MID_ROW_FORMAT)
    for j in [27, 36, 45]:
        print(ROW_FORMAT.format(*sudoku_nums[j : j + 9]))
    print(MID_ROW_FORMAT)
    for j in [54, 63, 72]:
        print(ROW_FORMAT.format(*sudoku_nums[j : j + 9]))
    print(BOT_ROW_FORMAT)
