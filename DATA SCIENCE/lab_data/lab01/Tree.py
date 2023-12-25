from typing import List

import numpy as np

from PointSet import PointSet, FeaturesTypes

class Tree:
    """A decision Tree

    Attributes
    ----------
        points : PointSet
            The training points of the tree
    """
    def __init__(self,
                 features: List[List[float]],
                 labels: List[bool],
                 types: List[FeaturesTypes],
                 h: int = 1):
        """
        Parameters
        ----------
            labels : List[bool]
                The labels of the training points.
            features : List[List[float]]
                The features of the training points. Each sublist
                represents a single point. The sublists should have
                the same length as the `types` parameter, while the
                list itself should have the same length as the
                `labels` parameter.
            types : List[FeaturesTypes]
                The types of the features.
        """
        self.points = PointSet(features, labels, types)
        self.h = h
        self.feature_index, gain = self.points.get_best_gain()
        if h>=1:
            
            list_features_0, list_labels_0 = [], []
            list_features_1, list_labels_1 = [], []
            
            for i in range(len(self.points.labels)):
                if(self.points.types[self.feature_index]==FeaturesTypes.CLASSES):
                    if self.points.features[i][self.feature_index] == self.points.get_best_threshold():
                        list_features_0.append(self.points.features[i])
                        list_labels_0.append(self.points.labels[i])
                    else:
                        list_features_1.append(self.points.features[i])
                        list_labels_1.append(self.points.labels[i])
                if(self.points.types[self.feature_index]==FeaturesTypes.BOOLEAN):
                    if self.points.features[i][self.feature_index] == 0:
                        list_features_0.append(self.points.features[i])
                        list_labels_0.append(self.points.labels[i])
                    else:
                        list_features_1.append(self.points.features[i])
                        list_labels_1.append(self.points.labels[i])
                if(self.points.types[self.feature_index]==FeaturesTypes.REAL):
                    if self.points.features[i][self.feature_index] < self.points.get_best_threshold():
                        list_features_0.append(self.points.features[i])
                        list_labels_0.append(self.points.labels[i])
                    else:
                        list_features_1.append(self.points.features[i])
                        list_labels_1.append(self.points.labels[i])
            list_features_0, list_features_1 = np.array(list_features_0), np.array(list_features_1)
            
            if gain == 0 or h== 1:
                #print("Pointset")
                self.left = PointSet(list_features_0, list_labels_0, types)
                self.right = PointSet(list_features_1, list_labels_1,  types)

            else:
                if():
                    self.left = PointSet(list_features_0, list_labels_0, types)
                else:
                    self.left = Tree(list_features_0, list_labels_0, types, h = h-1)
                if(np.all(list_features_1) or not np.any(list_features_1)):
                    self.right = PointSet(list_features_1, list_labels_1, types)
                else:
                    self.right = Tree(list_features_1, list_labels_1, types, h = h-1)       


    def decide(self, features: List[float]) -> bool:
        """Give the guessed label of the tree to an unlabeled point

        Parameters
        ----------
            features : List[float]
                The features of the unlabeled point.

        Returns
        -------
            bool
                The label of the unlabeled point,
                guessed by the Tree
        """
        if(self.points.types[self.feature_index] ==FeaturesTypes.BOOLEAN):
            if features[self.feature_index] == 0:
                if(type(self.left) == Tree):
                    return self.left.decide(features)
                else:
                    return self.left.more_votes()
            else:
                if(type(self.right) == Tree):
                    return self.right.decide(features)
                else:
                    return self.right.more_votes()
        if(self.points.types[self.feature_index] ==FeaturesTypes.REAL):
            if features[self.feature_index] < self.points.get_best_threshold():
                if(type(self.left) == Tree):
                    return self.left.decide(features)
                else:
                    return self.left.more_votes()
            else:
                if(type(self.right) == Tree):
                    return self.right.decide(features)
                else:
                    return self.right.more_votes()
        if(self.points.types[self.feature_index] ==FeaturesTypes.CLASSES):
            if features[self.feature_index] == self.points.get_best_threshold():
                if(type(self.left) == Tree):
                    return self.left.decide(features)
                else:
                    return self.left.more_votes()
            else:
                if(type(self.right) == Tree):
                    return self.right.decide(features)
                else:
                    return self.right.more_votes()

            
