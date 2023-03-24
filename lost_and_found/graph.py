from typing import List

from networkx import Graph, is_bipartite


class BlendBipartite(Graph):
    """Graph that encodes matches between true and predicted objects."""

    def __init__(self, incoming_graph_data=None, **attr):
        """Initialize BlendBipartite instance."""
        super().__init__(incoming_graph_data, **attr)

        # reqs: position information,
        # edges: match information,
        # optional (metadata): ellipticity information, angle, hlr, etc.

        for n in self.nodes(data=True):
            _, data = n
            assert data["grp"] in ["true", "pred"]
            assert isinstance(data["ra"], float)
            assert isinstance(data["dec"], float)
            assert isinstance(data["id"], int)

        for e in self.edges(data=True):
            _, _, data = e
            assert isinstance(data["weight"], float)
            assert data["weight"] >= 0

    def get_lost(self) -> List[int]:
        """Return all true indices with no predicted matches."""
        id_lost = []
        for n in self.nodes(data=True):
            _, data = n
            if data["grp"] == "true" and len(self[n]) == 0:
                id_lost.append(data["id"])
        return id_lost

    def get_found(self) -> List[int]:
        """Return all predicted indices with no truth matches."""
        id_found = []
        for n in self.nodes(data=True):
            _, data = n
            if data["grp"] == "pred" and len(self[n]) == 0:
                id_found.append(data["id"])
        return id_found

    def count_matches(self) -> List[int]:
        """For each true object, return number of matches."""
        counts = []
        for n in self.nodes(data=True):
            _, data = n
            if data["grp"] == "true":
                counts.append(len(self[n]))
        return counts

    def get_matched(self) -> List[int]:
        """Return list of matched pred ids."""
        matched = []
        for n in self.nodes(data=True):
            _, data = n
            if data["grp"] == "pred" and len(self[n]) > 0:
                matched.append(data["id"])
        return matched

    def get_k_l_matches(self, k: int, l: int) -> List[int]:
        """Return nodes with k edges to true nodes and l edges to pred nodes."""
        pass

    def get_tp(self) -> int:
        """Return true positives: # of pred matched with truth."""
        return len(self.get_matched())


# NOTE: not restrict edges to be between true and pred nodes.
# Path: lost_and_found/match_info.py
