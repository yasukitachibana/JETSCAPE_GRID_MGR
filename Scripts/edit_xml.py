#import re
import os
import threading
import xml.etree.ElementTree as ET

class EditXml:
  _instance = None
  _lock = threading.Lock()
  __xml = None

  def __init__(self):
    pass

  def __new__(cls):
    with cls._lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
    return cls._instance

  def ReadXml(self, xml_filename):
    self.__xml = ET.parse(xml_filename)

  def Xml(self):
    return self.__xml

  def EditParams(self,tags,val):
    it = self.__xml
    
    for i in range(len(tags)):
      for el in it.iterfind(tags[i]):
        it = el
        print(el.text)
    # for tag in self.__xml.iterfind(tags[0]):
    #   print(tag.text)

    
    # for nic in root.iterfind('.//NIC/.'):
    # if nic.find('./NETWORK').text.strip()=="br100":
    #     print(nic.find('./MAC').text)
      
    pass
    
#     tag_module = GetTag(module_name)
#     match = re.search(tag_module,copy)
#     org = ''
#     if match:
#         org = match.group()
#     else:
#         print('failed to find the tag for the module: ' + module_name)
#         exit()

#     new = org
#     new = re.sub(GetTag(tag),GetTagVal(tag,val),new)
#     return copy.replace(org,new)


# def GetTag(tag):
#     return '<'+tag+'>(.|\s)*?</'+tag+'>'

# def GetTagVal(tag,val):
#     message1 = '\t<!-- auto-generated  -->\n\t'
#     message2 = '\n\t<!-- --------------- -->'
#     return message1+'<'+tag+'>'+str(val)+'</'+tag+'>'+message2


