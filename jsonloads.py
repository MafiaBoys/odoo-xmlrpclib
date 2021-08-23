from os import access ,R_OK
import json 


def loadsJsonFile(tagname,filename,dictAttributesError,attrs,_exit):

    _dict = _data = None

    if not filename:
       _exit('[func] _getJsonFileDict : filename = %s' % (filename))

    if access(filename ,R_OK) and tagname:
       try:
          with open(filename,'r') as _file:
               _data = _file.read()
       except IOError as _err:
           _file.close()
           _exit ('Cant be Read file <%s>' % (filename))

       _file.close()

       try:
          _dict = json.loads(_data)
       except ValueError as _err:
           _exit('Json File attrs Error')

       if not dictAttributesError(_dict ,[tagname]):
          _exit('tag <%s> Not found in file <%s>' % (tagname ,filename))

       if dictAttributesError( _dict [tagname] ,attrs):
          return _dict [tagname]
       else:
          _exit('File <%s> Tag <%s> Error attrs Not Exists' % (filename ,self.tagname))

       _exit('Permission Error')

