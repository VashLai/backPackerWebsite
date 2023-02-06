class Pages:
	def __init__(self,data,cur_page,page_num):
		self.data = data
		self.cur_page = cur_page
		self.page_num = page_num

	@property
	def page(self):
		return self.data

	@property
	def has_previous(self):
		return self.cur_page - 1 > 0

	@property
	def has_next(self):
		return self.page_num - self.cur_page > 0
	@property
	def previous_page_number(self):
		return self.cur_page - 1

	@property
	def next_page_number(self):
		return self.cur_page + 1
	