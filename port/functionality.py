from kivy.uix.button import Button

class controls():	
	start = Button(size_hint = (.09,.1), pos_hint = {'center_x':.5,'y':0})
	start.background_normal = 'img/play.png'
	start.background_down = 'img/play_dn.png'
	start.border = (0,0,0,0)


	stop = Button(size_hint = (.09,.1), pos_hint = {'center_x':.7,'y':0})
	stop.background_normal = 'img/stop.png'
	stop.background_down = 'img/stop_dn.png'
	stop.border = (0,0,0,0)

	reset = Button(size_hint = (.09,.1), pos_hint = {'center_x':.3,'y':0})
	reset.background_normal = 'img/reset.png'
	reset.background_down = 'img/reset_dn.png'
	reset.border = (0,0,0,0)

	sett = Button(size_hint = (.09,.1), pos_hint = {'center_x':.1,'y':0})
	sett.background_normal = 'img/info.png'
	sett.background_down = 'img/info_dn.png'
	sett.border = (0,0,0,0)