# Combat arena

The objective of this task is to write a script that emulates a combat arena. We have two monsters that fight with each other and we want to know which one wins.

## Input

You have file `combatants.json` which contains monster info.

Example:

```json
[
  {
    "name": "Dragon",
    "hp": 100,
    "damage": "6d6 + 1"
  },
  {
    "name": "Demogorgon",
    "hp": 150,
    "damage": "3d10"
  }
]
```

## Output

Your script should show the consecutive combat rounds on the standard output.

### Output format

```
<round number> <attacker> <defender> <damage> <defender hp before attack> <defender hp after attack>
```

Last line should have information about who wins and in how many rounds.

Example:

```
1 Demogorgon Dragon 20 100 80
2 Dragon Demogorgon 19 150 131
3 Demogorgon Dragon 12 80 68
4 Dragon Demogorgon 14 131 117
5 Demogorgon Dragon 21 68 47
6 Dragon Demogorgon 23 117 94
7 Demogorgon Dragon 17 47 30
8 Dragon Demogorgon 26 94 68
9 Demogorgon Dragon 22 30 8
10 Dragon Demogorgon 18 68 50
11 Demogorgon Dragon 19 8 -11
Demogorgon wins in 11 rounds!
```

## Combat guide

1. Randomly choose first attacker
2. In his round, attacking monster is lowering defender's hp by a random number (see Determining damage below)
3. Monster switch roles (defender become attacker and vice versa)
4. Monsters fight until any monster's hp reaches 0 or below.

### Determining damage

We use dice notation to describe damage dealt by a monster.

```
XdY[ + Z]
```

means:
> Roll Y-sided dice X times, sum the results and in the end add Z

Example:

```
2d10 - roll two ten-sided dice and sum results (results ranging from 2 to 20)
3d6 + 10 - roll 3 six-sided dice, sum results and add 10 (results raging from 13 to 28)
```

## Useful hints

You'll probably need this information to finish this task:
- [convert string to int](https://realpython.com/convert-python-string-to-int/)
- [for loop](https://realpython.com/python-for-loop/)
- [JSON](https://pymotw.com/3/json/)
- [lists and tuples](https://realpython.com/python-lists-tuples/)
- [randint](https://realpython.com/python-random/)
- [reading files](https://realpython.com/working-with-files-in-python/)
- [string formatting](https://realpython.com/python-formatted-output/)
- [string operations](https://realpython.com/python-string-split-concatenate-join/)
- [while loop](https://realpython.com/python-while-loop/)

## Additional challenges

If you finish this script quickly you can reach for additional challenges or go to next task (if it's available)

### Multiple combatants

Change your script to support more than 2 combatants. Think about a **simple** algorithm of choosing who to attack.

Ideas:
- monster attacks weakest/strongest monster of others
- give monsters different types that will determine who to attack (like fire monster wants to attack water monster first etc.)
- give monsters damage types and resistances (getting half damage of chosen type) and decide monster will make most effective attack

Remember!
- we don't want monsters to attack dead monsters and dead monsters attacking alive ones (remove them from combat)
- change fight end condition to having only one monster alive

### Unit and integration tests

Using [pytest](https://realpython.com/pytest-python-testing/):
- Write unit tests for your code. Change your architecture so that during tests code will not read files and print output.
- Write an integration test that will test the whole stack on testing data and check information sent to standard output.