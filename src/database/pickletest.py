from tinydb import TinyDB, Query

db = TinyDB('bluetooth.json')

bluetooth = Query()


print( db.search(bluetooth.name == "hello") )