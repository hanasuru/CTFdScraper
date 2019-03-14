Description:
`nc quantumbomb.live 1337`

You have a bomb and will receive a random qubit to query the bomb. You’re allowed to apply any unitary matrix to this query, and it’ll query the bomb in superposition of whether or not it’s a bomb. 'If the bomb measures |1>, it will explode. If the bomb measures |0>, it does nothing. ' Nothing is measured if there is no bomb.

gates are inputed as:

`numbers = np.matrix([[complex(numbers[0]), complex(numbers[1])], [
                        complex(numbers[2]), complex(numbers[3])]])`


_by asper_