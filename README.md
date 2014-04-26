# BDQDB

Bugsduggan Quote Database

Yes, it's a silly name but it's also a pallindrome and I find that pleasing.

## API spec

### GET /v1/

* __search__ - A URL encoded string, matched exactly
* __random__ - Accepts any input

Returns all quotes. If search is specified, returns all quotes that contain
the search string. If random is specified, returns a single quote selected
at random.

#### Example response

```
[
  {
    "name": "bugsduggan",
    "quotes": [
      {
        "id": 0,
        "text": "bdqdb is the best qdb ever"
      }
    ]
  },
  {
    "name": "other_dude",
    "quotes": [
      {
        "id": 0,
        "text": "I like trains!"
      },
      {
        "id": 1,
        "text": "Are those my feet?"
      }
    ]
  }
]
```

### GET /v1/:name

* __search__ - A URL encoded string, matched exactly
* __random__ - Accepts any input

Returns all quotes stored under a particular name. If search is specified,
returns all quotes that contain the search string. If random is specified,
returns a single quote selected at random. If there are no quotes
stored under that name, returns 404.

### POST /v1/:name

Adds a new quote under `:name`. Returns 201 if successful. If no `text` attribute
can be found, returns 400.

#### Example request

```
{"text": "Mary had a little lamb"}
```

### GET /v1/:name/:id

Returns a single quote from `:name` with `:id`. If there is no quote under
`:name` with `:id`, returns 404.

### DELETE /v1/:name/:id

Deletes a quote from `:name` with `:id`. If there is no quote under `:name`
with `:id`, returns 404.
