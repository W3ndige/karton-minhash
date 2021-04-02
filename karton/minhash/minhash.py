import requests
import datasketch

from typing import Dict, List
from karton.core import Karton, Task, Config


def post_minhash_to_sample(url: str, sha256: str, minhash_input=Dict) -> Dict:
    try:
        r = requests.post(f"{url}/sample/{sha256}/minhash", json=minhash_input)
    except ConnectionError:
        return None

    return r.json()


def extract_ngrams(data: List[any], n: int = 4):
    output = []

    if n == 1:
        return data

    for i in range(len(data) - n - 1):
        output.append(" ".join(data[i : i + n]))

    return output


class AuroraConfig(Config):
    def __init__(self, path=None) -> None:
        super().__init__(path)
        self.aurora_config = dict(self.config.items("aurora"))


class Minhash(Karton):
    """
    Calculates minhash value for the supplied feature data.

    Entrypoint for raw feature data. Calculates minhash value from
    the supplied data, allowing for further similarity matching.
    """

    identity = "karton.minhash"
    filters = [
        {
            "type": "feature",
            "stage": "raw"
        }
    ]

    def process(self, task: Task) -> None:
        sha256 = task.get_payload("sha256")
        data = task.get_payload("data")

        if task.headers["kind"] == "disasm":
            data = extract_ngrams(data)

        lean_minhash = self.process_minhash(data)
        minhash_input = {
            "seed": lean_minhash.seed,
            "hash_values": lean_minhash.hashvalues.tolist(),
            "minhash_type": task.headers["kind"].upper(),
        }

        post_json = post_minhash_to_sample(
            self.config.aurora_config["url"],
            sha256,
            minhash_input,
        )

        if not post_json:
            self.log.error(f"Couldn't send Minhash to sample {sha256}")

        task = Task(
            {
                "type": "feature",
                "kind": task.headers["kind"],
                "stage": "minhash"
            }
        )

        task.add_payload("sha256", sha256)
        task.add_payload("seed", lean_minhash.seed)
        task.add_payload("hash_values", lean_minhash.hashvalues.tolist())

        self.send_task(task)


    def process_minhash(self, data: List[str]) -> None:
        minhash = datasketch.MinHash(num_perm=256)
        for value in data:
            minhash.update(value.encode("utf-8"))

        return datasketch.LeanMinHash(minhash)
