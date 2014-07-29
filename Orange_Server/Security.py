import pyDes
import base64

class DES:
	def __init__(self, iv, key):
		self.iv = iv
		self.key = key

	def encrypt(self, data):
		k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
		d = k.encrypt(data)
		d = base64.encodestring(d)

	def decrypt(self, data):
		k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
		data = base64.decodestring(data)
		d = k.decrypt(data)
		return d