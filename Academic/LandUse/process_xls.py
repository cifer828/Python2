import xlrd
import xlwt

workbook = xlrd.open_workbook('poi_sh_2014.xlsx')
sheet = workbook.sheet_by_index(0)
pois = []
for row in range(0, 775):
    poi = []
    for col in range(0, 10):
        poi.append(sheet.cell_value(row, col))
    print poi
    try:
        if len(poi[2]) > len(poi[3]):
            poi.pop(3)
        else:
            poi.pop(2)
    except:
        poi.pop(3)
    pois.append(poi)
new_wb = xlwt.Workbook()
new_sheet = new_wb.add_sheet('sheet1', cell_overwrite_ok=True)
for row in range(0, 775):
    for col in range(0, 9):
        new_sheet.write(row, col, pois[row][col])
new_wb.save('extra_data.xls')
