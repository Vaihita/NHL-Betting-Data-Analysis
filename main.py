import NHL


while True:
    choice = input("\n \t Which data you'd like to obtain:\n\
                        a. NHL\n\
                        b. Exit\n\
                        Your Choose: ")
    if choice == "a":
        NHL.main()
    elif choice == "b":
        print("\n \t Thank You for Using!!")
        break
    else:
        print("\n \t No Such Option, Try Again")
