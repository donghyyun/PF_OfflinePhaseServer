import numpy as np

from radiomap_construction import CollectedDetails, CollectedRecords
from setting import NUM_PATH


def ws_rm_construction(collected_details_name):
    docs = []

    for idx in range(NUM_PATH):
        details = CollectedDetails(collected_details_name)
        details.set_details(idx)

        records = CollectedRecords(details)
        fingerprints = records.to_fingerprints()

        delta = (details.distance + 1) / len(fingerprints)

        for idx_, fingerprint in enumerate(fingerprints):
            delta_x, delta_y = delta * idx_ * np.cos(details.angle), delta * idx_ * np.sin(details.angle)
            new_coordinate = np.round(details.start_point + np.array([delta_x, delta_y]), 2)
            docs.append({
                'fingerprint': fingerprint,
                'coordinate': new_coordinate.tolist()
            })

    return docs


if __name__ == '__main__':
    save_inform = 'WS_save_inform(2021-04-08)'
    radio_map = ws_rm_construction(save_inform)
    for fp in radio_map:
        print(fp)
    print('total training point:', len(radio_map))

    import save_data.FindDBConnector
    save_data.FindDBConnector().close()
