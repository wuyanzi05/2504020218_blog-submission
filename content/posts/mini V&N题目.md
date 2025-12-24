## crypto

**题目信息 - pOgOcOd**

> - 难度：简单
> - 出题人：A1ic3

考点：解析 gifts、求 gcd、CRT、求根、RSA 解密


```python
import base64, sympy
from Crypto.Util.number import *

lines=open("gifts.txt").read().splitlines()
c=int(lines[0])
a=[int.from_bytes(base64.b64decode(x),"big") for x in lines[1:]]

def crt_merge(data):
    M=1;m1=0;m2=0
    for r,(s1,s2) in data:
        M2=M*r
        k1=((s1-m1)%r)*pow(M,-1,r)%r
        k2=((s2-m2)%r)*pow(M,-1,r)%r
        m1+=k1*M;m2+=k2*M
        M=M2
    return m1,m2,M

data=[]
primes=list(sympy.primerange(10**7,10**7+20000))[:80]
for r in primes:
    ar=[x%r for x in a]
    d=[(i+1)*ar[i+1]%r for i in range(len(ar)-1)]
    P=sympy.Poly(ar, sympy.symbols('x'), modulus=r)
    D=sympy.Poly(d, sympy.symbols('x'), modulus=r)
    G=sympy.gcd(P,D)
    if G.degree()==2:
        g=G.all_coeffs()
        c2,c1,c0=g
        inv=pow(c0,r-2,r)
        s1=c1*inv%r
        s2=c2*inv%r
        data.append((r,(s1,s2)))
    if len(data)>=40:break

S1,S2,M=crt_merge(data)
Δ=S1*S1-4*S2
√Δ=isqrt(Δ)
p=(S1+√Δ)//2
q=(S1-√Δ)//2
phi=(p-1)*(q-1)
e=0x10001
d=pow(e,-1,phi)
m=pow(c,d,p*q)
flag=m.to_bytes((m.bit_length()+7)//8,"big")
print(flag)

```



## misc

**题目信息 - D u know Pyc？**

> 你也听说过pyc？
>
> hint：好好想想明文攻击的条件 怎么构造呢
>
> - 难度：中等
> - 出题人：Hurkin

1、解压缩包，得Sect3t.jpg、flag.zip、flag.txt

2、处理Sect3t.jpg，得Sect3t文件，内含字符串表示作为密钥

```bash
unzip -v flag.zip
zipinfo -v flag.zip
zipdetails flag.zip
7z l -slt flag.zip
```

得到核心信息：包内有两个文件，均为 ZipCrypto 加密、未压缩（Stored）：`attack_it.pyc`（3302 bytes）`flag.py`（1411 bytes）

```
python 3.12.12
Bit Field 为 00 00 00 00
hash 字段非置空
```

3、利用pyc文件头：魔数（magic）、时间戳 / hash、源文件大小、bitfield（已知为0），构建bin文件作bkcrack明文攻击，最终爆出3个内部key；
4、有了 key，可以直接用 bkcrack 解密加密条目，而flag.py.decrypted可打开，根据该脚本文件以及前文得出的S3ct3t文件解得与另一个flag.txt内容相似的base64字符串，利用 RC4 线性&XOR 关系解题（base64 异或）。由于不懂密码就拿去喂AI了。

**题目信息 - wav也能像png那样美丽吗**

> 一步登天是极好的，但如果看不见那条通往终点的路，稍微绕一下也没关系的喵。
>
> - 难度：简单
> - 出题人：温婳霂
>

第一层：耳听wav音频，可明显意识到右声道10–31 s 的电码段，破译得`fakeflag1 LOOK-AT-THE-FILE-END`
第二层：使用010 Editor打开wav文件，在文件尾发现`fakeflag2 See_the_audio_spectrogram.`
第三层：仔细听，64s~76s可感受到有怪异波形干扰，查看频谱图发现嵌入文字`fakeflag3{Be aware of the sentences initials}`
根据fakeflag3，综合题目信息，得知提取三条fakeflag的首字母，即LSB（隐写技术）。
根据出题提醒“一步登天”，考虑到有现成脚本，故依次使用音频工具进行分析，最终以SilentEye WAV插件实现读取flag。

~~**题目信息 - welcome.pdf**~~

> ~~很简单吧o.O~~
>
> ~~难度：简单~~
> ~~出题人：Himekawa~~

~~1、用`AZR`修复一下题目压缩包，第一层`welcome.pdf.zip`就破解了，得到welcome.7z与welcome.pdf~~
~~2、对于welcome.pdf，搜寻了半天没有发现可疑隐写内容。~~
~~3、对于welcome.7z，不支持已知明文攻击，不清楚内在结构，目前已知信息只支持进行构造字典爆破~~

~~**题目信息** **-** **MCServer**~~

~~没来得及下工具，不会解，只能硬strings grep，无果。~~

**题目信息 - chatrobot**

> 新写的chatrobot好像日志设置有点问题？
> （机器人反射弧有点长捏，请耐心一点喵QAQ）
>
> - 难度：简单
> - 出题人：夏饭orz

题目核心结构：

```
前端网页 —→ Flask 后端（Python）—→ Java 程序（log4j 记录日志）
```

Flag 存放于 **Java 进程环境变量 FLAG** 中，由 Python 在运行Java之前写入。最终flag会通过一种显式日志泄露方式被打印到 stderr，而 Flask 会把 stderr 返回给用户。

`/chat`不返回stderr，而`/`（根路由） 原样返回→日志内容可见→flag泄露。

根据Java 端 log4j 配置

```perl
<PatternLayout pattern="%d ... executing ${sys:cmd} - %msg %n"/>
```

因此当 `cmd="${env:FLAG}"` 时，log4j 执行解析：`${sys:cmd}` → 得到字符串 `"${env:FLAG}"`，再对 `"${env:FLAG}"` 做变量展开 → 获取真实 FLAG（因为存在环境变量 FLAG）

使用POST / 执行：stdout + stderr → 返回给用户

最终payload如下

```css
POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded

text=${env:FLAG} x
```


