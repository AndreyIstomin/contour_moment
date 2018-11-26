from moment import Moment
import ogr
import os
from multiprocessing import Pool
from collections import namedtuple

field_list = ['geom', 'p', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7']
feature_tuple = namedtuple('feature_tuple', ','.join(field_list))


def save_features_to_file(output_path, features):
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(output_path):
        outDriver.DeleteDataSource(output_path)

    outDataSource = outDriver.CreateDataSource(output_path)
    out_lyr_name = os.path.splitext(os.path.split(output_path)[1])[0]
    outLayer = outDataSource.CreateLayer(out_lyr_name, geom_type=ogr.wkbPolygon)
    for each in field_list:
        fieldDefn = ogr.FieldDefn(each, ogr.OFTReal)
        outLayer.CreateField(fieldDefn)

    count = 0
    for feature in features:
        outFeature = ogr.Feature(outLayer.GetLayerDefn())
        outFeature.SetGeometry(feature.geom)
        for i, item in enumerate(field_list[1:-1:]):
            outFeature.SetField(item, feature[i+1])
        outLayer.CreateFeature(outFeature)
        count+=1
        # print (count)
        outFeature = None
    outDataSource = None

def executor(geom):
    try:
        m = Moment(geom)
        mm = m.compute(0, 0, central=True)
    except Exception:
        print(geom)
        return None
    else:
        sum = 0
        arr = []
        for i in range(0, 7):
            hu = m.compute_hu(i, scale_inv=True)
            arr.append(hu)
            sum += hu**2
        return (geom, mm, *arr)

def helper(args):
    a = executor(args[0])
    return a


if __name__ == '__main__':
    res_dir = os.path.join(os.path.dirname(__file__), 'test_resources')
    inShapefile = os.path.join(res_dir, 'russia_south_village_3857.shp')
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(inShapefile, 0)
    inLayer = inDataSource.GetLayer()

    output_path = os.path.join(os.path.split(inShapefile)[0], "moments.shp")

    ds = inDriver.Open(inShapefile, 0)

    lay = ds.GetLayer()
    geometries = []

    inLayerDefn = lay.GetLayerDefn()
    executor_args =[]
    count = 0
    for feature in lay:
        try:
            ingeom = feature.GetGeometryRef().Clone()
        except:
            pass
        else:
            executor_args.append((ingeom, ))
            count += 1
        if count> 10:
            break

    features = []
    pool = Pool(8)
    res = pool.map(helper, executor_args)
    pool.close()
    pool.join()
    for each in res:
        if each is not None:
            features.append(feature_tuple(*each))
    save_features_to_file(output_path, features)
    inDataSource = None
    print('end')