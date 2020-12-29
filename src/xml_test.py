import xml.etree.ElementTree as ET


# XMLデータの読み込み
tree = ET.parse('') 
root = tree.getroot()

# 最上位階層のタグ・中身
print(root.tag,root.attrib)
"""
rss {'version': '2.0'}
"""

# 子階層のタグ・中身
for child in root:
    print(child.tag, child.attrib)

"""
channel {}
"""


# 要素「title」のデータを1つずつ取得
for title in root.iter('title'):
    print(title.text)

"""
Example Title1
HogeHoge Item Title
"""


# 配列の要素番号でデータを取得
print(root[0])
print(root[0][0])
print(root[0][1])
print(root[0][2])
print(root[0][0].text)
print(root[0][1].text)
print(root[0][2].text)

"""




Example Title1
HogeHoge Description
http://example.ex/
""
