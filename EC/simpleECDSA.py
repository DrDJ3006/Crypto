import random
from hashlib import sha256
class ECDSA(object):
    def __init__(self, coeff_a:int, coeff_b : int, coeff_c : int, mod : int, order : int, generator : (int, int) ):
        self.coeff_a= coeff_a
        self.coeff_b = coeff_b
        self.coeff_c = coeff_c
        self.order=order
        self.mod = mod
        self.generator = generator
        if 4 * (self.coeff_b **3) + 27 * self.coeff_c **2 == 0:
            print("invalid curve")
            exit()
        self.equation = f'y^2 = x^3 + {self.coeff_a}*x^2 + {self.coeff_b}*x + {self.coeff_c} : GF({self.mod})'
        
    def is_on_curve(self,P : (int,int)):
        x,y = P
        if (y**2%self.mod) == ((x**3 + self.coeff_a * (x**2) + self.coeff_b * x + self.coeff_c) % self.mod):
            return True
        else:
            return False
        
    def get_y(self,x:int):
        y_pow=(x**3 + self.coeff_a * (x**2) + self.coeff_b * x + self.coeff_c) % self.mod
        return self.tonelli_shanks(y_pow)

    def point_addition(self, P: (int, int), Q: (int, int)):
        if P == (0, 0):
            return Q
        if Q == (0, 0):
            return P
        x1, y1 = P
        x2, y2 = Q
        if P!=Q:
            if x1 == x2:
                λ = (3 * x1 ** 2 + self.coeff_b) * pow(2 * y1, -1, self.mod) % self.mod
            else :
                λ = ((y2 - y1) * pow(x2 - x1, -1, self.mod)) % self.mod
        elif P==Q:
            λ = (3 * x1 ** 2 + self.coeff_b) * pow(2 * y1, -1, self.mod) % self.mod
        x3 = (λ  ** 2 - x1 - x2) % self.mod
        y3 = (λ  * (x1 - x3) - y1) % self.mod
        return x3,y3
    
    def scalar_multiplication(self, scalar : int,P :[int,int]):
        R=(0,0)
        while True:
            n=1
            Q=P
            while True:
                if n*2 > scalar:
                    break
                Q = self.point_addition(Q,Q)
                n=n*2
                       
            R=self.point_addition(R,Q)
            scalar = scalar - n
            if scalar == 1:
                R=self.point_addition(R,P)
                break
            if scalar == 0:
                break    
        return R
    
    def legendre_symbol(self, a, p):
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    def tonelli_shanks(self, n):
        p=self.mod
        if self.legendre_symbol(n, p) != 1:
            return None

        Q, S = p - 1, 0
        while Q % 2 == 0:
            Q //= 2
            S += 1

        z = 1
        while self.legendre_symbol(z, p) != -1:
            z += 1

        M = S
        c = pow(z, Q, p)
        t = pow(n, Q, p)
        R = pow(n, (Q + 1) // 2, p)

        while True:
            if t == 0:
                return 0
            if t == 1:
                return R

            i, temp = 0, t
            for i in range(1, M):
                temp = pow(temp, 2, p)
                if temp == 1:
                    break

            b = pow(c, 1 << (M - i - 1), p)
            M = i
            c = pow(b, 2, p)
            t = (t * c) % p
            R = (R * b) % p

    def generate_keys(self,private_key=None):
        if not private_key:
            private_key = random.randrange(1, self.mod)
        public_key = self.scalar_multiplication(private_key,self.generator)
        return private_key, public_key

    def hash_msg(self,message):
        return int(sha256(message.encode()).hexdigest(), 16)

    def sign(self,message, private_key):
        # This is a placeholder for signature generation
        k = random.randrange(1, self.mod)
        r, _ = self.scalar_multiplication(k, self.generator)
        s = (self.hash_msg(message) + r * private_key) * pow(k, -1, self.order) % self.order
        return (r, s)

    def sign_verify(self,message, signature, public_key):
        # This is a placeholder for signature verification
        r, s = signature
        w = pow(s, -1, self.order)
        u1 = self.hash_msg(message) * w % self.order
        u2 = r * w % self.order
        x, _ = self.point_addition(self.scalar_multiplication(u1, self.generator), self.scalar_multiplication(u2, public_key))
        return x == r


