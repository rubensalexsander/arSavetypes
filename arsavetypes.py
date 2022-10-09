"""
#Biblioteca para gerenciamento simple de banco de dados usando SQLite.

- Para iniciar a utilização é necessário criar uma pasta para o banco de dados que será criado pelo objeto. Recomenda-se criar um diretório chamado "db".

Objetos:

- EasyDb: Banco de dados que possui uma lista de keys (chaves) que retornam valores.
	.__init__: (#Construtor
		local - Local do Banco de dados. Padrão = "db\db.db"
	)

	.push(#Envia uma nova key ao banco de dados
		key - String que será utilizada para recuperar o valor.
		valor - Dados a ser salvo.
		force - True: Se a key já estiver sendo utilizada, o valor será reescrito. False: Se a key já estiver sendo utilizada, será criada uma nova key aleatória.
	)

	.pull(#Retorna valor cadastrado na key pelo método push
		key - Chave do valor a ser retornado.
	)

	.my_keys(#Retorna key cadastradas no Db
		filter - Se o valor estiver na posição 0 da chave, ela não será retornada na lista. Utilizada para separar chaves internas (criadas aleatoriamente têm #) e externas (criadas pelo usuário).
	)

	.add(#Adiciona valor a chaves que são do tipo list ou tupl
		key - Lista que receberá o novo valor
		value - Valor a ser adicionado
	)

	.clean_key(#Limpa valores cadastrados na key
		key - Key que será limpa
	)

- Tipos de valores:

	#Já suportados:

	String - str
	Inteiro - int
	Flutuante - float
	Lista - list
	Tupla - tuple

	#Em desenvolvimento:
	Dicionários - map
	Boleanos - bool

"""

from random import randint
from arSqlite import DbSqlite

class EasyDb:
	def __init__(self, local='database.db'):
		self.__local = local
		self.__tabela_principal = 'table01'
		try:
			self.__db = DbSqlite(self.__local)
			self.__db.get_table(self.__tabela_principal)
		except:
			self.__db.new_table(self.__tabela_principal, ('id TEXT NOT NULL PRIMARY KEY', 'valor TEXT NOT NULL'))
	
	def __edit_key(self, lastKey, new_key):
		if lastKey in self.my_keys():
			self.__db.edit_instance(self.__tabela_principal, lastKey, 'id', new_key)
			
	def __edit_value(self, key, new_value):
		if key in self.my_keys():
			self.__db.edit_instance(self.__tabela_principal, key, 'valor', new_value)
	
	def push(self, key=None, valor=None, force=None):
		def new_key(char='#'):
			return char + str(randint(1000000, 9999999))
		
		if not key: key = new_key()
		else: pass

		while key in self.my_keys(''):
			
			if force: 
				self.clean_key(key)
			else:
				if key[0] == '#':
					novaKey = new_key()
				else:
					novaKey = new_key('')
					print(f'Key {key}, já utilizada... Nova key: {novaKey}.')

				key = novaKey
		
		if type(valor) == type(''):
			valor = 'stri: ' + str(valor)
			self.__db.new_instance(self.__tabela_principal, (key, valor))
		
		elif type(valor) == type(0):
			valor = 'inte: ' + str(valor)
			self.__db.new_instance(self.__tabela_principal, (key, valor))
		
		elif type(valor) == type(1.0):
			valor = 'flot: ' + str(valor)
			self.__db.new_instance(self.__tabela_principal, (key, valor))
		
		else:
			if type(valor) == type([]): valorListString = 'list:'
			elif type(valor) == type(()): valorListString = 'tupl:'
			print(valor)
			
			for i in valor:
				valorListString += (' ' + self.push(None, i))
			self.__db.new_instance(self.__tabela_principal, (key, valorListString))
			
		return key
	
	def pull(self, key):
		try:
			dados = self.__db.get_instance(self.__tabela_principal, ['id', key])[0][1]
			tipo = dados[:4]
			conteudo = dados[6:]
			
			if tipo == 'stri': return str(conteudo)
			elif tipo == 'inte': return int(conteudo)
			elif tipo == 'flot': return float(conteudo)
			elif tipo == 'list': return list(self.pull(i) for i in conteudo.split())
			elif tipo == 'tupl': return tuple(self.pull(i) for i in conteudo.split())

		except:
			return "Não foi possível encontrar o conteúdo..."
	
	def my_keys(self, filter='#'):
		keys = []
		for i in self.__db.get_table(self.__tabela_principal):
			if not i[0][0] == filter: keys.append(i[0])
		return keys

	def add(self, key, value):
		dados = self.__db.get_instance(self.__tabela_principal, ['id', key])[0][1]
		
		if dados[:4] == 'list' or dados[:4] == 'tupl':
			lastValue = dados
			new_value = lastValue + ' ' + self.push(key=None, valor=value)
			self.__db.edit_instance(self.__tabela_principal, ['id', key], 'valor', new_value)
		else:
			print(f'Key: {key} is not list or tuple.')

	def clean_key(self, key):
		try: 
			valor = self.__db.get_instance(self.__tabela_principal, ['id', key])[0][1]
			tipo = valor[:4]
			conteudo = valor[6:]

		except: return False

		if tipo == 'stri' or tipo == 'inte' or tipo == 'flot':
			self.__db.del_instance(self.__tabela_principal, ["id", key])
		elif tipo == 'list' or tipo == 'tupl':
			for i in conteudo.split(): self.clean_key(i)
			self.__db.del_instance(self.__tabela_principal, ["id", key])
		
		return True
	
if __name__ == '__main__':
	ed = EasyDb('database.db')
	print(ed.my_keys())
