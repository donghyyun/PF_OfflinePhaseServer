import numpy as np

from radiomap_construction import WSCollectedDetails
from save_data import CollectionDetails, InsertDBConnector
from setting import FINGERPRINT, POINT


def ws_get_rm_points(collected_details):
    details = WSCollectedDetails(collected_details)
    fingerprints = details.to_fingerprints()

    delta = (details.distance + 1) / len(fingerprints)
    docs = []
    for idx_, fingerprint in enumerate(fingerprints):
        delta_x, delta_y = delta * idx_ * np.cos(details.angle), delta * idx_ * np.sin(details.angle)
        new_coordinate = np.round(details.start_point + np.array([delta_x, delta_y]), 2)
        docs.append({
            FINGERPRINT: fingerprint,
            POINT: new_coordinate.tolist()
        })

    return docs


def ws_rm_construction(collected_details):
    rm_points = ws_get_rm_points(collected_details)
    InsertDBConnector().insert_rm_points(rm_points)


if __name__ == '__main__':
    collection_details = CollectionDetails()
    collection_details.coordinate = (0, 4, 0, 30)
    collection_details.save_start_time = "2021-04-08 21:40:31"
    collection_details.save_stop_time = "2021-04-08 21:41:17"

    radio_map = ws_get_rm_points(collection_details)
    for fp in radio_map:
        print(fp)
    print('total training point:', len(radio_map))

    import save_data.FindDBConnector
    save_data.FindDBConnector().close()
