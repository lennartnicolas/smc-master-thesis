from scipy.spatial import distance
import numpy as np

def getOntoDict(df):
    '''
    Helper function to put ontology csv in a dataframe
    Returns: Dict
    '''
    tree_dict = {}
    for i, row in df.iterrows():
        x = np.array(row.tolist())
        x = x[x != 'nan']
        tree_dict[i] = x
    return tree_dict

def getColormap(arr):
    '''
    Helper function to convert unique strings to int array for colormap
    arguments: array of strings/classes
    returns: list of corresponding integers
    '''
    y   = list(set(arr))
    dic = dict(zip(y, list(range(1,len(arr)+1))))
    cmap = [dic[v] for v in arr]
    return cmap

def movePoint(center, point, distance):
    ''' 
    Move point along same line by distance
    arguments: center position, point position, distance value
    returns: new point position
    '''
    v = np.subtract(point, center)
    u = v / np.linalg.norm(v)
    moved_point = center + distance * u
    return moved_point

def shiftPoints(points, new_center):
    '''
    Shift points by preserving the shape
    arguments: 
    returns: shifted points array
    '''
    com = np.mean(points, axis=0)
    delta = new_center - com
    shifted_points = points + delta
    return shifted_points

def rotate(p, origin=(0, 0), degrees=0):
    '''
    Rotate points around origin
    arguments: array of tuples/points, origin point, amount of rotation in degrees
    returns: array of new point positions
    '''
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)

def computeCentroid(p):
    '''
    Compute centroid position of given array
    arguments: array of tuples/points
    returns: x,y tuple of centroid point position
    '''
    sx = np.sum(p[:,0])
    sy = np.sum(p[:,1])
    return sx / p.shape[0], sy / p.shape[0]

def reduceDistance(p, centroid, prob):
    '''
    Compute the reduced distance based on the probability value
    arguments: point tuple, centroid position, probability
    returns: reduced point positions 
    '''
    dist = np.subtract(p, centroid)
    point = centroid + dist * prob
    return point

def sumProbabilites(probDict, ontoRef):
    '''
    Sum probabilites of embeddings 'top25probabilitiesclasses' key
    arguments: probability dictionary, AudioSet ontology reference strings
    returns: probability value <= 1
    '''
    sum_probs = 0
    count = 0
    for key in probDict.keys():
        if probDict[key] < 0.1:
            continue
        if key in ontoRef:
            count += 1
            sum_probs += probDict[key]
    return sum_probs / count if count != 0 else 0

def getDistance(A,B):
    return distance.euclidean(A,B)

def computeDistances(p, centroid):
    return [getDistance(point, centroid) for point in p]

def getMaxValIndex(arr):
    return max(range(len(arr)), key=arr.__getitem__)

def getMinValIndex(arr):
    return min(range(len(arr)), key=arr.__getitem__)