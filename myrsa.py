#Encoding: UTF-8
import random
# globale variable mit primzahlen
previous_primes = [2]

#Funktion zur Berechnung des größten gemeinsamen Teilers
def ggT(x,y):
	temp = 1

	if(y > x):
		temp = x
		x = y
		y = temp

	while( 0 != temp):
		temp = x % y
		x = y
		y = temp
	return x

#Funktion zur Überprüfung ob number eine Primzahl ist
def isPrime(number):
	for prev_prime in previous_primes:
                if( 0 == (number % prev_prime)):
			return False
	return True

#Funktion zur Berechnung von Primzahlen
def gen_prime(max):
	previous_primes = [2]
	last_prime = 0
	for i in xrange(2,max):
		if(isPrime(i)):
			previous_primes.append(i)
			last_prime = i
	return last_prime

#Funktion zur Berechnung des öffentlichen Schlüssels aus den Primzahlen p & q
def gen_pubkey(p,q):
	for e in xrange(random.randint(0,200),(p-1)*(q-1)-1): 
		if( ggT(e, (p-1)*(q-1)) == 1):
			return e

#Funktion zur Berechnung des privaten Schlüssels aus den Primzahlen p & q, sowie dem öffentlichen Schlüssel e
def gen_privkey(p,q,e):
	d_array = [] # Array mit allen möglichen privaten Schlüsseln
	
	#Brute Force-artige Berechnung von möglichen privaten Schlüsseln
	for k in xrange(-(p-1)*(q-1),(p-1)*(q-1)): #Bereich: -Phi(N)^2 bis Phi(N)^2
		for d in xrange (-e*e, e*e): #Bereich: -e^2 bis e^2
			if(1 == (e*d + k*(p-1)*(q-1)) ): # Brute-Force des erweiterten euklidschen Algorithmus
				d_array.append(d)
	
	#Array der größe sortieren und erste positive Ergebnis nehmen.
	d_array.sort()
	for d in d_array:
		if d > 0:
			return d

#Funktion zur Verschlüsselung einer Zahl mit dem öffentlichen Schlüssel
def pubkey_encrypt(text, pubkey, factor):
	return text ** pubkey % factor

#Funktion zur Entschlüsselung eines Chiffrats mit dem privaten Schlüssel
def privkey_decrypt(chiffre, privkey, factor):
	return chiffre **  privkey % factor

print "Generating prime p"
prime_p = gen_prime(random.randint(10,50))
print ">>Prime p:" + str(prime_p)

print "Generating prime q"
prime_q = gen_prime(random.randint(10,50))
print ">>Prime q:" + str(prime_q)

print "Calculating factor n"
factor_n = prime_p*prime_q
print ">>Factor n:" + str(factor_n)

print "Calculating Phi(N)"
phi_n = (prime_p-1)*(prime_q-1)
print ">>Phi(N):" + str(phi_n)

print "Generating pubkey e"
pubkey_e = gen_pubkey(prime_p, prime_q)
print ">>Pubkey e:" + str(pubkey_e)

print "Generating pubkey d"
privkey_d = gen_privkey(prime_p, prime_q, pubkey_e)
print ">>Privkey d:" + str(privkey_d)

print "Generating text"
text_clear = random.randint(0,100)
print ">>Text:" + str(text_clear)

print "Encrypting"
text_encrypted = pubkey_encrypt(text_clear, pubkey_e, factor_n)
print ">>Text (encrypted):" + str(text_encrypted)

print "Decrypting"
text_decrypted = privkey_decrypt(text_encrypted, privkey_d, factor_n)
print ">>Text (decrypted):" + str(text_decrypted)
