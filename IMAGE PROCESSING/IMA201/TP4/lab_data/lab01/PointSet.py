from typing import List, Tuple

from enum import Enum
import numpy as np

class FeaturesTypes(Enum):
    """Enumerate possible features types"""
    BOOLEAN=0
    CLASSES=1
    REAL=2

class PointSet:
    """A class representing set of training points.

    Attributes
    ----------
        types : List[FeaturesTypes]
            Each element of this list is the type of one of the
            features of each point
        features : np.array[float]
            2D array containing the features of the points. Each line
            corresponds to a point, each column to a feature.
        labels : np.array[bool]
            1D array containing the labels of the points.
    """
    def __init__(self, features: List[List[float]], labels: List[bool], types: List[FeaturesTypes]):
        """
        Parameters
        ----------
        features : List[List[float]]
            The features of the points. Each sublist contained in the
            list represents a point, each of its elements is a feature
            of the point. All the sublists should have the same size as
            the `types` parameter, and the list itself should have the
            same size as the `labels` parameter.
        labels : List[bool]
            The labels of the points.
        types : List[FeaturesTypes]
            The types of the features of the points.
        """
        self.types = types
        self.features = np.array(features)
        self.labels = np.array(labels)
        self.best_split_number = 0
        self.id = 0
        self.best_gain = 0
        self.col = 0
    
    def get_gini(self, split = None) -> float:
        """Computes the Gini score of the set of points
        Returns
        -------
        float
            The Gini score of the set of points
            
        """
        if split is None:
            labels = self.labels
        else:
            labels = split

        gini_result = 0.0
        
        for label in np.unique(labels):
            p = np.sum(labels == label)/len(labels)
            gini_result += p ** 2
    
        return 1-gini_result
    
    def get_best_gain(self) -> Tuple[int, float]:
        """Compute the feature along which splitting provself.ides the best gain

        Returns
        -------
        int
            The self.id of the feature along which splitting the set provself.ides the
            best Gini gain.
        float
            The best Gini gain achievable by splitting this set along one of
            its features.
        """
        self.best_gain = 0
        self.id = 0
        orig_gini = self.get_gini()
        
        
        for i in range(self.features.shape[1]):
        
            if(self.types[i] == FeaturesTypes.CLASSES or self.types[i] == FeaturesTypes.BOOLEAN):
        
                feature_values = self.features[:, i]
                classes = np.unique(feature_values)
                for c in classes:
                    
                    subset_0 = self.labels[feature_values == c]
                    subset_1 = self.labels[feature_values != c]
                    gini_split_0 = len(subset_0)/len(feature_values)*self.get_gini(split = subset_0)
                    gini_split_1 = len(subset_1)/len(feature_values)*self.get_gini(split = subset_1)
        
                    gini_gain = orig_gini - gini_split_1 - gini_split_0
                    if (gini_gain > self.best_gain ):
                        self.id = i
                        self.best_gain = gini_gain
                        self.best_split_number = c
            if(self.types[i] == FeaturesTypes.REAL):
        
                feature_values = self.features[:, i]
                classes = np.unique(feature_values)
                for c in classes:
                    
                    subset_0 = self.labels[feature_values < c]
                    subset_1 = self.labels[feature_values >= c]
                    gini_split_0 = len(subset_0)/len(feature_values)*self.get_gini(split = subset_0)
                    gini_split_1 = len(subset_1)/len(feature_values)*self.get_gini(split = subset_1)
        
                    gini_gain = orig_gini - gini_split_1 - gini_split_0
                    if (gini_gain > self.best_gain ):
                        self.id = i
                        self.best_gain = gini_gain
                        self.best_split_number = c
                    
                    subset_0 = self.labels[feature_values < self.best_split_number]
                    subset_1 = self.labels[feature_values >= self.best_split_number]
               
        return self.id, self.best_gain

    def get_best_threshold(self) -> float:
        if(self.types[self.id] == FeaturesTypes.BOOLEAN):
            return None
        
        if(self.types[self.id] == FeaturesTypes.CLASSES):
            return self.best_split_number
        
        if(self.types[self.id] == FeaturesTypes.REAL):
            
            feature_values = self.features[:, self.id]
            
            subset_0 = feature_values[feature_values < self.best_split_number]
            subset_1 = feature_values[feature_values >= self.best_split_number]
            L = np.max(subset_0)
            R = np.min(subset_1)
            
            return (R+L)/2

    def more_votes(self):
        c0=np.count_nonzero(self.labels==0)
        c1= np.count_nonzero(self.labels)
        return c1 > c0
        
                
        
            
            
        

