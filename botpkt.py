import telebot
from telebot import types

bot=telebot.TeleBot("863794419:AAFbgl-ZNK83kc18_ra_Ky7wBhqqSj4hQ6Q")

admin=[]
clientes=[]
pedidos=[]
text_pedidos={}
clientes_step={}
nombre={}
apodo={}

commands={
	'start':'Para inicializar el bot',
	'help':'Para obtener ayuda acerca del bot'
}

#-1:Acaba de hacer start
#-2:Dijo que era cliente y va a introducir su nombre
#0:Le sale la opcion de introducir su direccion o cancelar
#1:Va a introduccir su direccion
#2:Le sale la opcion de Hacer Pedidos o ir a Ajustes a cambiar su direccion
#3:Enviar un comentario para su pedido
#4:Le sale la opcion de cancelar el pedido o recordatelo
#10:Introducir la contrasena de Admin
#11:Menu Principal de Admin
#12:Ver Pedidos activos
#13:Enviar texto para responder el pedido
#14:Ver clientes
#15:Enviar nuevo apodo
#
#
def Cargar():
	file=open("datos.txt",'r')
	for line in file.readlines():
		tokens=str.split(line," ")
		if tokens[0]=="admin":
			admin.append(int(tokens[1]))
			clientes_step[int(tokens[1])]=11
		elif tokens[0]=="client":
			clientes.append(int(tokens[1]))
			nombre[int(tokens[1])]=tokens[2]
			apodo[int(tokens[1])]=tokens[3]
			clientes_step[int(tokens[1])]=int(tokens[4])
		else:
			pedidos.append(int(tokens[1]))
			text=""
			words=str.split(tokens[2],'_')
			for a in words:
				text+=a
				text+=" "
			text_pedidos[int(tokens[1])]=text
	file.close()

def Guardar():
	file=open("datos.txt",'w')
	for item in clientes:
		if item in admin:
			file.write("admin "+str(item)+"\n")
		else:
			file.write("client "+str(item)+" "+nombre[item]+" "+apodo[item]+" "+clientes_step[item]+"\n")
	for item in pedidos:
		text=""
		temp=str.split(text_pedidos[item]," ")
		for a in temp:
			text+=a
			text+="_"
		file.write("pedido "+str(item)+" "+text)
	file.close()

cancelar=types.ReplyKeyboardMarkup(one_time_keyboard=True)
cancelar.add('Cancelar')
establecer_dir=types.ReplyKeyboardMarkup(one_time_keyboard=True)
establecer_dir.add('Establecer Direccion','Cancelar')
hacer_pedido=types.ReplyKeyboardMarkup(one_time_keyboard=True)
hacer_pedido.add('Hacer Pedido','Ajustes')
cancelar_pedido=types.ReplyKeyboardMarkup(one_time_keyboard=True)
cancelar_pedido.add('Cancelar Pedido','Recordar')
hideBoard = types.ReplyKeyboardRemove()
client_admin=types.ReplyKeyboardMarkup(one_time_keyboard=True)
client_admin.add('Cliente','Admin')
admin_main_menu=types.ReplyKeyboardMarkup(one_time_keyboard=True)
admin_main_menu.add('Ver Pedidos','Poner Apodo')
pedidos_page=types.ReplyKeyboardMarkup(one_time_keyboard=True)
pedidos_page.add('Responder Pedido','Terminar Pedido','Atras')
apodo_page=types.ReplyKeyboardMarkup(one_time_keyboard=True)


@bot.message_handler(commands=['start'])
def command_start(message):
	cid=message.chat.id
	if cid not in clientes:
		clientes.append(cid)
		clientes_step[cid]=-1
		bot.send_message(cid,"Bienvenido\n Que eres?",reply_markup=client_admin)
	else:
		bot.send_message(cid,"Ya estas registrado")
	Guardar()

@bot.message_handler(func= lambda message:clientes_step[message.chat.id]==-1)
def selector(message):
	cid=message.chat.id
	text=message.text
	if text == 'Cliente':
		clientes_step[cid]=-2
		bot.send_message(cid,"Introduzca su nombre",reply_markup=hideBoard)
	elif text =='Admin':
		clientes_step[cid]=10
		bot.send_message(cid,"Introduzca la contraseña",reply_markup=hideBoard)
	else:
		bot.send_message(cid,"Por favor use los botones predeterminados",reply_markup=client_admin)
	Guardar()

#Region Clientes
@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==-2)
def nombre_hecho(message):
	cid=message.chat.id
	text=message.text
	clientes_step[cid]=2
	bot.send_message(cid,"Guardado",reply_markup=hacer_pedido)
	nombre[cid]=text
	apodo[cid]=text
	Guardar()

