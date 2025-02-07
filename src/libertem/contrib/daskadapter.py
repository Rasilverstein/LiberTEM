import dask
import dask.array


def make_dask_array(dataset, dtype='float32', roi=None):
    '''
    Create a Dask array using the DataSet's partitions as blocks.
    '''
    chunks = []
    workers = {}
    for p in dataset.get_partitions():
        d = dask.delayed(p.get_macrotile)(
            dest_dtype=dtype, roi=roi
        )
        workers[d] = p.get_locations()
        chunks.append(
            dask.array.from_delayed(
                d,
                dtype=dtype,
                shape=p.slice.adjust_for_roi(roi).shape,
            )
        )
    arr = dask.array.concatenate(chunks, axis=0)
    if roi is None:
        arr = arr.reshape(dataset.shape)
    return (arr, workers)
