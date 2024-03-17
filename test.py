import math

def format_root(n):
        N = abs(n)
        primes = []
        while N % 2 == 0:
            primes.append(2)
            N /= 2
        i = 3
        while i <= math.sqrt(abs(N)):
            if N % i == 0:
                primes.append(i)
                N /= i
            else:
                i += 2
        if N != 1:
            primes.append(int(N))

        outside = 1
        inside = 1
        index = 0
        while index < len(primes):
            num = primes[index]
            count = primes.count(num)
            if count > 0 :
                if count % 2 == 0:
                    outside *= (num ** (count/2))
                else: 
                    outside *= (num ** ((count-1)/2))
                    inside *= num
            index += count
        print(f"{int(outside)}√{int(inside)}")

format_root(19734132)