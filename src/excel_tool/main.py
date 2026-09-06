from excel_tool.functions.load import load_workbook

def main():
    fp1 = input("Please drop file 1 here: ")
    fp2 = input("Please drop file 2 here: ")
    load_workbook(fp1, fp2)


if __name__ == "__main__":
    main()