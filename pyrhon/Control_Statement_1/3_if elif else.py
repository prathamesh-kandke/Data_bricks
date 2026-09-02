'''no1 = int(input("Enter first number: "))
no2 = int(input("Enter second number: "))
no3 = int(input("Enter third number: "))

if no1 > no2 and no1 > no3:
    print(f'{no1} is greater than {no2} and {no3}')

elif no2 > no1 and no2 > no3:
    print(f'{no2} is greater than {no1} and {no3}')

elif no3 > no1 and no3 > no2:
    print(f'{no3} is greater than {no1} and {no3}')

else:
    print("All number are same..")'''

print("Triangle and its types")
a = int(input("Enter first side of triangle : "))
b = int(input("Enter second side of triangle : "))
c = int(input("Enter third side of triangle : "))

if a == b ==c:
    print("Its a equilateral Triangle")

elif(a == b) or (a == c) or (b == c) or (b == a) or (c == a) or (c == b):
    print("Its a isosceles Triangle")

elif(a*a == b*b + c*c) or (b*b == a*a+c*c) or (c*c == a*a + b*b):
    print("Its a right angle Triangle")

else:
    print("Its a scaler Triangle")