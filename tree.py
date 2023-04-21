from saveload import *

#################################Job class######################################
# used for store information for each tree node
class Job:
    """
    Job Info
    """
    # def __init__(self, title, company, location, joburl, companyurl, function, 
    #              isTech, type, salary, skill, isGoodAt):
    def __init__(self, json):
        self.title = json['title']
        self.company = json['company']
        self.location = json['location']
        self.joburl = json['joburl']
        self.companyurl = json['companyurl']
        self.function = json['function']
        self.type = json['type']
        self.salary = json['salary']
        self.skill = json['skill']
        # if (self.skill != 'not good at'):
        #     self.isGoodAt = 'No'
        # else:
        #     self.isGoodAt = 'Yes'

#################################tree & Node class################################
questionAll = [
                'Do you want to find internship?',
                'Do you want to do technical job?',
                'Are you good at Java/ C++/ Python/ Sql/ Matlab/ Aws(one of these is fine)?',
                'Do you want to work in Big City(New York/ Chicago/ Los Angeles/ Houston)'
                ]
def isIntern(val):
    if 'internship' == val.type.lower():
        return True
    return False
def isTech(val):
    if 'engineer' in val.function.lower():
        return True
    return False
def isSkilled(val):
    if 'not good at' != val.skill.lower():
        return True
    return False
def isBig(val):
    for i in ['new york', 'chicago', 'los angeles', 'houston']:
        if i in val.location.lower():
            return True
    return False


class Node:
    def __init__(self, val, depth=0):
        # depth = None if val is Job, depth is integer if val is question
        self.left = None
        self.right = None
        self.depth = depth
        if (depth != 0):
            self.val = [val]
        else:
            self.val = val

class jobTree:
    def createNode(self, data, depth=0):
        """
        Utility function to create a node.
        """
        return Node(data, depth)
    def insertQuestion(self, node, data):
        if node == None:
            node = self.createNode(data)
            node.depth += 1
            return node
        else:
            node.left = self.insertQuestion(node.left, data)
            node.left.depth = node.depth + 1
            node.right = self.insertQuestion(node.right, data)
            node.right.depth = node.depth + 1
        return node
    def insertJob(self, node, val):
        if node == None:
            node = self.createNode(val, depth=5)
            # node.depth += 1
            return node
        if (node.depth == 1):
            if isIntern(val):
                return self.insertJob(node.left, val)
            return self.insertJob(node.right, val)
        elif (node.depth == 2):
            if isTech(val):
                return self.insertJob(node.left, val)
            return self.insertJob(node.right, val)
        elif (node.depth == 3):
            if isSkilled(val):
                return self.insertJob(node.left, val)
            return self.insertJob(node.right, val)
        elif (node.depth == 4):
            if isBig(val):
                node.left = self.insertJob(node.left, val)
                return node.left
            node.right = self.insertJob(node.right, val)
            return node.right
        else:
            node.val.append(val)
            # print(val.location)
        return node
def main(q1,q2,q3,q4):
    # load cache file 
    cache_list = open_cache('cache.json')
    job_list = [Job(i) for i in cache_list]
    # declare a tree
    tree = jobTree()
    root = None
    # insert question to tree
    root = tree.insertQuestion(root, questionAll[0])
    for i in range(1,len(questionAll)):
        tree.insertQuestion(root, questionAll[i])
    for i in job_list:
        tree.insertJob(root, i)
    job_desired = simplePlay(root,q1,q2,q3,q4)
    return job_desired


def simplePlay(tree,q1,q2,q3,q4):
    """
    plays the game once by using the tree to guide its questions.
    
    Parameters
    ----------
    tree: root of tree
    
    Returns
    -------
    bool
        returns True or False 
        depending on whether the computer guessed correctly

    
    """
    try:
        text, left, right = tree.val, tree.left, tree.right
    except:
        print('No suitable job!')
        return None
    # if left is None and right is None and text is None:
    #     print('No suitable job!')
    #     return []
    if left is None and right is None:
        count = 1
        try:
            for i in tree.val:
            #     print(f'{count}.')
                count += 1
            #     print(i.title)
            #     print(i.location)
            #     print(i.joburl)
            return tree.val
        except:
            # print('No suitable job!')
            return None
    else:
        # prompt = input(f'{text} ')
        if (tree.depth == 1):
            prompt = q1
        elif (tree.depth == 2):
            prompt = q2
        elif (tree.depth == 3):
            prompt = q3
        elif (tree.depth == 4):
            prompt = q4
        if yes(prompt):
            tree = left
        else:
            tree = right
        return simplePlay(tree,q1,q2,q3,q4)

def yes(prompt):
    """
    Uses the prompt to ask the user a yes/no question

    Parameters
    ----------
    prompt: string

    Returns
    -------
        returns True if the answer is yes, False if it is no.
    """
    if prompt.lower().strip() in ['yes', 'y', 'sure', 'yup']:
        return True
    # elif prompt.lower() in ['no', 'n', 'not']:
    else:
        return False

if __name__ == '__main__':
    main('yes', 'yes', 'yes', 'yes')