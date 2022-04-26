from pyzbar import pyzbar
import requests, cv2
from private import TOKEN


class FnsNalogAPI:
	API_URL = 'https://proverkacheka.com/api/v1/check/get'
	HEADERS = { 
		'accept': '*/*',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
		}
		
	def __init__(self,  token):
		self.__token = token


	def get_info(self, qr_info):
		request_data = {
			'fn': qr_info['fn'],
			'fd': qr_info['i'],
			'fp': qr_info['fp'],
			't':  qr_info['t'],
			'n':  qr_info['n'],
			's':  qr_info['s'],
			'qr': 1,
			'token': self.__token,
			}
		response = requests.post(FnsNalogAPI.API_URL, data=request_data, headers=FnsNalogAPI.HEADERS).json()
		api_response_code = response['code']
		return api_response_code, response['data']['json']


class Сheque:
	def __init__(self, image):
		self.qr_image = image
		self.qr_string = ''
		self.data = {}
		self.parsed = False


	def parse_qr(self):
		try:
			self.qr_string = pyzbar.decode(self.qr_image)
			raw_data = self.qr_string[0].data.decode().split('&')
			self.data = {value.split('=')[0]: value.split('=')[1] for value in raw_data}
			self.parsed = True
		except:
			self.parsed = False


def get_image_with_qr(path):
	try:
		print('Image uploaded successfully!')
		return  cv2.imread(path) 
	except:
		print('Image load error...')
		return None


def get_info_from_api(cheque):
	qr_string = cheque.qr_string
	qr_data = cheque.data
	fns_api = FnsNalogAPI(TOKEN)
	code, data = fns_api.get_info(qr_data)
	print('QR string: ', qr_string)
	print('API response code: ', code)
	print('API response data: ', data)


def cheque_info(path):
	image = get_image_with_qr(path)
	cheque = Сheque(image)
	cheque.parse_qr()
	if cheque.parsed:
		print('QR-code parsed successfully!')
		get_info_from_api(cheque)
	else:
		print('QR-code cannot be parsed...')


cheque_info('img/good_qr.jpg')
#cheque_info('img/bad_qr.jpg')