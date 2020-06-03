import scheduler   # For testing
import db          # For testing

row_head = "<tr>"
row_tail = "</tr>"

cell_head = "<td>"
cell_tail = "</td>"

cell_head_th = "<th>"
cell_tail_th = "</th>"

table_head = "<h2>Schedule</h2><table>"
table_tail = "</table>"

table_head_head = "<thead>"
table_head_tail = "</thead>"

table_body_head = "<tbody>"
table_body_tail = "</tbody>"

header_loc = "./header"
footer_loc = "./footer"

display_file_name = "display.html"

titles = [
            "Truck ID",
            "Origin",
            "Destination",
            "Load",
            "Load Start",
            "Departure",
            "Arrival",
            "Unload Start",
            "Break Start",
            "Distance(m)",
            "Fuel Cost(SEK)"
        ]

def table_HTML_gen(head_strings, row_strings):
    table = table_head

    head_row = table_head_head + row_head
    for i in head_strings:
        head_row += (cell_head_th + i + cell_tail_th)
    head_row += (row_tail + table_head_tail)

    table += (head_row + table_body_head)

    all_rows = ""
    for i in row_strings:
        all_cells = ""
        for j in i:
            all_cells += cell_head
            all_cells += j
            all_cells += cell_tail
        all_rows += row_head + all_cells + row_tail

    table += (all_rows + table_body_tail + table_tail)

    return table

def save_HTML(contents, sum_price_rand, sum_dist_rand, sum_price_dss, sum_dist_dss):
    file = open(header_loc,"r")
    header = file.read()
    file.close()

    file = open(footer_loc,"r")
    footer = file.read()
    file.close()
    # contents2 = scheduler.plan_schedule("08:00", "17:00", "12:00", 60, 15, 10, 10) # For testing
    table = table_HTML_gen(titles, contents)
    # print(contents) # For testing

    summed_results = """
            <span style=\"float: left;\">FIFO Distance: {} km</span><br>
            <span style=\"float: left;\">FIFO Cost: {} SEK</span><br><br>
            <span style=\"float: left;\">DSS Distance: {} km</span><br>
            <span style=\"float: left;\">DSS Cost: {} SEK</span><br><br>
            <span style=\"float: left;\">Saved Distance: {} km ({}%)</span><br>
            <span style=\"float: left;\">Saved Cost: {} SEK ({}%)</span><br><br>
    """.format(sum_dist_rand/1000, sum_price_rand, sum_dist_dss/1000, sum_price_dss, (sum_dist_rand-sum_dist_dss)/1000, (round((1-((sum_dist_dss/1000)/(sum_dist_rand/1000))),2)*100), (sum_price_rand-sum_price_dss), (round((1-((sum_price_dss/1000)/(sum_price_rand/1000))),2)*100))

    complete = header + summed_results + table + footer
    print(complete)

    file = open(display_file_name,"w+")
    file.write("%s" % complete)
    file.close()

# save_HTML() # For testing
