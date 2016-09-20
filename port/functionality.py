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

	info = Button(size_hint = (.09,.1), pos_hint = {'center_x':.1,'y':0})
	info.background_normal = 'img/info.png'
	info.background_down = 'img/info_dn.png'
	info.border = (0,0,0,0)

	prsts = Button(size_hint = (.09,.1), pos_hint = {'center_x':.9,'y':0})
	prsts.background_normal = 'img/click.png'
	prsts.background_down = 'img/click_dn.png'
	prsts.border = (0,0,0,0)

	sett = Button(size_hint = (.09,.1), pos_hint = {'center_x':.5,'top':1})
	sett.background_normal = 'img/sett.png'
	sett.background_down = 'img/sett_dn.png'
	sett.border = (0,0,0,0)
