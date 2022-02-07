
class Mode1(Exception):
    def __init(self,msg):
        super().__init__(msg)
class Mode2(Exception):
    def __init(self, msg):
        super().__init__(msg)

a = input("Enter your name : ")
try:
    if a == "shobhit":
        raise Mode1("sp")
    if a == "rajeshwari":
        raise Mode2("ru")


except Mode1:
    print("Name was Shobhit")
    try:
        if a == "shobhit":
            raise Mode1("sp")
        if a == "rajeshwari":
            raise Mode2("ru")

except Mode2:
    print("Name was Rajeshwari")

finally:
    print("Finally Statement")

print("The End")





try:



except:


finally:








