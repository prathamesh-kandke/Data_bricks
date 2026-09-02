'''x = int(input("Enter a number: "))
y = int(input("Enter another number: "))

if x > y:
    print(f'{x} is greater than {y}')

else:
    print(f'{y} is greater than {x}')

print("Program Executed Successfully")'''

'''str1 = "AI With Python"
str2 = "    AI with Python"

if str1.upper() == str2.upper().strip():
    print("Both String are Same")

else:
    print("Both String are Different")'''

'''a = int(input("Enter a number: "))
b = int(input("Enter another number: "))

if (a > b) and (a != b):
    print("if block executed")

else:
    print("else block executed")'''


'''a = int(input("Enter a number: "))
b = int(input("Enter another number: "))

if (a > b) or (a != b):
    print("if block executed")

else:
    print("else block executed")'''

#no = int(input("Enter a number: "))

# if no%2==0:
#     print(f'{no} is even')
#
# else:
#     print(f'{no} is odd')

str1 = input("Enter a word to check palindrome :")
# str2=""
str1 = str1.lower()

if str1 == str1[::-1]:
    print("palindrome")

else:
    print("not palindrome")

# for i in str1:
#     if str2 == str1[::-1]:
#         print("palindrome")
#     else:
#         print("not palindrome")