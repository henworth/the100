# The100

An asynchronous Python client for accessing the100.io API. All GET endpoints that are currently exposed are supported by The100. Those can be seen in the100.io's official documentation [here](http://www.the100.io/api-docs/index.html).

Here are some examples of The100 in action (assuming this code is running in an event loop):

### Getting a User

```python
import the100

api = the100.The100('your-api-key')
json = await api.get_user('example')
api.close()
```

### Getting a Group

```python
import the100

api = the100.The100('your-api-key')
json = await await api.get_group(1234)
api.close()
```

### Getting a Group's Gaming Sessions

```python
import the100

api = the100.The100('your-api-key')
json = await api.get_group_gaming_sessions(1234)
api.close()
```

## Dependencies

- Python 3.6+
- `aiohttp` library
