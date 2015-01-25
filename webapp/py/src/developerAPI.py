userid = ''

data_loading = False
data = ''

f3_mean = 0
fc5_mean = 0
af3_mean = 0
f7_mean = 0
t7_mean = 0
p7_mean = 0
o1_mean = 0
o2_mean = 0
p8_mean = 0
t8_mean = 0
f8_mean = 0
af4_mean = 0
fc6_mean = 0
f4_mean = 0

delta_sum_mag = {}
theta_sum_mag = {}
alpha_sum_mag = {}
beta_sum_mag = {}
gamma_sum_mag = {}

def write_userid(user) :
	global userid
	userid = user

def write_delta_sum_mag(channel,power) :
	global delta_sum_mag
	delta_sum_mag[channel] = power

def write_theta_sum_mag(channel,power) :
	global theta_sum_mag
	theta_sum_mag[channel] = power

def write_alpha_sum_mag(channel,power) :
	global alpha_sum_mag
	alpha_sum_mag[channel] = power

def write_beta_sum_mag(channel,power) :
	global beta_sum_mag
	beta_sum_mag[channel] = power

def write_gamma_sum_mag(channel,power) :
	global gamma_sum_mag
	gamma_sum_mag[channel] = power

def get_userid():
	return [userid]

def get_delta_sum_mag(channel) :
	return delta_sum_mag[channel]

def get_theta_sum_mag(channel) :
	return theta_sum_mag[channel]

def get_alpha_sum_mag(channel) :
	return alpha_sum_mag[channel]

def get_beta_sum_mag(channel) :
	return beta_sum_mag[channel]

def get_gamma_sum_mag(channel) :
	return gamma_sum_mag[channel]

def format_data_to_emit() :
	global data_loading
	global data
	data_loading = True
	data = ''
	data += "F3:" + str(delta_sum_mag['F3']) + ',' + str(theta_sum_mag['F3']) + ',' + str(alpha_sum_mag['F3']) + ',' + str(beta_sum_mag['F3']) + ',' + str(gamma_sum_mag['F3']) + '\n'
	data += "FC5:" + str(delta_sum_mag['FC5']) + ',' + str(theta_sum_mag['FC5']) + ',' + str(alpha_sum_mag['FC5']) + ',' + str(beta_sum_mag['FC5']) + ',' + str(gamma_sum_mag['FC5']) + '\n'
	data += "AF3:" + str(delta_sum_mag['AF3']) + ',' + str(theta_sum_mag['AF3']) + ',' + str(alpha_sum_mag['AF3']) + ',' + str(beta_sum_mag['AF3']) + ',' + str(gamma_sum_mag['AF3']) + '\n'
	data += "F7:" + str(delta_sum_mag['F7']) + ',' + str(theta_sum_mag['F7']) + ',' + str(alpha_sum_mag['F7']) + ',' + str(beta_sum_mag['F7']) + ',' + str(gamma_sum_mag['F7']) + '\n'
	data += "T7:" + str(delta_sum_mag['T7']) + ',' + str(theta_sum_mag['T7']) + ',' + str(alpha_sum_mag['T7']) + ',' + str(beta_sum_mag['T7']) + ',' + str(gamma_sum_mag['T7']) + '\n'
	data += "P7:" + str(delta_sum_mag['P7']) + ',' + str(theta_sum_mag['P7']) + ',' + str(alpha_sum_mag['P7']) + ',' + str(beta_sum_mag['P7']) + ',' + str(gamma_sum_mag['P7']) + '\n'
	data += "O1:" + str(delta_sum_mag['O1']) + ',' + str(theta_sum_mag['O1']) + ',' + str(alpha_sum_mag['O1']) + ',' + str(beta_sum_mag['O1']) + ',' + str(gamma_sum_mag['O1']) + '\n'
	data += "O2:" + str(delta_sum_mag['O2']) + ',' + str(theta_sum_mag['O2']) + ',' + str(alpha_sum_mag['O2']) + ',' + str(beta_sum_mag['O2']) + ',' + str(gamma_sum_mag['O2']) + '\n'
	data += "P8:" + str(delta_sum_mag['P8']) + ',' + str(theta_sum_mag['P8']) + ',' + str(alpha_sum_mag['P8']) + ',' + str(beta_sum_mag['P8']) + ',' + str(gamma_sum_mag['P8']) + '\n'
	data += "T8:" + str(delta_sum_mag['T8']) + ',' + str(theta_sum_mag['T8']) + ',' + str(alpha_sum_mag['T8']) + ',' + str(beta_sum_mag['T8']) + ',' + str(gamma_sum_mag['T8']) + '\n'
	data += "F8:" + str(delta_sum_mag['F8']) + ',' + str(theta_sum_mag['F8']) + ',' + str(alpha_sum_mag['F8']) + ',' + str(beta_sum_mag['F8']) + ',' + str(gamma_sum_mag['F8']) + '\n'
	data += "AF4:" + str(delta_sum_mag['AF4']) + ',' + str(theta_sum_mag['AF4']) + ',' + str(alpha_sum_mag['AF4']) + ',' + str(beta_sum_mag['AF4']) + ',' + str(gamma_sum_mag['AF4']) + '\n'
	data += "FC6:" + str(delta_sum_mag['FC6']) + ',' + str(theta_sum_mag['FC6']) + ',' + str(alpha_sum_mag['FC6']) + ',' + str(beta_sum_mag['FC6']) + ',' + str(gamma_sum_mag['FC6']) + '\n'
	data += "F4:" + str(delta_sum_mag['F4']) + ',' + str(theta_sum_mag['F4']) + ',' + str(alpha_sum_mag['F4']) + ',' + str(beta_sum_mag['F4']) + ',' + str(gamma_sum_mag['F4'])
	data_loading = False
	#print 'data formatted = ' + data

def get_all_power() :
	#print 'userid = ' + userid
	#print 'data requested = ' + data
	while data_loading:
		pass
	return data