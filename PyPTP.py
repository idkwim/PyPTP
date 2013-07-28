#--
#
# Name: PyPTP
# Description: Python Pointer-to-Pointer fuzzing
#
# some dude named Level wrote this i guess...
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
#
#--
from sys import exit,modules
from inspect import getargspec,ismodule,isclass,isfunction,isbuiltin
from types import MethodType
from ctypes import *
from random import randrange,random
from optparse import OptionParser

class fuzzMap:
	def __init__(self,funcMap):
		filtered = {}
		for i in funcMap.iterkeys():
			# only care about functions with user input to manipulate
			if funcMap[i] is not None and funcMap[i] is not () and funcMap[i] is not [] and funcMap[i] is not {}:
				filtered[i] = funcMap[i]
		self.handler(filtered)
		return
	def handler(self,filtered):
		mutator,cases = self.mutator(),0
		print "[*] Total of %s calls which can be fuzzed" % (len(filtered))
		while True:
			try:
				print "[*] Sent %s fuzzed calls\r" % (cases),
				for i in set(filtered):
					fuzzArgs = ""
					for y in filtered[i]:
						foundType = str(y).split("'")[1]
						for matchType in mutator.cTypes.iterkeys():
							if foundType in mutator.cTypes[matchType]:
								if (matchType == 'str' or matchType == 'unicode'):
									mutatedData = mutator.string()
								if (matchType == 'int' or matchType == 'float' or matchType == 'boolean'):
									mutatedData = mutator.integer()
							else:
								if "ctypes" not in foundType:
									mutatedData = "%s()" % (foundType)
						fuzzArgs+="%s," % (mutatedData)
					try:
						#execute fuzzed code
						eval('%s("%s")' % (i,fuzzArgs[:-1]))
					except:
						pass
				cases+=1
			except KeyboardInterrupt:
				print "[*] Processed total of %s fuzzed calls\r" % (cases)
				print "[*] Caught CTRL^C -- exiting"
				break
			except TypeError:
				pass
		return
		
	class mutator:
		def __init__(self):
			self.cTypes = {'str':['ctypes.c_char','ctypes.c_wchar','ctypes.c_char_p','ctypes.c_void_p'],'int':['ctypes.c_byte','ctypes.c_ubyte','ctypes.c_short',
				'ctypes.c_ushort','ctypes.c_int','ctypes.c_uint','ctypes.c_long','ctypes.c_ulong','ctypes.c_longlong','ctypes.c_ulonglong','ctypes.c_void_p'],
				'float':['ctypes.c_float','ctypes.c_double','ctypes.c_longdouble'],'unicode':['ctypes.c_wchar','ctypes.c_wchar_p'],'boolean':['ctypes.c_bool']}
			return
		def string(self):
			letters = [['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
						['!','@','#','$','%','^','&','*','(',')','_','+','-','=','[',']','\\','{','}','|',';',':','.','/','<','>','?','`','~',"\"","\'"],
						['x','d','h','n']]
			num = randrange(0,3)
			if (num == 0):
				#normal
				return '%s' % letters[0][randrange(0,26)]*randrange(0,0xFF)
			elif (num == 1):
				#special
				return '%s' % letters[1][randrange(0,30)]*randrange(0,0xFF)
			elif (num == 2):
				#format
				return '%s%i%s' % ('%',randrange(0,0xFF),letters[2][randrange(0,3)])
			else:
				num = randrange(0,2)
				if (num == 0):
					#normal
					return '%s' % self.mutate_encoding(letters[0][randrange(0,26)]*randrange(0,0xFF))
				elif (num == 1):
					#special
					return '%s' % self.mutate_encoding(letters[1][randrange(0,30)]*randrange(0,0xFF))
				elif (num == 2):
					#format
					return '%s' % self.mutate_encoding("%s%i%s" % ('%',randrange(0,0xFF),letters[2][randrange(0,3)]))
		def integer(self):
			num = randrange(0,3)
			if (num == 0):
				#int
				return randrange(0,0xFF)-randrange(0,0xFF)+round(random())
			if (num == 1):
				#float
				return random()
			if (num == 2):
				#bool
				if (random() % 2):
					return True
				else:
					return False
			if (num == 3):
				#dword
				return dwords[randrange(0,4)]*randrange(0,0xFF)
		def mutate_enoding(self,case):
			codeList = ['ascii','big5','big5hkscs','cp037','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855','cp856','cp857','cp858','cp860','cp861','cp862',
						'cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949','cp950','cp1006','cp1026','cp1140','cp1250','cp1251','cp1252','cp1253','cp1254','cp1255',
						'cp1256','cp1257','cp1258','euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2','iso2022_jp_2004',
						'iso2022_jp_3','iso2022_jp_ext','iso2022_kr','latin_1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6','iso8859_7','iso8859_8','iso8859_9','iso8859_10',
						'iso8859_13','iso8859_14','iso8859_15','iso8859_16','johab','koi8_r','koi8_u','mac_cyrillic','mac_greek','mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154',
						'shift_jis','shift_jis_2004','shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf_8','utf_8_sig','base64_codec','bz2_codec',
						'hex_codec','idna','mbcs','palmos','punycode','quopri_codec','raw_unicode_escape','rot_13','string_escape','undefined','unicode_escape','unicode_internal','uu_codec',
						'zlib_codec']
			while True:			
				try:
					newcase = case.encode(codeList[randrange(0,len(codeList))])
					if (newcase): break
				except:
					continue
			return newcase

class funcMap:
	def __init__(self,mod):
		self.actr = 0
		self.mctr = 0
		self.mappedFunc = {}
		try:
			modules['__main__'].__setattr__('%s' % (mod.split(".")[0]),__import__('%s' % (mod)))
		except:
			print '[*] could not import %s\n' % (mod)
			exit(1)
		return
		
	def map_args(self,func):
		if "argtypes" in self.get_attrs(eval('%s' % (func))):
			self.mctr+=1
			return eval('%s.argtypes' % (func))

	def get_attrs(self,mod):
		list = []
		for i in dir(mod):
			if "_" not in i and "__" not in i:
				list.append(i)
			else:
				pass
		return list

	def crawl_imports(self,mod):
		try:
			if ("%s" % (mod) not in self.mappedFunc):
				list = []
				Rawexports = eval("self.get_attrs(%s)" % (mod[0]))
				for export in Rawexports:
					if ("%s.%s" % (mod[0],export) not in self.mappedFunc):
						try:
							self.mappedFunc["%s.%s" % (mod[0],export)] = self.map_args("%s.%s" % (mod[0],export))
						except:
							pass
						self.actr+=1
				if (self.mctr != 0):
					print "[*] mapped: %s/%s %s%s\r" % (self.mctr,self.actr,round(self.mctr / (self.actr * 1.0)*100,2),"%"),
				else:
					print "[*] mapped: 0/%s\r" % (self.actr),			
		except (KeyboardInterrupt, RuntimeError):
			print "[*] error crawling imports"
			exit(1)
		print "[*] functions mapped, fuzzing"
		fuzzMap(self.mappedFunc)	
		return
		
	
def main():
	print "python pointer-to-pointer function fuzzin' by Level\n"
	parser = OptionParser()
	parser.add_option("--module",dest="module",help="Python Module (ex: OpenGL.GL)")
	o,a = parser.parse_args()
	mapper = funcMap('%s' % (o.module))
	mapper.crawl_imports(['%s' % o.module])
	exit(0)
	
if __name__=="__main__":
	main()