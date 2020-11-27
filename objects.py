"""
Object representations for startup ecosystem.
"""

class Company:
    def __init__(self, object_id, name, category, status, founding_date, funding_total_usd):
        self.object_id = object_id
        self.name = name
        self.category = category
        self.status = status
        self.founding_date = founding_date
        self.funding_total_usd = funding_total_usd

    def __str__(self):
        return self.name

    def get_object_id(self):
        return self.object_id

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_status(self):
        return self.status

    def get_founding_date(self):
        return self.founding_date

    def get_funding_total_usd(self):
        return self.funding_total_usd

class Fund:
    def __init__(self, object_id, name, funding_date, raised_amount, raised_currency_code):
        self.object_id = object_id
        self.name = name 
        self.funding_date = funding_date
        self.raised_amount = raised_amount
        self.raised_currency_code = raised_currency_code

    def __str__(self):
	    return self.object_id, self.name
	
    def get_object_id(self):
	    return self.object_id

    def get_name(self):
        return self.name

    def get_funding_date(self):
        return self.funding_date
        
    def get_raised_amount(self):
        return self.raised_amount

    def get_raised_currency_code(self):
        return self.raised_currency_code

class Investment:
	def __init__(self, funded_object_id, investor_object_id):
		self.funded_object_id = funded_object_id
		self.investor_object_id = investor_object_id		

	def __str__(self):
		return str(self.investor_object_id) + "funded" + str(self.funded_object_id)

	def get_funded_object_id(self):
		return self.funded_object_id

	def get_investor_object_id(self):
		return self.investor_object_id
