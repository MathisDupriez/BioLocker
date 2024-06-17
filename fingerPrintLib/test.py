import time
from fplib import fplib

# Setup the fingerprint module variables
# Replace 'port=0' with your actual port, e.g., '/dev/ttyS0'
fp = fplib(port='/dev/ttyAMA10', baud=115200, timeout=3)

# Module initializing
try:
    init = fp.init()
    print("is initialized :", init)

    # Run only task that is specified
    task = 1  # You can change this number to test different functionalities

    #=#=# ---------------------------- T.A.S.K.S ---------------------------------- #=#=#
    # 1. turning ON & OFF LED
    if task == 1:
        # ON
        led = fp.set_led(True)
        print("\n |__ LED status :", led) 

        time.sleep(2)

        # OFF
        led = fp.set_led(False)
        print("\n |__ LED status :", led)

    # 2. check if finger is pressed or not
    elif task == 2:
        pressed = fp.is_finger_pressed()
        print("\n |__ is finger pressed ?", pressed)

    # 3. make fingerprint template
    elif task == 3:
        data, downloadstat = fp.MakeTemplate()
        print(f"\n |__ Is template fetched ?", downloadstat)

        img_arr = []
        if downloadstat:
            data = bytearray(data)
            for ch in data:
                img_arr.append(ch)
        print("fetched template data: ", img_arr)

    # 4. enroll fingerprint to device memory
    elif task == 4:
        if fp.is_finger_pressed():
            print("\n |__Finger is pressed")
            id, data, downloadstat = fp.enroll()
            print(f"\n |__ID: {id} & is captured ?", data != None)
            print(f"\n |__ enrolled counts :", fp.get_enrolled_cnt())

    # 5. delete saved template from device (delete all/ delete by id)
    elif task == 5:
        status = fp.delete()  # delete all
        print("\n |__ Delete status: ", status)
        print(f"\n |__ enrolled counts :", fp.get_enrolled_cnt())

    # 6. identify / recognize fingerprint
    elif task == 6:
        id = fp.identify()
        print("\n |__ identified id:", id)

    # 7. settemplate - set a template data to device
    elif task == 7:
        DATA = []  # a 502 length python list, that we get after running "task 3"
        fp.delete(idx=0)
        status = fp.setTemplate(idx=0, data=DATA)
        print("\n |__ set template status :", status)
    
    elif task == 8:
        try:
            id_to_retrieve = int(input("Entrez l'ID du modèle à récupérer: "))
            template, status = fp.get_template(id_to_retrieve)
            if status:
                print(f"\n |__ Modèle d'empreinte pour l'ID {id_to_retrieve}:")
                print(template)
            else:
                print(f"\n |__ Échec de la récupération du modèle pour l'ID {id_to_retrieve}")
        except ValueError:
            print("ID invalide. Veuillez entrer un nombre entier.")


except Exception as e:
    print("Error:", str(e))
