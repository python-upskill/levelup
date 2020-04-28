# Combat database

Currently you have an API that can conduct a combat between two monsters. Now it's time to save some data to database.

Use an ORM and create a database that will store this information:

- Monster info (store information about monster, so that when monster is in fight second time it won't be downloaded again)
- Fights and victories (store them in db so that they could be reviewed later)

After it, please add new endpoints to your API that would allow to GET lists and details of all your tables.

Additionally, allow filtering and searching for stuff in your API.

Examples:

```
/monsters/?damage_dice=4
/victories/?ko=false
/fights/?length=7
```

It's up to you how to shape the db schema, but please create at list one foreign key relation.

## Useful hints

- [Simple ORM for Python](https://github.com/coleifer/peewee)


## Additional challenges

### More filter options

Implement more custom filtering options to your APIs:

1. Comparison operators (`/monsters/?damage_dice__lessthan=6`)
2. Search with partial match (`/monsters/?name=gob` returning `goblin` and `hobgoblin`)
3. Complex filters (`/fights/?combatants["name"]='dragon'`)

Also - add pagination to your API.

### Monster CRUD

Add support to POST/PATCH/PUT/DELETE methods to monster API to allow managing custom monsters.

### Docker

Contenerize your application with PostgreSQL or MySQL database container.
