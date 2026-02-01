#i figerd out how to commet i hope reading the script files for rain world dowporw
def calculator(a,b,op):
    if op == "+" or op == "add":
        return a+b
    elif op == "-" or op == "subtract":
        return a-b
    elif op == "multiply" or op == "*":
        return a*b
    elif op == "divide" or op == "/" or op == "÷":
        if b == 0:
            print("can'nt divied by 0")
        else:
            return a/b
    elif op == "%" or op == "mod" or op == "modulous":
        return a % b
    elif op == "cba" or op == "chess battle advanced" :
        if b == 0:
            print("can'nt chess the battle of 0 advanced")
        else :
            return a+b*a-b%a/b

        
aa=int(input("wats the first number "))
ba=int(input("whats the second number "))
opa=input("whats your operation ")
print(calculator(aa,ba,opa))

