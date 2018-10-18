# Engines

### Engine blueprints
Located in `engines.blueprints`

## CacheBasedEngine

Run `redis-cli`and register a random recommendation
for `item_id=100` and engine `CacheBasedEngine`:

``` shell
set CacheBasedEngine-100 "[(1, 0.9), (2, 0.7)]"
```
