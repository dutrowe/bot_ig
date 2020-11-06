import pyautogui, datetime
from selenium import webdriver
from time import sleep
from collections import Counter



class Bot:

    url = 'https://www.instagram.com/'
    
    btn_iniciar_sesion = '//*[@id="loginForm"]/div/div[3]/button'
    btn_sesion_auto = '//*[@id="react-root"]/section/main/div/div/div/section/div/button'
    btn_activar_noti = '/html/body/div[4]/div/div/div/div[3]/button[2]'
    numero_seguidores = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'
    numero_siguiendo = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
    scroll_seguidores = '/html/body/div[5]/div/div/div[2]'
    btn_cerrar_ventana = '/html/body/div[5]/div/div/div[1]/div/div[2]/button'
    barra_busqueda = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'
    btn_usuario = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]'
    btn_amistad = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button'
    btn_unfollow = '/html/body/div[5]/div/div/div/div[3]/button[1]'

    def __init__(self):
        """
        Pide el nombre de usuario y contraseña de IG
        Abre el navegador y muestra el website de IG
        """
        # Debes descargar el web driver para tu navegador y hacer referencia a la ubicación
        # en donde está guardado.
        self.browser = webdriver.Chrome('./chromedriver')
        self.browser.get(self.url)
        self.browser.maximize_window()

    def iniciar_sesion(self, usuario, password):
        """
        Inicia sesión en IG
        """        
        # Esperamos un momento a que la página cargue en su totalidad
        sleep(5)

        # Escribimos y enviamos el usuario y contraseña
        self.browser.find_element_by_name('username').send_keys(usuario)
        # @todo => por qué asigno esto a una variable? WTF
        contraseña = self.browser.find_element_by_name('password').send_keys(password)
        sleep(2)
        self.browser.find_element_by_xpath(self.btn_iniciar_sesion).click()

    def quitar_mensajes(self):
        """
        Nos encargamos de los mensajes de inicio de sesión automático
        y de activar notificaciones
        """
        sleep(5)
        # Inicio de Sesión Automático
        self.browser.find_element_by_xpath(self.btn_sesion_auto).click()

        sleep(5)
        # Hace click en "Ahora No", en el mensaje de activar notificaciones
        self.browser.find_element_by_xpath(self.btn_activar_noti).click()

    def buscar_perfil(self, usuario):
        """
        Entra a mi perfil y retorna la cantidad de personas a las que sigo
        y la cantidad de personas que me siguen
        """
        #Entra a mi perfil
        self.browser.find_element_by_link_text(usuario).click()

        #cantidad de followers y no followers
        sleep(3)
        cantidadDeSeguidores = int(self.browser.find_element_by_xpath(self.numero_seguidores).text)
        cantidadSigues = int(self.browser.find_element_by_xpath(self.numero_siguiendo).text)

        diccionario = {
            'seguidores': cantidadDeSeguidores,
            'seguidos': cantidadSigues
        }

        return diccionario

    def comparacion(self, lista1, lista2):
        """
        Compara los valores que hay en dos listas y los retorna
        """
        lista1_si_lista2_no = []
        lista1_no_lista2_si = []
        lista1_si_lista2_si = []

        for item in lista1:
            if item in lista2:
                lista1_si_lista2_si.append(item)
            else:
                lista1_si_lista2_no.append(item)
        
        for item in lista2:
            if item not in lista1:
                lista1_no_lista2_si.append(item)

        return lista1_si_lista2_no, lista1_no_lista2_si, lista1_si_lista2_si

    @property
    def listaSeguidores(self):
        #Selecciona mis seguidores
        self.browser.find_element_by_partial_link_text('seguidores').click()

        #scrollbox
        sleep(2)
        scrollbox = self.browser.find_element_by_xpath(self.scroll_seguidores)
                
        #links
        # links = scrollbox.find_elements_by_tag_name('a')

        pyautogui.moveTo(662,393)

        llegoAlFinal = False
        cantidad = []

        # inicio = datetime.datetime.now()
        while llegoAlFinal != True:
            links = scrollbox.find_elements_by_tag_name('a')

            # List que contiene "Web Elements"
            print(f'links => {type(links)}')

            cantidad.append(len(links))

            print(f'len(links) => {len(links)}')

            print(f'cantidad => {cantidad}')

            print(f'Counter(cantidad) => {Counter(cantidad)}')

            print(f'dict(Counter(cantidad)) => {dict(Counter(cantidad))}')

            print(f'dict(Counter(cantidad)).items() => {dict(Counter(cantidad)).items()}')

            print(f'list(dict(Counter(cantidad)).items()) => {list(dict(Counter(cantidad)).items())}')

            ocurrencias = list(dict(Counter(cantidad)).items())
            for key, value in ocurrencias:
                if value > 7:
                    llegoAlFinal = True
            pyautogui.scroll(-1000)
            sleep(2)

        nombres = [name.text for name in links if name.text != '']


        # final = datetime.datetime.now()

        self.browser.find_element_by_xpath(self.btn_cerrar_ventana).click()

        return nombres

    @property
    def listaSiguiendo(self):
        siguiendo = []
        #Selecciona las personas a las que sigo
        self.browser.find_element_by_partial_link_text('seguidos').click()

        #scrollbox de seguidos
        sleep(3)
        scrollboxSeguidos = self.browser.find_element_by_xpath(self.scroll_seguidores)

        #links Seguidos
        linksSeguidos = scrollboxSeguidos.find_elements_by_tag_name('a')

        #mueve el mouse al scrollbox
        pyautogui.moveTo(662,393)

        inicio = datetime.datetime.now()
        
        llegoAlFinal = False
        cantidad = []
        
        while llegoAlFinal != True:
            linksSeguidos = scrollboxSeguidos.find_elements_by_tag_name('a')
            cantidad.append(len(linksSeguidos))
            ocurrencias = list(dict(Counter(cantidad)).items())
            for key, value in ocurrencias:
                if value > 7:
                    llegoAlFinal = True
            pyautogui.scroll(-1000)
            sleep(2)

        siguiendo = [name.text for name in linksSeguidos if name.text != '']

        final = datetime.datetime.now()

        self.browser.find_element_by_xpath(self.btn_cerrar_ventana).click()

        return siguiendo
    
    def unfollow(self, lista_de_usuarios):
        """
        Dejar de seguir a quienes no te siguen
        """
        for usuario in lista_de_usuarios:
            sleep(5)
            self.browser.find_element_by_xpath(self.barra_busqueda).send_keys(usuario)
            sleep(5)
            self.browser.find_element_by_xpath(self.btn_usuario).click()
            sleep(5)
            self.browser.find_element_by_xpath(self.btn_amistad).click()
            sleep(5)
            self.browser.find_element_by_xpath(self.btn_unfollow).click()
