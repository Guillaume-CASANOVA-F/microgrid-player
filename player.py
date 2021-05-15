# python 3
# this class combines all basic features of a generic player
import numpy as np
import pulp

Capa = 60
Pmax = 10
rho_c = 0.95
rho_d = 0.95
delta_t = 0.5

class Player:

	def __init__(self):
		# some player might not have parameters
		self.parameters = 0
		self.horizon = 48

	def set_scenario(self, scenario_data):
		self.data = scenario_data

	def set_prices(self, prices):
		self.prices = prices

	def compute_all_load(self):
		load = np.zeros(self.horizon)
		for time in range(self.horizon):
			load[time] = self.compute_load(time)
		return load

	def compute_battery_load(self):
		
		my_lp_problem = pulp.LpProblem("My_LP_Problem", pulp.LpMinimize)
		variables = {}
		for t in range(self.horizon):
			
			variables[t] = {}

			var_name = "battery_load_+" + str(t)
			variables[t]["battery_load_+"] = pulp.LpVariable(var_name, 0, Pmax)

			var_name = "battery_load_-" + str(t)
			variables[t]["battery_load_-"] = pulp.LpVariable(var_name, 0, Pmax)

			stock = sum ( [delta_t * ( rho_c*variables[t]["battery_load_+"] - (variables[t]["battery_load_-"]/rho_d) ) ] for s in range(1, t+1) )

			constraint_name = "stock_positif" + str(t)
			my_lp_problem += stock >= 0

			constraint_name = "stock_ne_depasse_pas_la_capacite" + str(t)
			my_lp_problem += stock <= Capa

		my_lp_problem.setObjective(
		    pulp.lpSum([self.prices[t] * variables[t]["total_load"] * Delta_t for t in range(48)]))
		my_lp_problem.solve()
	
		battery_load = []
        	for t in range(self.horizon):
			for variable in my_lp_problem.variables():
                		if variable.name == "battery_load" + str(t):
                			battery_load.append(variable.varValue)
      	  				self.res = np.array(battery_load)
		return battery_load
	
	def take_decision(self, time):
		# TO BE COMPLETED
		return self.battery_load[time]

	def compute_load(self, time):
		load = self.take_decision(time)
		# do stuff ?
		load += self.data[time]
		return load

	def reset(self):
		# reset all observed data
		pass


numero_scenario = 0

T = pd.read_csv('indus_cons_scenarios.csv')
T_indus = T[T["site_id"]==1] # Industrial_consumer ID
scenario_data_complet = T_indus[]
scenario_data = T_indus[T_indus["scenario"]==numero_scenario]
	
Industrial_consumer = Player()
Industrial_consumer.set_prices(prices)
Industrial_consumer.set_scenario(scenario_data)

