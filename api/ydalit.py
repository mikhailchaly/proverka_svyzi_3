print("1-сложение")
print("2-вычитание")
print("3-умножение")
print("4-деление")
k=int(input("Вебрите действие "))

if k==1:
    a=int(input("Введи 1 число "))
    b=int(input("Введи 2 число "))
    print(f'{a} + {b} = {a+b}')