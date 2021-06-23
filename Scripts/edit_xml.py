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

  def EditParams(self,xpath,val):
    element = self.__xml.find(xpath)    
    if element == None:
      self.AddElement(xpath)
      element = self.__xml.find(xpath)
    element.text = val

  def AddElement(self,xpath):
    path_list = xpath.split('/')
    path = path_list[0]
    parent = self.__xml
    element = parent
    for i in range(1,len(path_list)):
      path = os.path.join(path,path_list[i])
      parent = element
      element = self.__xml.find(path)
      if element == None:
        element = ET.SubElement(parent, path_list[i])

  def DeleteElement(self,xpath):
    parent = self.__xml.find(os.path.dirname(xpath))
    element = self.__xml.find(xpath)
    if not element == None:
      parent.remove(element)

  def PrintXml(self,filename):
    self.__xml.write(filename,encoding='UTF-8')