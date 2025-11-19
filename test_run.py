from geom_utils import dist, midpoint, vec, dot, cross, normalize, perpendicular

print("---- Geometry Function Tester ----")

A = None
B = None

while True:

    if A is None or B is None:
        print("\nEnter two points:")
        x1 = float(input("Enter x1: "))
        y1 = float(input("Enter y1: "))
        x2 = float(input("Enter x2: "))
        y2 = float(input("Enter y2: "))
        A = (x1, y1)
        B = (x2, y2)

    print("\nChoose a function to test:")
    print("1) dist")
    print("2) midpoint")
    print("3) vec")
    print("4) dot (needs vector C)")
    print("5) cross (needs vector C)")
    print("6) normalize (A→B)")
    print("7) perpendicular (A→B)")

    choice = input("Enter number: ")

    if choice == "1":
        print("dist =", dist(A, B))

    elif choice == "2":
        print("midpoint =", midpoint(A, B))

    elif choice == "3":
        print("vec =", vec(A, B))

    elif choice == "4":
        x3 = float(input("Enter Cx: "))
        y3 = float(input("Enter Cy: "))
        C = (x3, y3)
        print("dot =", dot(vec(A, B), C))

    elif choice == "5":
        x3 = float(input("Enter Cx: "))
        y3 = float(input("Enter Cy: "))
        C = (x3, y3)
        print("cross =", cross(vec(A, B), C))

    elif choice == "6":
        print("normalize =", normalize(vec(A, B)))

    elif choice == "7":
        print("perpendicular =", perpendicular(vec(A, B)))

    else:
        print("Invalid choice.")

    again = input("\nDo you want to do another operation? (y/n): ").lower()
    if again != "y":
        print("Goodbye!")
        break

    same = input("Use SAME points? (y/n): ").lower()
    if same != "y":
        A = None
        B = None
