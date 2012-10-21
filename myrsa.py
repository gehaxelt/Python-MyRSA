#Encoding: UTF-8
import random
# globale variable mit primzahlen
previous_primes = [2]

def gcd(a, b):
    '''Return the greatest common divisor (gcd) of two numbers.

    Use the recursive variant of the extended Euclidean algorithm
    to compute the GCD of a and b. Also find two numbers x and y
    that satisfy ax + by = gcd(a,b).

    '''
    if b == 0:
        return (a, 1, 0)
    (d_, x_, y_) = gcd(b, a % b)
    (d, x, y) = (d_, y_, x_ - (a // b) * y_)
    return (d, x, y)

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

def gen_privkey(p, q, e):
    ''' Return the private key exponent d.

    Compute the private exponent d using the extended Euclidean algorithm.
    d is the multiplicative inverse of e % ((p - 1) * (q - 1)),
    so it satisfies d * e == 1 % ((p - 1) * (q - 1)).

    '''
    phi_n = (p - 1) * (q - 1)
    (x, d, y) = gcd(e, phi_n)
    if d < 0: d += phi_n
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

assert prime_p != prime_q

print "Calculating factor n"
factor_n = prime_p*prime_q
print ">>Factor n:" + str(factor_n)

print "Calculating Phi(N)"
phi_n = (prime_p-1)*(prime_q-1)
print ">>Phi(N):" + str(phi_n)

# e doesn't have to be choosen at random. any prime number < phi_n will work.
e = 17
print ">>Public exponent e:" + str(e)

assert e < phi_n

print "Generating pubkey d"
privkey_d = gen_privkey(prime_p, prime_q, e)
print ">>Privkey d:" + str(privkey_d)

print "Generating text"
text_clear = random.randint(0,100)
print ">>Text:" + str(text_clear)

print "Encrypting"
text_encrypted = pubkey_encrypt(text_clear, e, factor_n)
print ">>Text (encrypted):" + str(text_encrypted)

print "Decrypting"
text_decrypted = privkey_decrypt(text_encrypted, privkey_d, factor_n)
print ">>Text (decrypted):" + str(text_decrypted)
