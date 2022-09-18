## How to get started

### Install pte-xdf

```bash
$ pip install pte-xdf
```

### Use

```python
import pte_xdf

fname = "my_recording.xdf"
```

Load a recording and use only the stream with `'stream_id' = 1`.

```python
raw = pte_xdf.read_raw_xdf(fname=fname, stream_picks=1, verbose=True)
```

Output:
```
Reading file:
my_recording.xdf
Number of streams in file: 1.
Streams being loaded: 1.
```

Load a recording and use only the stream with `name' = 'SAGA'`.
```python
raw = pte_xdf.read_raw_xdf(fname, stream_picks='SAGA', verbose=True)
```

Output:
```
Reading file:
my_recording.xdf
Number of streams in file: 1.
Streams being loaded: SAGA.
```