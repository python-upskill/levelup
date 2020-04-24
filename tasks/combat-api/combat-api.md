# Combat API

Now it's time to add some networking to our project. In this task you will add connection to API and make your app a REST API itself.

## Input

JSON POST request:

```json
{
  "combatants": ["orc", "goblin"],
  "max_rounds": 7
}
```

- `combatants` key is a list of two string elements (unless your code supports more than two combatants)
- `max_rounds` is an integer which sets maximum number of combat rounds. When this number of rounds passes and no monster won yet monsters with higher current hp wins.

In current version you do not get information about combatants in the API call. Instead of loading it from file you should use this API:

```
https://www.dnd5eapi.co/api/monsters/<combatant-name>
```

Example:

```
https://www.dnd5eapi.co/api/monsters/orc
```

In the json you'll get from this API look for three things:
- full name
- hit points number
- attack damage. Many monsters have multiple attack options, so pick any attack that has damage (attacks are in "actions" section).

Find a way to react to wrong entries sent in `combatants` key (use suitable error code and message).

### Hint

If you are looking for monster examples you could use lookup call to search by part of monster name:

```
https://www.dnd5eapi.co/api/monsters/?name=dragon
```

## Output

Output is similar as in previous task, but in JSON form:
```json
{
  "rounds": [
    {
      "round": 1,
      "attacker": "orc",
      "defender": "goblin",
      "damage": 8,
      "previous_hp": 40,
      "current_hp": 32,
    },
    {
      "round": 2,
      "attacker": "goblin",
      "defender": "orc",
      "damage": 6,
      "previous_hp": 55,
      "current_hp": 49,
    },
    {
      "round": 3,
      "attacker": "orc",
      "defender": "goblin",
      "damage": 2,
      "previous_hp": 32,
      "current_hp": 30,
    },
    {
      "round": 4,
      "attacker": "goblin",
      "defender": "orc",
      "damage": 6,
      "previous_hp": 49,
      "current_hp": 43,
    },
    {
      "round": 5,
      "attacker": "orc",
      "defender": "goblin",
      "damage": 8,
      "previous_hp": 30,
      "current_hp": 22,
    },
    {
      "round": 6,
      "attacker": "goblin",
      "defender": "orc",
      "damage": 5,
      "previous_hp": 43,
      "current_hp": 38,
    },
    {
      "round": 7,
      "attacker": "orc",
      "defender": "goblin",
      "damage": 2,
      "previous_hp": 22,
      "current_hp": 20,
    }
  ],
  "victory": {
    "winner": "orc",
    "rounds": 7,
    "ko": false
  }
}
```

## Useful hints

- [Python requests library](https://requests.readthedocs.io/en/master/)
- [REST API framework](https://falcon.readthedocs.io/en/stable/)

## Additional challenges

### Challenges from previous task

Both "Multiple combatants" or "Unit and integration tests" makes sense also here, so if you didn't do it in previous task you could try them now.

### Multiattack

Check monster JSON for action called "Multiattack" and if it has one, get damage information from all his attacks and use all of them in monster's turn.

### Combat record

Keep all combats that your API conducted in memory and add new method to your API - GET - that allows getting information about past fights.

Allow lookup by different parameters (monster name parts, number of rounds, ko, winner).