def get_gene_input():
    while True:
        power = input("Decide your power capability: ")
        movement = input("Decide your movement capability: ")
        bag_size = input("Decide your bag size: ")
        if not power or not movement or not bag_size:
            print("Re-enter.")
            continue
        if int(power) + int(movement) + int(bag_size) == 10:
            break
        print("Sum is not 10. Please re-input.\n")
    return int(power), int(movement), int(bag_size)
