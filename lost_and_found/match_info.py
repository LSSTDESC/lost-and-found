from typing import List, Optional


class MatchInfo:
    def __init__(
        self,
        matches: List[List[int]],
        true_inds: List[int],
        pred_inds: List[int],
        weights: Optional[List[List[float]]] = None,
        ancil=None,
    ):
        """
        Initialize MatchInfo.

        Args:
            matches: List of lists one per true object, where each sublist are the
                predicted indices of predicted objects that are matched with the
                corresponding true object.
            weights: List of lists, same shape as matches, where each entry
                is the weight of the match. If `None`, all weights are set to 1.
                (e.g inverse distance)
            true_inds: List of true indices.
            pred_inds: List of predicted indices.
            ancil: ID numbers, etc.

        TODO: consider ingesting distance and also using it as a weight.
        TODO: Consider using the number of matches to a given object as a weight.

        Pathological cases:
            - Naive matching algorithm with radius = inf, saturates precion and recall
            - Detection algorithm that outputs many spurious predictions

        Framing:
            true_positives = set([x for match in self.matches for x in match])
            false_positives = self.found
            false_negatives = self.lost
            # tp + fn = total truth
            # tp + fp = total predicted
            # Notion of negative only if we did this pixel-wise
            # precision and recall will be saturated by a naive algorithm if we allow multiple matches per object

            # another framing
            # tp = set(true_inds) - set(self.lost)
            # precision = tp / (# total number of predictions)
            # recall = tp / t
        """
        # TODO: Generalize this later
        assert len(matches) == len(true_inds)

        self.matches = matches
        self.lost = self._get_lost()
        self.found = self._get_found(pred_inds)
        self.weights = weights
        self.ancil = ancil

        if weights is None:
            self.weights = [[1 for _ in range(len(m))] for m in self.matches]

    def _get_lost(self) -> List[int]:
        """Return all true indices with no predicted matches."""
        id_lost = []
        for i, true_id in enumerate(self.matches):
            if true_id == []:
                id_lost.append(i)
        return id_lost

    def _get_found(self, pred_inds: List[int]) -> List[int]:
        """Return all predicted indices with no truth matches."""
        all_pred_ids = set(pred_inds)
        flatmatch = set([x for match in self.matches for x in match])
        id_found = all_pred_ids - flatmatch
        return list(id_found)

    def _get_best(self):
        """For each true object, return the pred index of match with highest weight."""
        raise NotImplementedError()

    def count_matches(self) -> List[int]:
        """For each true object, return number of matches."""
        counts = [len(match) for match in self.matches]
        return counts

    # the non-image metrics here
    def get_tp(self) -> int:
        """Return true positives, # of predicted objects matched with a true object."""
        return len(set([x for match in self.matches for x in match]))

    def get_fp(self) -> int:
        """Return false positives, # of predicted not matched with any true object."""
        return len(self.found)

    def get_fn(self) -> int:
        """Return false negatives, defined as..."""
        raise NotImplementedError()

    def get_tn(self) -> int:
        """Return true negatives, defined as..."""
        raise NotImplementedError()

    def get_precision(self) -> float:
        """Return precision defined as tp/(tp+fp)

        NOTE: Could define as tp / (sum of weights of all matches). That way if naive alg. matches 1 pred with everything , precision will be low.

        NOTE: intuitively , precision should be high if only a few matches and
        weights are relatively high for those few matches.
        """
        tp = self.get_tp()
        fp = self.get_fp()
        return tp / (fp + tp)

    def get_recall(self) -> float:
        """Return recall, defined as tp / n_truth"""
        tp = self.get_tp()
        n_truth = len(self.matches)
        return tp / n_truth

    def __str__(self):
        # gives IQR of matches, count lost, count found
        return "hello world"
