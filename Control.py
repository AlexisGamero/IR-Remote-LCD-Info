import serial
import pyautogui
import winsdk.windows.media.control as media_control
import asyncio

arduino = serial.Serial('COM9', 9600)

async def media():
    while True:
    # Obtener el administrador de sesiones multimedia
        session_manager = await media_control.GlobalSystemMediaTransportControlsSessionManager.request_async()

    # Obtener la sesión actual
        current_session = session_manager.get_current_session()

        if current_session:
        # Obtener la información multimedia de la sesión actual
            media_info = await current_session.try_get_media_properties_async()

            if (media_info.title.__len__() < 16):
                title = media_info.title.ljust(16,' ')
            else:
                title = media_info.title
            if (media_info.artist.__len__() < 16):
                artist = media_info.artist.ljust(16,' ')
            else:
                artist = media_info.artist
        
            arduino.write(title.encode('ascii','ignore')[:16] + artist.encode('ascii','ignore')[:16] + '.'.encode('ascii'))
            await asyncio.sleep(2)
        else:
            print("No hay sesión multimedia activa.")
    #await asyncio.sleep(1)

async def control():
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().strip()
            print(data);
            # Ejecuta acciones según los datos recibidos
            if data == b'3':
                pyautogui.press('playpause')
                print("Play-Pause")
            elif data == b'0':
                pyautogui.press('volumeup')
                print("Volume Up")
            elif data == b'4':
                pyautogui.press('volumedown')
                print("Volume Down")
            elif data == b'2':
                pyautogui.press('nexttrack')
                print("Next track")
            elif data == b'1':
                pyautogui.press('prevtrack')
                print("Previous Track")
            elif data == b'16':
                pyautogui.press('stop')
                print("Stop")
            elif data == b'19':
                pyautogui.move(10,0)
                print("Cursor Right")
            elif data == b'1A':
                pyautogui.move(0,-10)
                print("Cursor Up")
            elif data == b'18':
                pyautogui.move(-10,0)
                print("Cursor Left")
            elif data == b'17':
                pyautogui.move(0,10)
                print("Cursor Down")
            elif data == b'15':
                pyautogui.click()
                print("Click")
        await asyncio.sleep(0)

async def main():
    tarea_media = asyncio.create_task(media())
    tarea_control = asyncio.create_task(control())

    await asyncio.gather(tarea_media, tarea_control)

if __name__ == "__main__":
    asyncio.run(main())

            