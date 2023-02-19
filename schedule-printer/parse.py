from datetime import datetime
from lxml import etree
from download import load_schedule


NOW = datetime.now()
DATETIME_FORMAT = '%A, %b %d, %I:%M %p'
WEBPAGE = etree.HTML(load_schedule())


def root() -> etree.Element:
    """return the schedule ul, taking the following path in schedule.html: 
    html -> body -> div id=page-view -> div class=content-wrapper -> 
    div class=content -> div class=modiu-base tabular-calendar-view ->
    ul class=modui-base modiu-list-view
    """
    return WEBPAGE.xpath("body/div[@id='page-view']/div[1]/div[2]/div[2]/ul")[0]


def weeks(dom: etree.Element) -> list[etree.Element]:
    """return weekly schedules, taking the following path:
    root() -> li
    """
    return dom.getchildren()


def week(n: int) -> etree.Element:
    """return mass schedule for a given week, taking the following path: 
    root() -> li[n] -> div class=modui-base mass-group-view
    """
    return weeks()[n][0]


def table(week: etree.Element) -> tuple[str, etree.Element]:
    """return label, table for a given week, taking the following path:
    week(n) -> div class=modui-base mass-group-label
    week(n) -> div class=modui base mass-group
    """
    table = week.find("div/div[@class='mass-group']/table")
    label = week.find("div/div[@class='mass-group-label']").text
    return table, label


def table_header(table: etree.Element) -> etree.Element:
    """return table header, taking the following path: 
    table(n) -> tbody -> tr class=modui base mass-list-row header-row
    """
    return table.find("tbody").getchildren()[0]


def header_values(header: etree.Element) -> list[str]:
    """return list of strings for each element in header row"""
    return [elem.text for elem in header.getchildren()][1:]


def rows(table: etree.Element) -> list[etree.Element]:
    """return table rows, taking the following path:
    table(n) -> tbody -> tr class=modui base mass-list-row mass-header
    """
    return table.find("tbody").getchildren()[1:]


def row(table: etree.Element, n: int) -> list[etree.Element]:
    """return specific row of a table, taking the following path:
    table(n) -> tbody -> tr class=modui base mass-list-row[i] 
    """
    return rows(table)[n]


def cells(row: etree.Element) -> list[etree.Element]: 
    """return cells given specific row of table, taking the following path: 
    row[i] -> tr class=modui-base mass-list-row mass-header
    """
    return row.getchildren()


def process_date(date: str) -> datetime:
    """return datetime given date in schedule format (string)"""
    date = datetime.strptime(date, DATETIME_FORMAT)
    return datetime(year=NOW.year if not (date.month == '1' and NOW.month == '12') else NOW.year + 1, 
                    month=date.month, 
                    day=date.day, 
                    hour=date.hour, 
                    minute=date.minute)


def values(cells: list[etree.Element], header_values: list[str]) -> list[tuple]: 
    """return processed values given cells"""
    
    res = []
    ix = cells[0]
    values = cells[1:]

    # select date cell; store link and date
    date_cell = ix.getchildren()[0]
    link = date_cell.values()[3]
    date = process_date(date_cell.text)

    # loop through each value cell
    for cell, title in zip(values, header_values): 
        positions = cell.getchildren()[0].getchildren()
        
        # loop through each individual in each cell, grabbing name
        for position in positions: 
            name = position\
                .find("div/div[@class='minister']/span")\
                .text\
                .replace('\n', '')\
                .replace('\t', '')

            # append record to res
            record = (date, link, name, title)
            res.append(record)

    return res


def flatten(res: list[list]):
    res, _ = [], res
    for li in _:
        for v in li: 
            res.append(v)
    return res


def main():
    res = []
    dom = root()

    for wk in weeks(dom):
        tbl, lbl = table(wk)
        h = table_header(tbl)
        h_v = header_values(h)

        for row in rows(tbl):
            c = cells(row)
            v = values(c, h_v)
            res.append(v)

    parsed = flatten(res)
    return parsed


if __name__ == '__main__': 
    main()
