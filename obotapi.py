from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

class OG(object):
	
	
	def __init__(self, user, pwd, uni):
		self.browser = RoboBrowser(parser='html.parser')
		self.browser.open('https://es.ogame.gameforge.com:443/main/login')
		self.user = user
		self.pwd = pwd
		self.uni = uni
		self.loggin(user, pwd, uni)
		
	def loggin(self, user, pwd, uni):
		login_form = self.browser.get_form(id='loginForm')
		login_form['login'].value = user
		login_form['pass'].value = pwd
		login_form['uni'].value = uni
		
		self.browser.submit_form(login_form)
	
	def get_resources(self, planet):
		self.browser.open('https://s149-es.ogame.gameforge.com/game/index.php?page=overview&cp=' + planet)
		metal = self.browser.select('#resources_metal')
		cristal = self.browser.select('#resources_crystal')
		deuterio = self.browser.select('#resources_deuterium')
		materia_oscura = self.browser.select('#resources_darkmatter')
		energia = self.browser.select('#resources_energy')
	
		res = {'metal':metal[0].string.strip(),
				'cristal':cristal[0].string.strip(),
				'deuterio':deuterio[0].string.strip(),
				'materia_oscura':materia_oscura[0].string.strip(),
				'energia':energia[0].string.strip()
		}
		
		return res
	
	def get_cons_queue(self):
		
		self.browser.open('https://s149-es.ogame.gameforge.com/game/index.php?page=overview')
		desarrollos = self.browser.select('table.construction')
		desarrollos_header = self.browser.select('.content-box-s .header h3')
		desarrollos_nombre = [None]*3
		desarrollos_to_level = [None]*3
		desarrollos_time_left = [None]*3
		
		j = 0
		for i in desarrollos:
			#desarrollos_nombre
			if i.select('td.idle'):
				desarrollos_nombre[j] = BeautifulSoup('<mitag>None</mitag>', 'html.parser')
			else:
				desarrollos_nombre[j] = i.select('th')[0]
				
			#desarrollos_to_level
			if i.select('span.level'):
				desarrollos_to_level[j] = i.select('span.level')[0]
			else:
				desarrollos_to_level[j] = BeautifulSoup('<mitag>None</mitag>', 'html.parser')
			
			#desarrollos_time_left
			if i.select('td.timer span'):
				desarrollos_time_left[j] = i.select('td.timer span')[0]
			else:
				desarrollos_time_left[j] = BeautifulSoup('<mitag>None</mitag>', 'html.parser')
			
			j+=1
				
		res = {'ed_q':[desarrollos_header[0], desarrollos_nombre[0], desarrollos_to_level[0], desarrollos_time_left[0]],		#Edificios
				'in_q':[desarrollos_header[1], desarrollos_nombre[1], desarrollos_to_level[1], desarrollos_time_left[1]],		#Investigacion
				'ha_q':[desarrollos_header[2], desarrollos_nombre[2], desarrollos_to_level[2], desarrollos_time_left[2]]		#Hangar
		}
		
		return res
	
	def build_cool_stuff(self, stuff, building_type, planet, modus='1'):
		#TODO - Completar diccionario
		cons_dict = {'mina_metal':'1',
				'mina_cristal':'2',
				'mina_deuterio':'3',
				'mina_energia':'4',
				'almacen_metal':'22',
				'almacen_cristal':'23',
				'almacen_deuterio':'24',
				'cazador_ligero':'204',
				'cazador_pesado':'205',
				'nave_carga_p':'202',
				'nave_carga_g':'203',
				'sonda_espionaje':'210',
				'lanzamisiles':'401',
				'laser_p':'402',
				'laser_g':'403',
				'fabrica_robots':'14',
				'tec_blin':'111'
		}
		
		
		self.browser.open('https://s149-es.ogame.gameforge.com/game/index.php?page=' + building_type + '&cp=' + planet)
		
		build_form = self.browser.get_form(action = 'https://s149-es.ogame.gameforge.com/game/index.php?page=' + building_type + '&deprecated=1')
		
		type = cons_dict[stuff]
		if building_type != 'research':
			token = build_form['token'].value 
			data = {'token':token,
					'type':type,
					'modus':modus
			}
		else:
			data = {'type':type,
					'modus':modus
			}
		response = self.browser.session.post('https://s149-es.ogame.gameforge.com/game/index.php?page=' + building_type + '&deprecated=1', data)
		
		print(response)
		
		
		
		
		
		
	