#@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==0)
#def est_dir(message):
#	if message.text == 'Establecer Direccion':
#		clientes_step[message.chat.id]=1
#		bot.send_message(message.chat.id,"Envie su Direccion",reply_markup=hideBoard)
#	elif message.text=='Cancelar':
#		clientes_step[message.chat.id]=2
#		bot.send_message(message.chat.id,"Cancelado",reply_markup=hacer_pedido)
#	else :
#		bot.send_message(message.chat.id,"Por favor use los botones predeterminados",reply_markup=establecer_dir)
#
#@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==1)
#def save_dir(message):
#	cid=message.chat.id
#	direccion_clientes[cid]=message.text
#	clientes_step[cid]=2
#	bot.send_message(cid,"Direccion Guardada",reply_markup=hacer_pedido)

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==2)
def hacer_pedidos(message):
	cid=message.chat.id
	text=message.text
	if text == 'Hacer Pedido':
		clientes_step[cid]=3
		bot.send_message(cid,"Por favor escriba algun comentario a su pedido",reply_markup=cancelar)
	elif text=='Ajustes':
		clientes_step[cid]=0
		bot.send_message(cid,"Ajustes",reply_markup=establecer_dir)
	else:
		bot.send_message(cid,"Por favor use los botones predeterminados",reply_markup=hacer_pedido)
	Guardar()

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==3)
def comment_pedido(message):
	cid=message.chat.id
	text=message.text
	pedidos.append(cid)
	text_pedidos[cid]=text
	clientes_step[cid]=4
	bot.send_message(cid,"Su pedido ha sido enviado correctamente.",reply_markup=cancelar_pedido)
	for ad in admin:
		bot.send_message(ad,"El cliente "+nombre[cid]+" ["+apodo[cid]+"]"+" :\n"+text)
	Guardar()

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==4)
def pedido_hecho(message):
	cid=message.chat.id
	text=message.text
	if text == 'Cancelar Pedido':
		for ad in admin:
			bot.send_message(ad,"El cliente "+apodo[cid]+" :\n"+text)
		pedidos.remove(cid)
		bot.send_message(cid,"Pedido Cancelado",reply_markup=hacer_pedido)
		clientes_step[cid]=2
	elif text == 'Recordar':
		for ad in admin:
			bot.send_message(ad,"El cliente "+apodo[cid]+" te recuerda que:\n"+text_pedidos[cid])
		bot.send_message(cid,"Recordatorio Enviado")
	else :
		bot.send_message(cid,"Por favor use los botones predeterminados",reply_markup=cancelar_pedido)
	Guardar()
#EndRegion

#Region Admin

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==10)
def check_password(message):
	cid=message.chat.id
	text=message.text
	if text== 'C@brera.':
		clientes_step[cid]=11
		bot.send_message(cid,"Correcto",reply_markup=admin_main_menu)
	else:
		clientes_step[cid]=-1
		bot.send_message(cid,"Incorrecto",reply_markup=client_admin)
	Guardar()

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==11)
def main_admin(message):
	cid=message.chat.id
	text=message.text
	if text=='Ver Pedidos':
		a="Pedidos Activos :\n"
		index=0
		for item in pedidos:
			a+=nombre[item]+" ["+apodo[item]+"] :"+text_pedidos[item]+" /responder_pedido_"+index+" /teminar_pedido_"+index+"\n"
			index+=1
		bot.send_message(cid,a,reply_markup=hideBoard)
		clientes_step[cid]=12
	elif text=='Poner Apodo':
		a="Clientes :\n"
		index=0
		for item in clientes:
			a+=nombre[item]+" ["+apodo[item]+"] /cambiar_apodo_"+index
			index+=1
		bot.send_message(cid,a,reply_markup=hideBoard)
		clientes_step[cid]=14
	else :
		bot.send_message(cid,"Comando No Encontrado",reply_markup=admin_main_menu)
	Guardar()

id_to_send=0
@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==12)
def main_admin(message):
	cid=message.chat.id
	text=message.text
	tokens=str.split(text,'_')
	if tokens[0]=="/responder":
		p=int(tokens[2])#El numero de pedido
		id_to_send=pedidos[p]
		clientes_step[cid]=13
		bot.send_message(cid,"Envie su respuesta",reply_markup=hideBoard)
	#Verificar si es terminar pedido y cual es
	elif tokens[0]=="/terminar":
		p=int(tokens[2])#El numero de pedido
		pedido.remove(pedidos[p])
		clientes_step[cid]=11
		bot.send_message(cid,"Pedido Removido",reply_markup=admin_main_menu)
	else:
		clientes_step[cid]=11
		bot.send_message(cid,"Comando no Encontrado",reply_markup=admin_main_menu)
	Guardar()

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==13)
def main_admin(message):
	cid=message.chat.id
	text=message.text
	bot.send_message(id_to_send,"Respuesta a su Pedido:\n"+text)
	clientes_step[cid]=11
	bot.send_message(cid,"Respuesta Enviada",reply_markup=admin_main_menu)
	Guardar()

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==14)
def main_admin(message):
	cid=message.chat.id
	text=message.text
	#Verificar si es cambiar y a cual
	tokens=str.split(text,'_')
	if tokens[0]=="/cambiar":
		p=int(tokens[2])#Numero
		id_to_send=clientes[p]
		clientes_step[cid]=15
		bot.send_message(cid,"Introduzca el apodo nuevo",reply_markup=hideBoard)
	else:
		clientes_step[cid]=11
		bot.send_message(cid,"Comando no Encontrado",reply_markup=admin_main_menu)
	Guardar()

@bot.message_handler(func=lambda message:clientes_step[message.chat.id]==15)
def main_admin(message):
	cid=message.chat.id
	text=message.text
	apodo[id_to_send]=text
	clientes_step[cid]=11
	bot.send_message(cid,"Apodo Cambiado",reply_markup=admin_main_menu)
	Guardar()
#EndRegion
Cargar()
bot.polling()





	