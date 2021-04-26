import datetime as dt
import random
import sys
import time
import vk_api
sys.path.insert(0, '../')

from validate_email import validate_email
from pymongo import MongoClient
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload

from data import token, password

AllText = []
admin_id = []
dialog_id = []

def init():
	global cluster, db, TextColl, vk_session, vk, upload, id_group, longpoll

	print('Началась инициализцаия программы')
	connectionVK = False
	connectionDB = False
	while not connectionDB:
		try:
			cluster = MongoClient(f'mongodb+srv://admin:{password}@cluster0.e4imk.mongodb.net/LibraryDataBase?retryWrites=true&w=majority')
			db = cluster["LibraryDataBase"]
			TextColl = db["TextForBot"]
			connectionDB = True
			print("CONNECTED TO DATABASE")
		except Exception as error:
			print(error)
			time.sleep(5)
	while not connectionVK:
		try:
			vk_session = vk_api.VkApi(token=token)
			vk = vk_session.get_api()
			upload = VkUpload(vk)
			id_group = vk_session.method('groups.getById')[0]['id']
			longpoll = VkBotLongPoll(vk_session, id_group, wait = 15)
			UpdateText()
			UpdateAdminId()
			connectionVK = True
			print("CONNECTED TO VK.SERVER")
		except Exception as error:
			print(error)
			time.sleep(5)

def UpdateText():
	AllText.clear()
	for text in TextColl.find().sort("_id"):
		AllText.append(text["text"])

def UpdateAdminId():
	admin_id.clear()
	admins = vk_session.method('groups.getMembers', {'group_id': id_group, 'filter': "managers"})
	for user_id in admins['items']:
		admin_id.append(user_id['id'])

def search_ticket(peer_id):
	date = dt.datetime.now(tz=None).strftime('%d%m%Y')
	num_mes = vk_session.method('messages.search', {'peer_id': peer_id, 'count': 3, 'date': date})
	number = num_mes['items'][2]['text']
	return number

def add_photo(photo):
	response = upload.photo_messages(photo)[0]
	access_key = response['access_key']
	owner_id = response['owner_id']
	photo_id = response['id']
	return f'photo{owner_id}_{photo_id}_{access_key}'

def format(text, type):
	if (type == 'number'):
		result = (text[0:2].isdigit()) and (text[2:3]=='-') and (text[3:].isdigit() and (len(text) == 9))
	elif (type == 'email'):
		result = ((text.find('@') < text.rfind('.')) and (validate_email(text)))
	else:
		print("WRONG FORMAT TYPE")
		result = None
	return result

def get_user_name(user_id):
	return vk_session.method('users.get', {'user_ids': user_id})[0]['first_name']

def keyboard(type):
	if(type == 1):
		keyboard = VkKeyboard(one_time = False, inline = False)
		keyboard.add_vkapps_button(app_id = 5887784, owner_id = -165584339, hash = '',label = 'Аренда коворкинга')
		keyboard.add_openlink_button(label = 'Полезные статьи', link = 'https://vk.com/@rzhevka_lib')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 6013442, owner_id = -17047312, hash = 'form_id=1', label = 'Организация события')
		keyboard.add_button(label = 'Где мы и время работы', color = 'secondary')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 5575136, owner_id = -17047312, hash = '',label = 'Афиша')
		keyboard.add_button(label = 'Продлить книгу', color = 'secondary')
	elif(type == 2):
		keyboard = VkKeyboard(one_time = False, inline = False)
		keyboard.add_button(label = 'Назад в меню', color = 'negative')
	elif(type == 3):
		keyboard = VkKeyboard(one_time = False, inline = False)
		keyboard.add_vkapps_button(app_id = 5887784, owner_id = -165584339, hash = '',label = 'Аренда коворкинга')
		keyboard.add_openlink_button(label = 'Полезные статьи', link = 'https://vk.com/@rzhevka_lib')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 6013442, owner_id = -17047312, hash = 'form_id=1', label = 'Организация события')
		keyboard.add_button(label = 'Где мы и время работы', color = 'secondary')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 5575136, owner_id = -17047312, hash = '',label = 'Афиша')
		keyboard.add_button(label = 'Продлить книгу', color = 'secondary')
		keyboard.add_line()
		keyboard.add_button(label = 'Вывести меню', color = 'positive')
	elif(type == 4):
		keyboard = VkKeyboard(one_time = True, inline = False)
		keyboard.add_button(label = 'Да', color = 'positive')
		keyboard.add_button(label = 'Нет', color = 'negative')
		keyboard.add_line()
		keyboard.add_button(label = 'Назад в меню', color = 'secondary')
	elif(type == 5):
		keyboard = VkKeyboard(one_time = False, inline = False)
		keyboard.add_vkapps_button(app_id = 5887784, owner_id = -165584339, hash = '',label = 'Аренда коворкинга')
		keyboard.add_openlink_button(label = 'Полезные статьи', link = 'https://vk.com/@rzhevka_lib')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 6013442, owner_id = -17047312, hash = 'form_id=1', label = 'Организация события')
		keyboard.add_button(label = 'Где мы и время работы', color = 'secondary')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 5575136, owner_id = -17047312, hash = '',label = 'Афиша')
		keyboard.add_button(label = 'Продлить книгу', color = 'secondary')
		keyboard.add_line()
		keyboard.add_button(label = 'Изменить текст сообщений', color = 'negative')
		keyboard.add_button(label = 'Контакты', color = 'secondary')
	elif(type == 6):
		keyboard = VkKeyboard(one_time = False, inline = False)
		keyboard.add_vkapps_button(app_id = 5887784, owner_id = -165584339, hash = '',label = 'Аренда коворкинга')
		keyboard.add_openlink_button(label = 'Полезные статьи', link = 'https://vk.com/@rzhevka_lib')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 6013442, owner_id = -17047312, hash = 'form_id=1', label = 'Организация события')
		keyboard.add_button(label = 'Где мы и время работы', color = 'secondary')
		keyboard.add_line()
		keyboard.add_vkapps_button(app_id = 5575136, owner_id = -17047312, hash = '',label = 'Афиша')
		keyboard.add_button(label = 'Продлить книгу', color = 'secondary')
		keyboard.add_line()
		keyboard.add_button(label = 'Вывести меню', color = 'positive')
		keyboard.add_button(label = 'Контакты', color = 'secondary')
		keyboard.add_button(label = 'Изменить текст сообщений', color = 'negative')
	return keyboard

