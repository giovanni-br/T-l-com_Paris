from typing import List

def precision_recall(expected_results: List[bool], actual_results: List[bool]) -> (float, float):
    """Compute the precision and recall of a series of predictions

    Parameters
    ----------
        expected_results : List[bool]
            The true results, that is the results that the predictor
            should have find.
        actual_results : List[bool]
            The predicted results, that have to be evaluated.

    Returns
    -------
        float
            The precision of the predicted results.
        float
            The recall of the predicted results.
    """
    TP = 0
    FN, FP = 0, 0
    for i in range(len(expected_results)):
            if  actual_results[i] == True and expected_results[i] == False:
                FP += 1
            elif  actual_results[i] == False and expected_results[i] == True:
                FN +=1
            elif actual_results[i] ==True and  expected_results[i] == True:
                TP +=1
    if TP == 0:
        return 0,0
    else:
        return  TP/(TP+FP), TP/(TP+FN)
                
    
def F1_score(expected_results: List[bool], actual_results: List[bool]) -> float:
    """Compute the F1-score of a series of predictions

    Parameters
    ----------
        expected_results : List[bool]
            The true results, that is the results that the predictor
            should have find.
        actual_results : List[bool]
            The predicted results, that have to be evaluated.

    Returns
    -------
        float
            The F1-score of the predicted results.
    """
    
    precision, recall = precision_recall(expected_results, actual_results)
    if precision ==0 or recall==0:
        return 0
    else:
        return 2*(precision*recall)/(precision + recall)
