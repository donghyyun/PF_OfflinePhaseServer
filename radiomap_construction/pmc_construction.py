from radiomap_construction import PMCCollectedDetails
from save_data import CollectionDetails, InsertDBConnector
from setting import FINGERPRINT, POINT


def pmc_get_rm_points(collected_details):
    details = PMCCollectedDetails(collected_details)
    fingerprint = details.to_fingerprints()

    docs = [{
        FINGERPRINT: fingerprint,
        POINT: details.point,
        'collection_time': details.collection_time,
        'DEBUG_num_of_collected_rss': collected_details.record_count()
    }]

    return docs


def pmc_rm_construction(collected_details):
    rm_points = pmc_get_rm_points(collected_details)
    InsertDBConnector().insert_rm_points(rm_points)


if __name__ == '__main__':
    collection_details = CollectionDetails()
    collection_details.coordinate = (4, 14)
    collection_details.save_start_time = "2021-04-08 21:40:31"
    collection_details.save_stop_time = "2021-04-08 21:41:17"

    radio_map = pmc_get_rm_points(collection_details)
    for fp in radio_map:
        print(fp)
    print('total training point:', len(radio_map))
