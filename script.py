# -*- coding: UTF-8 -*-
import sys
import functools
from xmlrpclib import ServerProxy,Fault ,dumps,loads 


DATABASES = {
      'default' : {
           'URI': 'http://localhost:8069/',
           'service' : 'xmlrpc/2',
           'database': 'dbname',
           'username': 'admin',
           'password': 'admin'
      }
}

class createConnection(object):

	def __init__(self, tagname='default'):
	    super(createConnection, self).__init__()

        if not self.hasAttributes(DATABASES ,[tagname]):
	       self.reportError('[-] <{}> Not Found! in DATABASES'.format(tagname))
         
        if not self.hasAttributes(DATABASES[tagname],['URI','service','database','username','password']):
           self.reportError('[-] DATABASES[{}] Attributes Not Exists!'.format(tagname))

        SERVER = DATABASES[tagname]
        URI = self.getURI(SERVER['URI'] ,SERVER['service'])

        _user = SERVER['username']
        _pass = SERVER['password']

        UID = ServerProxy(self.getURI(URI ,'common')).login(SERVER['database'] ,_user ,_pass)
 
        OBJECT_URI = self.getURI(URI,'object')
        self.execute_command = functools.partial(ServerProxy(OBJECT_URI).execute,SERVER['database'],UID,_pass)
            

	def hasAttributes(self,_dict,attributes=[]):

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



        def read(self,model_id,domain=[],*args):
            return self.execute_command(model_id,'search_read',domain ,*args)
    

        def search(self,model_id,domain=[],*args):
            return self.execute_command(model_id,'search',domain,*args)



        def get(self,model_id,ids=[]):
            return self.execute_command(model_id,'name_get',ids)



        def write(self,model_id ,ids=[],fields={}):

            status = False
            try:
               status = self.execute_command(model_id ,'write',ids,fields)
            except Fault as error:
                   self.reportError(error.__dict__['faultString'])

            return status      


        def read_fields(self,model_id,domain=[],fields=[]):
            return self.execute_command(model_id,'fields_get',[],{'attributes':fields})


        def create(self,model_id,fields={}):
            return self.execute_command(model_id,'create',fields)	    
      

        def product_product(self ,traduction):
            pass


        def checkPermissions(self,model_id,permissions=[],raise_exception=False):
            return self.execute_command(model_id,'check_access_rights',[permissions],{'raise_exception':raise_exception})
               

        def getURI(self,URI ,_subURI , sepURI='/',mode=False):
        
            if _subURI and URI:
               if not _subURI.endswith(sepURI) and mode:
                  _subURI += sepURI
                  
               if not URI.endswith(sepURI):
                  URI += sepURI
               return URI + _subURI
            return URI

        def reportError(self,message=None):

            if message:
	       print (message)
	    sys.exit(1)  


def print_table(records):

    tabs = 45 

    for record in records:
        print ('name: ' + record['name'] + (' ' * (tabs - len(record['name']))) + 'product_uom_qty: -> ' + str(record['product_uom_qty'])+'\t' + record['state'])


if __name__ == '__main__':

   session = createConnection()
   records = session.read('stock.move',['&',('product_uom_qty','>',0),('state','not in',['cancel','done'])])
   #for record in records:
   #    print ('name: ' + record['name'],record['product_uom_qty'])

   print_table(records)

   # print (session.search('product.product',[('virtual_available','>',0)]))
   # print (session.checkPermissions('product.product',['read','write']))
   # ids = session.search('product.product',[('virtual_available','<=',0)])
   # print ids #session.write('product.product',ids,{'virtual_available': 777})       

   ## _ids = session.search('view.main',[('email','=','email@example.com')])
   ##  print session.write('view.main',_ids,{'usioaosiiiisiis':'error'})    



def auto(model_id ,traduction):

     




