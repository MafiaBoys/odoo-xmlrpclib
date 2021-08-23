from os import access ,R_OK
import json 
import types
import json 
import sys

from jsonloads import loadsJsonFile
from xmlrpclib import ServerProxy,socket,MultiCall
from functools import partial 

__list__ = {

    '_attrs_' : ['host','service','dbname','username','password'],
    '_perms_' : ['read','write','unlink','create'],
    '_json_filename_' : 'file.json'
}


class SocketProxy(object):
  
    def __init__(self,tagname=None):

        common = _object = None
        self.tagname = tagname
        self.host = None
        self.uid = self.execute = None

        db = None
        key = None
        user = None
 
        if not tagname:
           self.exit('tag name error')
        
        self.server = loadsJsonFile (tagname,
                      __list__['_json_filename_'],
                      self.dictAttributesError,
                      __list__['_attrs_'] ,
                      self.exit)

        self.host = self.addSubdomain (self.server['host'],
                    self.server['service']) 
        
        common  = ServerProxy(self.addSubdomain(self.host,'common'))
        _object = ServerProxy(self.addSubdomain(self.host,'object')) 


        user = self.server['username']
        key  = self.server['password']
        db   = self.server['dbname']

        if not (self.checkInstance(common) and self.checkInstance(_object)):
           self.exit('Instance common and Object Error')

        try:
           self.uid = common.login(db,user,key)
        except socket.error as e:
               self.exit('[Errno 111] Connection refuse -> Server Not started')


        if self.uid > 0:
           self.execute = partial(_object.execute ,db ,self.uid ,key)
      

        if not self.execute:
           self.exit('execute is none')
     

    def dictAttributesError(self,_dict,attributes):

        dictAttributeError = True

        if _dict and attributes:
           try:
              for attribute in attributes:
                  if not attribute in _dict:
                  
                     dictAttributeError = not dictAttributeError
                     break
           except AttributeError as e:
               return not dictAttributeError

        if dictAttributeError:
           for attribute in attributes:
           
               if not _dict[attribute]:
                  dictAttributeError = not dictAttributeError
                  break

        return dictAttributeError



    def exit (self,message=None):
        if message:
           print message
        sys.exit()

    def checkInstance(self,name):
        return type(name) == types.InstanceType


    def addSubdomain(self,domain,_sub ,state=False):

        separator = '/'

        if _sub and domain:
           if not _sub.endswith(separator) and state:
              _sub += separator

           if not domain.endswith(separator):
              domain += separator

           return domain + _sub
        return domain

    def read (self,_name ,fields):

    
        return self.execute(_name ,'search_read',[],fields)
#--------------------------------------------------------------------------------------------



db = SocketProxy('mostafa')

db.version()
db.read()

if db.checkPermission('res.parnter',['read']):
   db.read('res.parnter',['name','value'])
   db.search('res.parnter',[])
