
# repocitorio de documentacion  https://github.com/fananimi/pyzk

from pyzkfp import ZKFP2
from pyzkfp._construct.errors_handler import AlgorithmLibraryInitializationError
import time
import os
import platform
import sys

class Fingerprint():

    def __init__(self):

        self.zkfp2 = ZKFP2()

    def clear_console(self):
        # Determina el sistema operativo
        current_os = platform.system()

        if current_os == "Windows":
            # Si es Windows, usa 'cls'
            os.system('cls')
        else:
            # Si es Unix/Linux/Mac, usa 'clear'
            os.system('clear')

    def animate_message(self, message, duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            for suffix in ['', '.', '..', '...']:
                sys.stdout.write(f'\r{message}{suffix}')
                sys.stdout.flush()
                time.sleep(0.5)
                time.sleep(2)
                try:
                    self.device_fingerprint()
                    print('reconocido')
                    return True
                except:
                    print('no')
                    
        sys.stdout.write('\r' + ' ' * (len(message) + 3) + '\r')  # Clear the line after the animation



    def consultar(self):
        print('ponga la huella')
        for i in range(3):
            while True:
                capture = self.zkfp2.AcquireFingerprint()
                if capture:
                    tmp, img = capture
                    fingerprint_id, score = self.zkfp2.DBIdentify(tmp)
                    # print(f'usuario registrado con id: {fingerprint_id}')
                    # res = self.zkfp2.DBMatch(tmp, fingerprint_id) # returns 1 if match, 0 if not
                    # if res == 1:
                    if fingerprint_id == 1:
                        print('usuario registrado')
                        time.sleep(3)
                        return True
                    else:
                        print('No se econtro el usuario, intenta de nuevo')
                        break
        self.clear_console()
        print('No se econtro el usuario')
        time.sleep(3)

    def registrar(self):
        print('ponga la huella 3 veces')
        conH = 0
        templates = []
        id_input = int(input('ingresa id: '))
        for i in range(3):
            if conH != 0:
                print('poner huella Nuevamente')

            while True:
                capture = self.zkfp2.AcquireFingerprint()
                if capture:
                    print(capture)
                    print('fingerprint captured')
                    tmp, img = capture
                    print(tmp)
                    templates.append(tmp)
                    self.zkfp2.show_image(img) # requires Pillow lib
                    break
        regTemp, regTempLen = self.zkfp2.DBMerge(*templates)
        print(regTemp)
        print(regTempLen)
        # Store the template in the device's database
        finger_id = id_input # The id of the finger to be registered
        self.zkfp2.DBAdd(finger_id, regTemp)
        print('Usuario registrado con Exito..!')
        time.sleep(3)

    def device_fingerprint(self):

        self.zkfp2.Init() # Initialize the ZKFP2 class
        # Get device count and open first device
        device_count = self.zkfp2.GetDeviceCount()
        print(f"{device_count} devices found")
        self.zkfp2.OpenDevice(0) # connect to the first device

    def main(self):

        while True:
            try:
                self.device_fingerprint()
                while True:
                        self.clear_console()
                        accion = input("""
                            Hola que accion deseas realizar 
                                1. Registrar 
                                2. Consultar
                                3. Salir
                        """
                        )

                        if accion == '1':
                            self.registrar()
                        elif accion == '2':
                            self.consultar()
                        elif accion == '3':
                            return
                        else:
                            print("Escoge una opcion valida")
            except AlgorithmLibraryInitializationError as e:
                print(f"Error al inicializar: {e}")
                self.animate_message("Conecta el huellero", 10)
                self.clear_console()


if __name__ == "__main__":
    f = Fingerprint()
    f.main()
