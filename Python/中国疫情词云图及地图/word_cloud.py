import openpyxl
from wordcloud import WordCloud

def generate_pic(frequency,name):
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/STKAITI.TTF",
                        background_color="white",
                        width=1920,height=1080)
    wordcloud.generate_from_frequencies(frequency)
    wordcloud.to_file('%s.png'%(name))

wb = openpyxl.load_workbook('data.xlsx')
ws = wb['国内疫情']
frequency_in = {}
for row in ws.values:
    if row[0] == '地区':
        pass
    else:
        frequency_in[row[0]] = float(row[1])
frequency_out = {}
sheet_name = wb.sheetnames
for each in sheet_name:
    if "洲" in each:
        ws = wb[each]
        for row in ws.values:
            if row[0] == '国家':
                pass
            else:
                frequency_out[row[0]] = float(row[1])
generate_pic(frequency_in,"国内疫情词云图")
generate_pic(frequency_out,"世界疫情词云图")