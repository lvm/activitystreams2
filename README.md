# Activity Streams 2.0

A (hacky) library that allows creation of ActivityStreams 2.0 Types.

## Content

This lib contains:

* All properties defined in [W3C Activity Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)
* Models for the 8 Core Types (Object, Link, Activity, IntransitiveActivity, Collection, OrderedCollection, CollectionPage, OrderedCollectionPage)
* Everything you need to create Extended Types 

## Example

```
from activitystreams2 import make_activitystream_class, properties, OrderedCollection

Note = make_activitystream_class("Note", properties.OBJECT_PROPERTIES)

note1 = Note(id="https://example.com/1", name="hello world", content="hey!!")
note2 = Note(id="https://example.com/2", name="bye world", content="bye!!")
note3 = Note(id="https://example.com/3", name="end of the world", content="oh no")

notes = sorted([note3, note1, note2], key=lambda n: n.id)
for note in notes:
    note.dismiss_context()

collection = OrderedCollection(totalItems=len(notes), items=notes, current=0)

print(collection)
print(json.dumps(collection.asdict(), indent=2))
```

## Test

```
$ python3 -m unitest discover tests
```
Note: Tests are a bit lousy at the moment.

To properly test this lib, you can use the Test Suite provided in the [ActivityStreams github repo](https://github.com/w3c/activitystreams/tree/master/test).

```
$ git clone https://github.com/w3c/activitystreams /tmp/activitystreams
$ ./bin/activitystream-validator /tmp/activitystreams/test/simple0003.json
$ ./bin/mass-activitystream-validator /tmp/activitystreams/test/
```
Note: `vocabulary-ex196-jsonld.json` will always fail because it isn't [formatted correctly](https://github.com/w3c/activitystreams/blob/master/test/vocabulary-ex196-jsonld.json) (or at least `json.load` won't parse it).


## LICENSE

See [LICENSE](LICENSE)