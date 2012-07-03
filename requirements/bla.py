class Adapter:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Adapter2(Adapter):
	def cool(self):
		return 'at last'

ad = Adapter2('aw', 'awfff')

print(ad.x)
print ad.cool()
