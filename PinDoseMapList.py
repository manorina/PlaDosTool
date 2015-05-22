from pylinac.core import io as io
import PinDoseMap as pdm

class PinDoseMapList:

	"""A wrapper class to hold PinDoseMap objects as a list.
	Intended to use for planar dose maps from Pinnacle for IMRT QA
    
	TODO: more details?"""
	
	def __init__(self, my_dir=''):
		self.pin_dose_folder = None
    
		if my_dir != '':
			if os.path.exists(my_dir):
				print ("Entries:\n=======\n\n")
                
				for f in os.listdir(my_dir):
					print("entry: %s" % f)
			else:
				print ("check this path exists: %s" % my_dir)
		else:
			self.pin_dose_folder = io.get_folder_UI(None, 'Please select planned planar dose files ...')
			print("Pinnacle planar dose folder is %s" % self.pin_dose_folder)
            
