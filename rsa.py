import math
import random
import time

def extendedEuclidean(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = extendedEuclidean(b % a, a)
		return (gcd, y - b//a * x, x)

def fermatPrimalityTest(n):
    if n > 1:
        for t in range(20):
            rand = random.randint(2, n)-1
            if pow(rand,n-1,n) != 1:
                return False
        return True
    else:
        return False

def geraPrimo(bits):  
    n = random.randint(0, pow(2, bits))
    if n % 2 == 0:
        n = n+1

    while not fermatPrimalityTest(n):
        n += 2

    return n

def chavePublica(bits):
	p = geraPrimo(bits)
	q = geraPrimo(bits)
	while p == q:
		q = geraPrimo(bits)

	e = random.randint(0, pow(2,16))
	while math.gcd(e, (p-1)*(q-1)) != 1:
		e = random.randint(0, pow(2,16)) 

	return (e, p, q)

def chavePrivada(e, p, q):
    d = extendedEuclidean(e, (p-1)*(q-1))[1]
    if d < 1:
        d = d + ((p-1)*(q-1))

    return (int(d), p * q)

def criptografa(mensagem, e, n):
    cript = []
    for c in mensagem:
        cript.append(pow(ord(c), e, n))

    return cript

def descriptografa(mensagem, d, n):
    decript = []
    for i in mensagem:
        decript.append(chr(pow(int(i), d, n)))

    return decript

def quebra_forcabruta(n):
	p = int(math.sqrt(n)) + 1

	if p % 2 == 0:
		p += 1

	while n % p != 0:
		p -= 2

	q = n // p

	return (p, q)

def G(x,c):
	return pow(x,2) + c

def pollard_rho(n):
	x = random.randint(1, n)
	c = random.randint(1, n)
	y = x
	p = 1

	while p == 1:
		x = G(x, c) % n
		y = G(G(y, c), c) % n
		p = math.gcd(abs(x-y), n)

	return (p, n // p)


def tempos_geracao_chave(bits, sample):
	print("Bits Tempo")
	time.sleep(5)

	for b in bits:
		tempos = []
		print(b, end = " ")
		for i in range(sample):
			start = time.time()
			e, p, q = chavePublica(b)
			d, n = chavePrivada(e, p, q)
			end = time.time()
			tempos.append(end - start)

		print(sum(tempos) / len(tempos))
		time.sleep(0.5)

def tempos_forca_bruta(bits, sample):
	print("Bits Tempo")
	time.sleep(5)

	for b in bits:
		tempos = []
		print(b, end = " ")
		for i in range(sample):
			e, p, q = chavePublica(b)
			d, n = chavePrivada(e, p, q)
			start = time.time()
			quebra_forcabruta(n)
			end = time.time()
			tempos.append(end - start)

		print(sum(tempos) / len(tempos))
		time.sleep(0.5)

def tempos_pollards(bits, sample):
	print("Bits Tempo")
	time.sleep(5)

	for b in bits:
		tempos = []
		print(b, end = " ")
		for i in range(sample):
			e, p, q = chavePublica(b)
			d, n = chavePrivada(e, p, q)
			start = time.time()
			pollard_rho(n)
			end = time.time()
			tempos.append(end - start)

		print(sum(tempos) / len(tempos))
		time.sleep(0.5)

def alltests():
	print("# Geracao")
	tempos_geracao_chave(range(32, 2048, 32), 20)
	print("# Pollards")
	tempos_pollards(range(8, 129, 4), 5)
	print("# Forca bruta")
	tempos_forca_bruta(range(8, ))

def main():
	bits = 32
	msg = open("mensagem.txt", "r")
	encripted = open("mensagem.crypt", "w")
	uncripted = open("mensagem.decrypt", "w")
	e, p, q = chavePublica(bits)
	d, n = chavePrivada(e, p, q)

	print("(p,q) = " + str((p,q)))
	print("(e,n) = " + str((e,n)))
	print("(d,n) = " + str((d,n)))

	M = msg.read()
	C = criptografa(M, e, n)

	for i in C:
		encripted.write(str(i))
		encripted.write(' ')

	encripted.close()
	encripted = open("mensagem.crypt", "r")
	C = encripted.read().split()

	M = descriptografa(C, d, n)
	for j in M:
		uncripted.write(str(j))
	msg.close()
	encripted.close()
	uncripted.close()

	print(pollard_rho(n))
	#print(quebra_forcabruta(n))

if __name__ == '__main__':
    main()
	