# Walking Password Calculator (c)2020 @jekuz
#
# Walking password is a password of nearby buttons like 12345678
# You can change 'same_key' for getting 'stay on button' variants, shift, diagonal ways and length options.
# You will get all possible walking password variants from any key into 'passwords.txt' file

same_key = True
shift = True
diagonal_ways = False
password_length = 8
minimum_password_length = 3
file = open('passwords.txt', 'w')
keymap = ("               ",
          " `1234567890-= ",
          "  qwertyuiop[]\\",
          "  asdfghjkl;'  ",
          "  zxcvbnm,./   ",
          "               ")
usual_keys = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shift_keys = "~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"
key_reverse = {**dict(zip(usual_keys, shift_keys)), **dict(zip(shift_keys, usual_keys))}
password_counter_from_key = 0
data = {}


# Returns key's position(x,y) from keymap
def position(key):
    for y, row in enumerate(keymap):
        for x in range(len(row)):
            if keymap[y][x] == key:
                return x, y


# Returns keys string around start key
def keys_around(key):
    keys_around = ''
    if same_key:
        keys_around = key
    x, y = position(key)
    ways = [y, x + 1], [y + 1, x], [y, x - 1], [y - 1, x]
    if diagonal_ways:
        ways += [y + 1, x + 1], [y - 1, x - 1], [y + 1, x - 1], [y - 1, x + 1]
    for way in ways:
        try:
            next_key = keymap[way[0]][way[1]]
        except IndexError:
            continue
        if next_key != " ":
            keys_around += next_key
    return keys_around


# Returns password list of all shifted variants
def password_shifted(password):
    # Creating 'shifted' versions:
    # Getting all password variants in binary list of password
    # Example: '**' = ['00','01','10','11'] - 1 is shifted, 0 is not
    binary_list = []
    pass_count = 2 ** len(password)
    for i in range(pass_count):
        binary_list.append(str(format((pass_count + i), 'b')[1:]))

    password = [*password]
    pass_list = []

    # Getting all password versions according to binary list
    for binary_pattern in binary_list:
        for n, digit in enumerate(binary_pattern):
            if digit == '1' and password[n] in usual_keys:
                password[n] = key_reverse[password[n]]
            if digit == '0' and password[n] in shift_keys:
                password[n] = key_reverse[password[n]]
        # Convert password into string and adding into password list
        password_string = ''
        for key in password:
            password_string += key
        pass_list.append(password_string)

    return pass_list


# Passwords calculating and saving in file (recursion)
def password_calculator(key, password_length):
    global password_counter_from_key
    password_length -= 1
    if password_length == 0:
        return
    for next_key in data[key[-1]]:
        password = key + next_key
        if len(password) >= minimum_password_length:
            if shift:
                for variant in password_shifted(password):
                    file.write(variant + '\n')
                    password_counter_from_key += 1
            else:
                file.write(password + '\n')
                password_counter_from_key += 1
        password_calculator(password, password_length)


# Calculating all possible 'walking passwords' and saving into file
def main():
    total_password_counter = 0
    global password_counter_from_key

    # Creating dictionary where each start key have all keys around
    for key in usual_keys:
        data[key] = keys_around(key)

    # Calculating passwords starts from any key
    for key in usual_keys:
        print(f"Calculating passwords from key '{key}'.. ", end='')
        password_calculator(key, password_length)
        print(f"{password_counter_from_key}")
        total_password_counter += password_counter_from_key
        password_counter_from_key = 0
    print(f"\nTotal passwords: {total_password_counter}")
    file.close()


if __name__ == "__main__":
    main()
