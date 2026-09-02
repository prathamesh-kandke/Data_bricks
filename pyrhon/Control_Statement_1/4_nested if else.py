'''marks = int(input("Enter your marks: "))

if marks >= 150:
    print("Admission to medical")
    if marks >= 185:
        print("Admission to medical MBBS")
    elif marks >= 170:
        print("Admission to medical BHMS")
    else:
        print("Admission to medical BDS")

else:
    print("Admission to Engineering")
    if marks >= 140:
        print("Admission to Computer Engineering")
    elif marks >= 130:
        print("Admission to Civil Engineering")
    else:
        print("Admission to Other Engineering Branch")'''

year = int(input("Enter year: "))
'''if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print("Its a leap year")
else:
    print("Not a leap year")'''

if year % 4 == 0:
    if year % 100 == 0:
        if year % 400 == 0:
            print("Its a leap year")
        else:
            print("Not a leap year")
    else:
        print("Its a leap year")
else:
    print("Its not a leap year")
