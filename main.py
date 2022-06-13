import calendar
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from borb.pdf import Table, FlexibleColumnWidthTable, TableCell, X11Color
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF

months = ['ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ',
          'ДЕКАБРЬ']

with open('names.txt', encoding='utf-8') as inf:  # чтение файла и копирование имен в строку nameList
    nameList = inf.readlines()
    nameList = [line.rstrip() for line in nameList]


def get_date():
    print('Введите месяц и год\nНапример: 11.2019')
    while True:
        input_date = input()
        input_date = '1.' + input_date
        try:
            curr_date = datetime.strptime(input_date, '%d.%m.%Y')
            break
        except:
            print('Введите правильную дату')
    return curr_date

date = get_date() # переменная даты

print('Рисуем таблицу...')
reset_date = date

num_of_days = int((calendar.monthrange(date.year, date.month))[1])

document = Document()
page = Page(width=PageSize.A4_LANDSCAPE.value[0],height=PageSize.A4_LANDSCAPE.value[1])
document.append_page(page)

layout = SingleColumnLayout(page)
layout._vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

font_path: Path = Path(__file__).parent / "timesnewromanpsmt.ttf"
custom_font: Font = TrueTypeFont.true_type_font_from_file(font_path)

printtext = 'График дежурства на ' + str(months[date.month - 1])
layout.add(Paragraph(printtext,
                     vertical_alignment=Alignment.TOP,
                     text_alignment=Alignment.CENTERED,
                     font_size=Decimal(20),
                     font=custom_font))

t: Table = FlexibleColumnWidthTable(
    number_of_columns=num_of_days + 1,
    number_of_rows=len(nameList) + 1,
    horizontal_alignment=Alignment.CENTERED)

m = Decimal(2)

for i in range(-1, len(nameList)):
    for j in range(num_of_days + 1):
        if i == -1 and j == 0:
            t.add(Paragraph(' '))
            continue
        elif i == -1 and j > 0:
            if date.isoweekday() == 6 or date.isoweekday() == 7:
                t.add(TableCell(Paragraph(str(j), text_alignment=Alignment.CENTERED, vertical_alignment=Alignment.TOP,
                    padding_bottom=Decimal(m + 1),
                    font=custom_font),
                    background_color=X11Color("Red"),
                    preferred_width=Decimal(17)))
            else:
                t.add(TableCell(Paragraph(str(j), text_alignment=Alignment.CENTERED, vertical_alignment=Alignment.TOP,
                     padding_bottom=Decimal(m + 1),
                     font=custom_font),
                     preferred_width=Decimal(17)))
        elif i > -1 and j == 0:
            t.add(TableCell(Paragraph(nameList[i],text_alignment=Alignment.CENTERED,
                padding_top=Decimal(m),
                padding_left=Decimal(m),
                padding_bottom=Decimal(m),
                padding_right=Decimal(m),
                font=custom_font)))
            continue
        else:
            if date.isoweekday() == 6 or date.isoweekday() == 7:
                t.add(TableCell(Paragraph(' '), background_color=X11Color("Red")))
            else:
                t.add(Paragraph(' '))
        date += timedelta(days=1)
    date = reset_date
layout.add(t)

with open("list.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, document)