from random import randint
from arSqlite import Db

localDb = 'db\db.db'
tabelaPrincipal = 'table01'

try:
	db = Db(localDb)
	db.getTabela(tabelaPrincipal)

except:
	db.novaTabela(tabelaPrincipal, ('id TEXT NOT NULL PRIMARY KEY', 'valor TEXT NOT NULL'))


def editKey(lastKey, newKey):
	if lastKey in myKeys():
		lastValue = pull(lastKey)
		cleanKey(lastKey)
		push(newKey, lastValue)

def putOn(key, value):
	if type(pull(key)) == type([]) or type(pull(key)) == type(()):
		lastValue = pull(key)
		lastValue.append(value)
		push(key, lastValue, force=True)
	else:
		print(f'Key: {key} is not list or tuple.')

def cleanKey(key):
	try: 
		valor = db.getInstancia(tabelaPrincipal, ['id', key])[0][1]
		tipo = valor[:4]
		conteudo = valor[6:]

	except: return False

	if tipo == 'stri' or tipo == 'inte' or tipo == 'flot':
		db.delInstancia(tabelaPrincipal, ["id", key])
	elif tipo == 'list' or tipo == 'tupl':
		for i in conteudo.split(): cleanKey(i)
		db.delInstancia(tabelaPrincipal, ["id", key])
	
	return True

def push(key=None, valor=None, force=None):
	def newKey(char='#'):
		return char + str(randint(1000000, 9999999))
	
	if not key: key = newKey()
	else: pass

	while key in myKeys(filter=None):
		if force: 
			cleanKey(key)
		else:
			if key[0] == '#':
				novaKey = newKey()
			else:
				novaKey = newKey('')
				print(f'Key {key}, já utilizada... Nova key: {novaKey}.')

			key = novaKey
	#print(type(valor))
	if type(valor) == type(''):
		valor = 'stri: ' + str(valor)
		db.novaInstancia(tabelaPrincipal, ['id', 'valor'], (key, valor))
	
	elif type(valor) == type(0):
		valor = 'inte: ' + str(valor)
		db.novaInstancia(tabelaPrincipal, ['id', 'valor'], (key, valor))
	
	elif type(valor) == type(1.0):
		valor = 'flot: ' + str(valor)
		db.novaInstancia(tabelaPrincipal, ['id', 'valor'], (key, valor))
	
	else:
		if type(valor) == type([]): valorListString = 'list:'
		elif type(valor) == type(()): valorListString = 'tupl:'
		print(key)
		for i in valor:
			
			valorListString += (' ' + push(None, i))
		db.novaInstancia(tabelaPrincipal, ['id', 'valor'], (key, valorListString))
		
	return key

def pull(key):
	try:
		dados = db.getInstancia(tabelaPrincipal, ['id', key])[0][1]
		tipo = dados[:4]
		conteudo = dados[6:]
		
		if tipo == 'stri': return str(conteudo)
		elif tipo == 'inte': return int(conteudo)
		elif tipo == 'flot': return float(conteudo)
		elif tipo == 'list': return list(pull(i) for i in conteudo.split())
		elif tipo == 'tupl': return tuple(pull(i) for i in conteudo.split())

	except:
		return "Não foi possível encontrar o conteúdo..."

def myKeys(filter='#'):
	myKeys = []
	for i in db.getTabela(tabelaPrincipal):
		if not i[0][0] == filter: myKeys.append(i[0])
	return myKeys
	
if __name__ == '__main__':

	print(myKeys())
