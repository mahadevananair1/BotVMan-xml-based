x = input("enter 1st num")
y = input("enter 2st num")

try:
    sum = int(x) + int(y)
except:
    print("you typed a character")
print(sum)