from openpyxl import load_workbook

src = "Issues/bug722.xlsx"
#src = "../fixed.xlsx"
#src = "../Issues/bug722-xl.xlsx"

wb = load_workbook(src, keep_links=True)
