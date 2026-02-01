#prime cheacker
n = int(input("enter a number: "))
is_prime = True


if n <= 1:
    is_prime = False
else:
    for i in range(2,n):
        if n%i == 0:
            is_prime = False
            break
            
if is_prime:
    print("prime number")
else:
    print("not prime")