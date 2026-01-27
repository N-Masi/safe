# TODO: get more resolution stores
models = {
    'keisler': {
        '240x121': 'gs://weatherbench2/datasets/keisler/2020-240x121_equiangular_with_poles_conservative.zarr',
    },
    'pangu': {
        '240x121': 'gs://weatherbench2/datasets/pangu/2018-2022_0012_240x121_equiangular_with_poles_conservative.zarr',
        '1440x721': 'gs://weatherbench2/datasets/pangu/2018-2022_0012_0p25.zarr',
    },
    'graphcast': {
        '240x121': 'gs://weatherbench2/datasets/graphcast/2020/date_range_2019-11-16_2021-02-01_12_hours-240x121_equiangular_with_poles_conservative.zarr',
        '1440x721': 'gs://weatherbench2/datasets/graphcast/2020/date_range_2019-11-16_2021-02-01_12_hours_derived.zarr',
    },
    'sphericalcnn': {
        '240x121': 'gs://weatherbench2/datasets/sphericalcnn/2020-240x121_equiangular_with_poles.zarr',
    },
    'fuxi': {
        '240x121': 'gs://weatherbench2/datasets/fuxi/2020-240x121_equiangular_with_poles_conservative.zarr',
        '1440x721': 'gs://weatherbench2/datasets/fuxi/2020-1440x721.zarr',
    },
    'neuralgcm': {
        '240x121': 'gs://weatherbench2/datasets/neuralgcm_deterministic/2020-240x121_equiangular_with_poles_conservative.zarr',
    },
    'neuralgcm-ens-mean': {
        '64x32': 'gs://weatherbench2/datasets/neuralgcm_ens/2020-64x32_equiangular_conservative_mean.zarr',
        '240x121': 'gs://weatherbench2/datasets/neuralgcm_ens/2020-240x121_equiangular_with_poles_conservative_mean.zarr',
    },
    'ifs-hres': {
        '64x32': 'gs://weatherbench2/datasets/hres/2016-2022-0012-64x32_equiangular_conservative.zarr',
        '240x121': 'gs://weatherbench2/datasets/hres/2016-2022-0012-240x121_equiangular_with_poles_conservative.zarr',
        '512x256': 'gs://weatherbench2/datasets/hres/2016-2022-0012-512x256_equiangular_conservative.zarr',
        '1440x721': 'gs://weatherbench2/datasets/hres/2016-2022-0012-1440x721.zarr',    
    },
    'ifs-ens-mean': {
        '64x32': 'gs://weatherbench2/datasets/ifs_ens/2018-2022-64x32_equiangular_conservative_mean.zarr',
        '240x121': 'gs://weatherbench2/datasets/ifs_ens/2018-2022-240x121_equiangular_with_poles_conservative_mean.zarr',
        '1440x721': 'gs://weatherbench2/datasets/ifs_ens/2018-2022-1440x721_mean.zarr',
    },
}

era5 = {
    '64x32': 'gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-64x32_equiangular_conservative.zarr',
    '240x121': 'gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr',
    '1440x721': 'gs://weatherbench2/datasets/era5/1959-2023_01_10-wb13-6h-1440x721_with_derived_variables.zarr',
}
