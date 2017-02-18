class StringTitle:
	name = 'string'
	def __init__(self,handler,string):
		self.title = string
	def get(self):
		return self.title
		
exports = [StringTitle]