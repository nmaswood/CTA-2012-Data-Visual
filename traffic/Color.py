class Colors(object):

	def gen_colors(self,num, type):

		base_num = {1:1.99, 2:35, 3:35}[type]

		if   num <= base_num:       return 0
		elif num <= base_num * 2:   return 1
		elif num <= base_num * 3:   return 2
		elif num <= base_num * 4:   return 3
		elif num <= base_num * 5:   return 4
		elif num <= base_num * 6:   return 5
		elif num <= base_num * 7:   return 6
		elif num <= base_num * 8:   return 7
		elif num <= base_num * 9:   return 8
		elif num <= base_num * 10:  return 9
		elif num <= base_num * 11:  return 10
		elif num <= base_num * 12:  return 11
		elif num <= base_num * 13:  return 12
		elif num <= base_num * 14:  return 13
		elif num <= base_num * 15:  return 14
		elif num <= base_num * 16:  return 15
		elif num <= base_num * 17:  return 16
		elif num <= base_num * 18:  return 17
		elif num <= base_num * 19:  return 18
		elif num <= base_num * 20:  return 19
		elif num <= base_num * 21:  return 20
		elif num <= base_num * 22:  return 21
		elif num <= base_num * 23:  return 22
		elif num <= base_num * 24:  return 23
		elif num <= base_num * 25:  return 24
		elif num <= base_num * 26:  return 25
		elif num <= base_num * 27:  return 26
		elif num <= base_num * 28:  return 27
		elif num <= base_num * 29:  return 28
		elif num <= base_num * 30:  return 29
		elif num <= base_num * 31:  return 30
		elif num <= base_num * 32:  return 31
		elif num <= base_num * 33:  return 32
		elif num <= base_num * 34:  return 33
		elif num <= base_num * 35:  return 34
		elif num <= base_num * 36:  return 35
		elif num <= base_num * 37:  return 36
		elif num <= base_num * 38:  return 37
		elif num <= base_num * 39:  return 38
		elif num <= base_num * 40:  return 39
		elif num <= base_num * 41:  return 41
		elif num <= base_num * 42:  return 42
		elif num <= base_num * 43:  return 43
		elif num <= base_num * 44:  return 44
		elif num <= base_num * 45:  return 45
		elif num <= base_num * 46:  return 46
		elif num <= base_num * 47:  return 47
		elif num <= base_num * 48:  return 48
		elif num <= base_num * 49:  return 49
		elif num <= base_num * 50:  return 51
		elif num <= base_num * 51:  return 52
		elif num <= base_num * 52:  return 53
		elif num <= base_num * 53:  return 54
		elif num <= base_num * 54:  return 55
		elif num <= base_num * 55:  return 56
		elif num <= base_num * 56:  return 57
		elif num <= base_num * 57:  return 58
		elif num <= base_num * 58:  return 59
		elif num <= base_num * 59:  return 60
		elif num <= base_num * 60:  return 61
		elif num <= base_num * 61:  return 62
		return 63

	def gradient(self):
		return [
		'FFFFFF',
        'FEFBFB',
        'FEF7F8',
        'FEF3F4',
        'FEEFF1',
        'FEECED',
        'FDE8EA',
        'FDE4E6',
        'FDE0E3',
        'FDDDE0',
        'FDD9DC',
        'FCD5D9',
        'FCD1D5',
        'FCCED2',
        'FCCACE',
        'FCC6CB',
        'FBC2C7',
        'FBBFC4',
        'FBBBC1',
        'FBB7BD',
        'FBB3BA',
        'FBB0B6',
        'FAACB3',
        'FAA8AF',
        'FAA4AC',
        'FAA0A8',
        'FA9DA5',
        'F999A2',
        'F9959E',
        'F9919B',
        'F98E97',
        'F98A94',
        'F88690',
        'F8828D',
        'F87F89',
        'F87B86',
        'F87783',
        'F7737F',
        'F7707C',
        'F76C78',
        'F76875',
        'F76471',
        'F7616E',
        'F65D6A',
        'F65967',
        'F65564',
        'F65160',
        'F64E5D',
        'F54A59',
        'F54656',
        'F54252',
        'F53F4F',
        'F53B4B',
        'F43748',
        'F43345',
        'F43041',
        'F42C3E',
        'F4283A',
        'F32437',
        'F32133',
        'F31D30',
        'F3192C',
        'F31529',
        'F31226']