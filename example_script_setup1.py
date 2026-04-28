from OpticsLabLib.Hardware_Interfaces import Camera, DM
import matplotlib.pyplot as plt
import numpy as np
import time

psf_cam_address = 1
sh_cam_address = 3
dm_address = 0

psf_cam_brand = "ueye"
sh_cam_brand = "ueye"
dm_brand = "ThorlabsDM"

acquire_pictures = False

with (Camera(psf_cam_address, psf_cam_brand if acquire_pictures else "dummycamera") as psfcam,
      Camera(sh_cam_address, sh_cam_brand if acquire_pictures else "dummycamera") as shcam,
      DM(dm_address, dm_brand) as dm):


    if acquire_pictures:
        psfcam.exposure = 10
        shcam.exposure = 10
        psfcam.start_acquisition()
        shcam.start_acquisition()
        
        
        fig, (ax1, ax2) = plt.subplots(1, 2)
        cam_width, cam_height = psfcam.sensor_size()
        ax1.set_title("PSF camera")
        ax2.set_title("Sh camera")

        psfax = ax1.imshow(np.zeros((cam_height, cam_width)), cmap='gray', origin="lower")
        shax = ax2.imshow(np.zeros((cam_height, cam_width)), cmap='gray', origin="lower")

        plt.ion()

    volt_range = np.linspace(-0.9, 0.9, 50, endpoint=True)
    dm_voltages = np.hstack((volt_range, volt_range[::-1]))

    while True:
        for dmvolt in dm_voltages:
            print(dmvolt)
            # Define the input voltages
            u = np.ones(dm.num_actuators) * dmvolt

            # Last two are tip/tilt, let's disable those for now
            u[-2:] = 0

            # Send to the DM
            dm.write(u, modal=False)

            if acquire_pictures:
                psfpic = psfcam.grab_frame()
                shpic = shcam.grab_frame()

                psfax.set_data(psfpic)
                shax.set_data(shpic)
                psfax.autoscale()
                shax.autoscale()
                plt.pause(0.001)
                
            time.sleep(0.01)
