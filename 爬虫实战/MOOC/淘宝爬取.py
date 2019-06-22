import requests
import re

headers = {
    'Cookies':"t=391a8b1ae4fcd9e62666cdbae1cbbdd7; cna=Uj56Fczal3ICASQXe5nXiHBR; cookie2=10dec6a51efb5f16458b5ff92d61894d; v=0; _tb_token_=5567eb8bdfe53; unb=3981314818; sg=685; _l_g_=Ug%3D%3D; skt=66a8c2b09f1d06a5; cookie1=Vqgq8AV7pu7zVxxxFD5YgNA%2BAWesmL81vsL%2ByY7aQU8%3D; csg=05b76b98; uc3=vt3=F8dBy3kZwTmBDaFVP1k%3D&id2=UNk%2FSaFuapoOtA%3D%3D&nk2=F5RHo3ge8Gx59a8%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; existShop=MTU2MTE5NzA5OQ%3D%3D; tracknick=tb223961776; lgc=tb223961776; _cc_=UtASsssmfA%3D%3D; dnk=tb223961776; _nk_=tb223961776; cookie17=UNk%2FSaFuapoOtA%3D%3D; tg=0; enc=EjDILAe17QdU%2Fz8XbYqlZdVf%2FNVFrbJ4VlqumO%2FdmP8AqU%2FgPWwBijhMJCOFE905PO631G9ak3rj%2B8k%2For1j4w%3D%3D; JSESSIONID=01D3C6AF8ECA686630C16B605FB1DF59; mt=ci=3_1; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=68805; uc1=cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&cookie14=UoTaGdxKmK2Ufw%3D%3D; l=bBEvM15PvdClqewyBOfZiZObAx7TNIdb4iVPhPx55ICPO_C9R69cWZhBoDYpC3GVw1DMR3SgKvQeBeYBq1f..; isg=BCUlFS1rlCltZPGLFuLd9f9LNOFVbnqO9eJG1ScLS9xrPkWw77P4xLOUzOLtEvGs"
    ,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

}

r = requests.get(url='https://s.taobao.com/search?q=书包',headers=headers,timeout=10)
html = r.text
print(html)
print(r.status_code)
regx = re.compile('.*?"raw_title":"(.*?)"')

result =re.findall(regx,html)
print(result)

### 由于信息都封装在script中，现在还没能解析


