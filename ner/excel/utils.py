
import xlwt

def create_excel_workbook():
    workbook = xlwt.Workbook()
    setup_sheet = workbook.add_sheet("setup", cell_overwrite_ok = True)
    #setup_sheet.set_col_default_width(3000)
    #print "worksheet: %s" % str(dir(setup_sheet))
    s = "Setup Functions"
    setup_sheet.write(0, 0, s)
    setup_sheet.col(0).width = 256 * (len(s) + 1)
    setup_sheet.write(1, 0, "R, W, S, RF, WF")
    setup_sheet.write(2, 0, "Command")
    s = "Peripheral Device Name"
    setup_sheet.write(2, 1, s)
    setup_sheet.col(1).width = 256 * (len(s) + 1)
    s = "Offset"
    setup_sheet.write(2, 2, s)
    setup_sheet.col(2).width = 256 * (len(s) + 1)
    s = "Value"
    setup_sheet.write(2, 3, s)
    setup_sheet.col(2).width = 256 * (len(s) + 1)
    s = "Response Destination: Default: Column = 0, (Same Row)"
    setup_sheet.write(2, 4, s)
    setup_sheet.col(4).width = 256 * (len(s) + 1)


    loop_sheet = workbook.add_sheet("loop", cell_overwrite_ok = True)
    s = "Loop Functions"
    loop_sheet.write(0, 0, s)
    loop_sheet.col(0).width = 256 * (len(s) + 1)
    loop_sheet.write(1, 0,  "R, W, S, RF, WF")
    loop_sheet.write(2, 0, "Command")
    s = "Peripheral Device Name"
    loop_sheet.write(2, 1, s)
    loop_sheet.col(1).width = 256 * (len(s) + 1)
    s = "Offset"
    loop_sheet.write(2, 2, s)
    loop_sheet.col(2).width = 256 * (len(s) + 1)
    s = "Value"
    loop_sheet.write(2, 3, s)
    loop_sheet.col(2).width = 256 * (len(s) + 1)
    s = "Response Destination: Default: Column = 1, (Same Row)"
    loop_sheet.write(2, 4, s)
    loop_sheet.col(4).width = 256 * (len(s) + 1)


    result_sheet = workbook.add_sheet("results", cell_overwrite_ok = True)
    s = "Results"
    result_sheet.write(0, 0, "Results")
    result_sheet.col(0).width = 256 * (len(s) + 1)
    return workbook


