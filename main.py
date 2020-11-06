import pyinputplus
from bot import Bot

user =  input('Ingrese su usuario de Instagram: ')
passw = pyinputplus.inputPassword('Ingresa tu Contaseña: ','*')

insta = Bot()
insta.iniciar_sesion(user, passw)
insta.quitar_mensajes()

datos = insta.buscar_perfil(user)
noMeSiguen, noSigo, enComun = insta.comparacion(insta.listaSiguiendo,insta.listaSeguidores)

insta.browser.minimize_window()

mensaje_detalle = f'''
--- Sigues a {datos["seguidos"]} personas y te siguen {datos["seguidores"]} personas ---

=> No te siguen: {len(noMeSiguen)} personas
=> No sigues: {len(noSigo)} personas
=> Seguidores en común: {len(enComun)} personas

--- ¿Quieres ver quienes son estas personas? ---
=> Si [S]
=> No [N]

=> Salir [SR]
'''

mensaje_tipo_detalle = '''
--- ¿Qué detalle quieres ver? ---
=> No me siguen [NMS]
=> No sigo [NS]
=> En comun => [C]

=> Salir [SR]
'''

mensaje_unfollow = '''
--- ¿Quieres dejar de seguir a quienes no te siguen? ---
=> Si [S]
=> No [N]
'''

while True:
    respuesta_detalle = input(mensaje_detalle)
    # ¿Quieres ver quienes son estas personas?
    if respuesta_detalle == 'S':
        # Que detalle quieres ver?
        respuesta_tipo_detalle = input(mensaje_tipo_detalle)
        if respuesta_tipo_detalle == 'NMS':
            print(noMeSiguen)
        elif respuesta_tipo_detalle == 'NS':
            print(noSigo)
        elif respuesta_tipo_detalle == 'C':
            print(enComun)
        elif respuesta_tipo_detalle == 'SR':
            print('Saliendo...')
            break
        else:
            print(f'{respuesta_tipo_detalle} no es una opción válida')
            continue
    elif respuesta_detalle == 'SR':
        print('Saliendo...')
        break
    elif respuesta_detalle != 'N':
        print(f'{respuesta_detalle} no es una opción válida')
        continue
    
    # Quieres dejar de seguir?
    respuesta_unfollow = input(mensaje_unfollow)
    if respuesta_unfollow == 'S':
        insta.browser.maximize_window()
        insta.unfollow(noMeSiguen)
    elif respuesta_unfollow == 'N':
        continue
    else:
        print(f'{respuesta_detalle} no es una opción válida')
 
insta.browser.quit()