def check_change_message(text):
	try:
		if(int(text)==float(text)):
			if(int(text)!=0):
				return True
			else:
				return False
	except Exception as e:
		print(e)
	return False

def message_for_admins(text):
	for user_id in admin_id:
		send_message(user_id, text, '','')

def search_message(text, peer_id, count = 20):
	search = vk_session.method('messages.search', {'q': text, 'peer_id': peer_id, 'count': count})
	return search

def send_message(user_id, text, attachment, keyboard):
	if(keyboard != ''):
		vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'attachment': attachment, 'random_id': random.randint(-2147483648,+2147483648), 'keyboard':keyboard.get_keyboard(), 'dont_parse_links': 0})
	else:
		vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'attachment': attachment, 'random_id': random.randint(-2147483648,+2147483648), 'dont_parse_links': 0})

def main():
	error_count = 0
	init()
	while (error_count < 20):
		try:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					response = event.obj.message['text'].lower()
					user_id = event.obj.message['from_id']
					last_message_from_bot = ''
					UpdateAdminId()
					try:
						last_message_from_bot = vk_session.method('messages.getHistory', {'count': 2, 'user_id': user_id})['items'][1]['text']
					except Exception as error:
						print(error)
					if (event.from_user):
						if last_message_from_bot =='':
							send_message(user_id = user_id, text = "Добро пожаловать в нашу группу!", attachment = '', keyboard = '')
							send_message(user_id = user_id, text = 'Я чат-бот библиотеки "Ржевская". Меня создали для помощи специально вам, ' + (get_user_name(event.obj.message['from_id'])) + '. Вот, что я могу:', attachment = '', keyboard = '')
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
							else:
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(1))
						elif (last_message_from_bot == AllText[6]):#Тут начало продления книги
							if((response.find('назад') != (-1)) or (response.find('меню') != (-1))):
								send_message(user_id = user_id, text = 'Возвращаю вас в главное меню.', attachment = '', keyboard = '')
								if(user_id in admin_id):
									send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
								else:
									send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(1))
							else:
								if(format(response, 'number')):
									send_message(user_id = user_id, text = 'Введите свою почту:', attachment = '', keyboard = keyboard(2))
								else:
									send_message(user_id = user_id, text = 'Введен неверный номер билета, повторите ввод.', attachment = '', keyboard = '')
									send_message(user_id = user_id, text = AllText[6], attachment = '', keyboard = keyboard(2))
						elif (last_message_from_bot == 'Введите свою почту:'):
							if((response.find('назад') != (-1)) or (response.find('меню') != (-1))):
								send_message(user_id = user_id, text = 'Возвращаю вас в главное меню.', attachment = '', keyboard = '')
								if(user_id in admin_id):
									send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
								else:
									send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(1))
							else:
								if(format(response, 'email')):
									mail = response
									ticket_number = search_ticket(user_id)
									ticket_text = 'Запрос на продление книги от ' + '@id' + str(user_id) + ' (' +str((get_user_name(event.obj.message['from_id']))) + '):\nНомер билета: ' + str(ticket_number) + '\nАдресс эл. почты: ' + str(mail)
									message_for_admins(ticket_text)
									send_message(user_id = user_id, text = 'Ваша заявка была принята, ответ будет отправлен на почту. Возвращаю вас в главное меню.', attachment = '', keyboard = '')
									if(user_id in admin_id):
										send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
									else:
										send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(1))
								else:
									send_message(user_id = user_id, text = 'Введен неверный адрес электронной почты, повторите ввод.', attachment = '', keyboard = '')
									send_message(user_id = user_id, text = AllText[6], attachment = '', keyboard = keyboard(2))
						elif ((response.find('измен')!=(-1)) and (user_id in admin_id)):
							send_message(user_id = user_id, text = "Введите номер сообщения для его изменения:\n1 - Аренда коворкинга\n2 - Организация события\n3 - Афиша\n4 - Полезные статьи\n5 - Где мы и время работы\n6 - Продлить книгу\n7 - Контакты", attachment = '', keyboard = '')
						elif ((last_message_from_bot =="Введите номер сообщения для его изменения:\n1 - Аренда коворкинга\n2 - Организация события\n3 - Афиша\n4 - Полезные статьи\n5 - Где мы и время работы\n6 - Продлить книгу\n7 - Контакты") and (user_id in admin_id)):
							if((response.isdigit()) and (check_change_message(response))):
								send_message(user_id = user_id, text = "Вывожу прежнее сообщение по номеру " + response + "\n\n" + AllText[int(response)] + "\n\nНапишите сообщение для замены. Если вы не хотите производить замену напишите\n Отмена", attachment = '', keyboard = '')
							else:
								send_message(user_id = user_id, text = "Введен неверный номер, вывожу основное меню.", attachment = '', keyboard = '')
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
						elif ((last_message_from_bot.find('Вывожу прежнее сообщение по номеру ') != (-1)) and (user_id in admin_id)):
							if(response != 'отмена'):
								send_message(user_id = user_id, text = "Замена успешно произведена", attachment = '', keyboard = '')
								last_text = vk_session.method('messages.getHistory', {'count': 2, 'user_id': user_id})['items'][1]['text']
								TextColl.update_one({"_id": int(last_message_from_bot[35]) + 1}, {"$set": {"text": last_text}})
								UpdateText()
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
							else:
								send_message(user_id = user_id, text = "Замена сообщения не была произведена, вывожу меню.", attachment = '', keyboard = '')
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
						elif ((response.find('назад') != (-1)) or (response.find('меню') != (-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(5))
							else:
								send_message(user_id = user_id, text = AllText[0], attachment = '', keyboard = keyboard(1))
						elif ((response == '1') or (response.find('аренд')!=(-1)) or (response.find('коворк')!=(-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[1], attachment = '', keyboard = keyboard(6))
							else:
								send_message(user_id = user_id, text = AllText[1], attachment = '', keyboard = keyboard(3))
						elif ((response == '2') or (response.find('организ')!=(-1)) or (response.find('событ')!=(-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[2], attachment = '', keyboard = keyboard(6))
							else:
								send_message(user_id = user_id, text = AllText[2], attachment = '', keyboard = keyboard(3))
						elif ((response == '3') or (response.find('афиш')!=(-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[3], attachment = '', keyboard = keyboard(6))
							else:
								send_message(user_id = user_id, text = AllText[3], attachment = '', keyboard = keyboard(3))
						elif ((response == '4') or (response.find('стать')!=(-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[4], attachment = '', keyboard = keyboard(6))
							else:
								send_message(user_id = user_id, text = AllText[4], attachment = '', keyboard = keyboard(3))
						elif ((response == '5') or (response.find('время')!=(-1)) or (response.find('где')!=(-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[5], attachment = add_photo('map.jpg'), keyboard = keyboard(6))
							else:
								send_message(user_id = user_id, text = AllText[5], attachment = add_photo('map.jpg'), keyboard = keyboard(3))
						elif ((response == '6') or (response.find('продл')!=(-1))):
							send_message(user_id = user_id, text = AllText[6], attachment = '', keyboard = keyboard(2))
						elif ((response == '7') or (response.find('контакт')!=(-1))):
							if(user_id in admin_id):
								send_message(user_id = user_id, text = AllText[7], attachment = '', keyboard = keyboard(6))
							else:
								send_message(user_id = user_id, text = AllText[7], attachment = '', keyboard = keyboard(3))
						else:
							if(user_id in admin_id):
								send_message(user_id = user_id, text = "Не понимаю, чего вы от меня хотите :(\nВоспользуйтесь меню или свяжитесь с администраторами группы, они точно смогут вам помочь.\n\n" + AllText[7], attachment = '', keyboard = keyboard(5))
							else:
								send_message(user_id = user_id, text = "Не понимаю, чего вы от меня хотите :(\nВоспользуйтесь меню или свяжитесь с администраторами группы, они точно смогут вам помочь.\n\n" + AllText[7], attachment = '', keyboard = keyboard(1))
						# elif (response == 'ссылка'):
						# 	url = 'https://vk.com/gim199300686?sel=' + str(user_id)
						# 	message_for_admins('Вот ссылка на беседу с @id' + str(user_id) + ' (' +str((get_user_name(event.obj.message['from_id']))) + '):\nСсылка: ' + url)
		except Exception as error:
			error_count += 1
			print(error)
	main()

main()