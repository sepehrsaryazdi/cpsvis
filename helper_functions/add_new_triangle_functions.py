from enum import unique
from lib2to3.pytree import convert
import numpy as np
import mpmath as mp
from scipy.fftpack import diff
mp.mp.dps = 300
mp.mp.pretty = False

def enumerate_classes(inverse_hash,limit):
    letters = list(inverse_hash.keys())
    
    
    unique_letters = []
    for letter in letters:
        if inverse_hash[letter] not in unique_letters:
            unique_letters.append(letter)

    enumerations = ["𝟙"]+unique_letters

    

    def inverse(string):
        
        new_string = []
        for x in string[::-1]:
            new_string.append(inverse_hash[x])
        return ''.join(new_string)

    def check_powers(string):
        
        for power in range(2,int(len(string)/len(enumerations[-1])+8)):
            
            for letter in enumerations:
                if string == letter*power:
                    return letter
        
        return string
    
    def reverse(string):
        return string[::-1]
    
    def cyclic(string):
        n = len(string)
        new_string = string
        for i in range(n):
            new_temp_string = [x for x in new_string]
            new_temp_string.insert(0,new_string[-1])
            new_temp_string.pop()
            new_string = ''.join(new_temp_string)
            
                
            for other_string in enumerations:
                if other_string == new_string or inverse(new_string) == other_string:
                    # if string == "AbaB":
                    #     print(enumerations)
                    #     print(inverse(new_string))
                    #     print('did return')
                    return new_string
        return new_string
    

    checklist = [lambda x: x, cyclic,inverse, check_powers]

    def recursive_add(string):
        current_enumeration = []
        all_current_enumerations = []

        for letter in letters:
            all_current_enumerations.append(string+letter)

        for letter in letters:
            if letter == inverse_hash[string[-1]] or letter == inverse_hash[string[0]]:
                continue
            result = ''.join(f'{string}{letter}')
            
            skip = False
            for check in checklist:
                if check(result) in enumerations:
                    
                    skip=True
                    break
            
            

            if not skip: 
                current_enumeration.append(result)

        for result in current_enumeration:
            enumerations.append(result)

        if current_enumeration and len(current_enumeration[-1])>limit:
            return

        for result in all_current_enumerations:
            recursive_add(result)
    
    recursive_add("A")
    
    return enumerations

def convert_string_to_index(string):
    letters = [x for x in string]
    indices = []
    i=0
    while i <= len(letters)-1:
        power = 1
        letter = letters[i]
        index = [letter]
        j=i+1
        while j <= len(letters)-1:
            if letters[i] == letters[j]:
                power+=1
            else:
                break
            j+=1
        index.append(power)
        i=j
        indices.append(index)
    return indices

            
#convert_string_to_index("AAAbABBbbb")



#print(enumerate_classes({"A": "a", "a": "A", "B": "b", "b":"B"},4))

def reduce_conjugacy_class(string):

   

    inverse_hash = {"A": "a", "a": "A", "B": "b", "b":"B"}


    
    if len(string)>=2:
        current_length = len(string)
        next_length = 0
        while next_length < current_length:
            current_length = len(string)
            reduced_string = []
            i = 0
            while i < len(string)-1:
                if string[i] == inverse_hash[string[i+1]]:
                    i+=2
                else:
                    reduced_string.append(string[i])
                    i+=1
            
            if len(string)>=2 and string[-1] != inverse_hash[string[-2]]:
                reduced_string.append(string[-1])
            next_length = len(reduced_string)
            string = ''.join(reduced_string)
            if len(string) == 1:
                break
            next_length = len(reduced_string)
    did_reduce = True
    conjugacy_left = ["A","a","B","b"]
    while did_reduce:
        did_reduce=False
        if len(string)>=2:
            for element in conjugacy_left:
                new_string = [x for x in string]
                
                if new_string[0] == inverse_hash[element] and new_string[-1] == element:
                    new_string.remove(new_string[0])
                    new_string.remove(new_string[-1])

                if len(string)> len(new_string):
                    did_reduce = True
                    string = ''.join(new_string)
                    break
    string = ''.join(string)
    if not string:
        string = "𝟙"
    return string

#print(reduce_conjugacy_class("ABab"))

def k_smallest_lengths_add(k_smallest_lengths, new_length, difference_precision=0.1):

    k = len(k_smallest_lengths)

    smallest_index_larger_than = 0
    while smallest_index_larger_than < k and k_smallest_lengths[smallest_index_larger_than] < new_length + difference_precision:
        smallest_index_larger_than+=1
    if smallest_index_larger_than < k and not abs(k_smallest_lengths[smallest_index_larger_than-1] - new_length) < difference_precision:
        k_lengths_temp = list(k_smallest_lengths)
        k_lengths_temp.pop()
        k_lengths_temp.insert(smallest_index_larger_than,new_length)
        k_smallest_lengths = np.array(k_lengths_temp)
    
    if smallest_index_larger_than == k-1:
        if k_smallest_lengths[smallest_index_larger_than-1] > new_length + difference_precision:
            k_smallest_lengths[-1] = new_length
        

    #print(k_smallest_lengths)
    return k_smallest_lengths

# k_smallest_lengths = [np.inf,np.inf]

# k_smallest_lengths = k_smallest_lengths_add(k_smallest_lengths, 0)
# k_smallest_lengths = k_smallest_lengths_add(k_smallest_lengths, 3.85)


def compute_translation_matrix_torus(x):
    [A,B,a_minus,a_plus,b_minus,b_plus,e_minus,e_plus] = x
    alpha1 = edge_matrix(e_plus,e_minus)*mp.inverse(triangle_matrix(A))*edge_matrix(b_minus, b_plus)*triangle_matrix(B)
    alpha2 = triangle_matrix(B)*edge_matrix(a_plus,a_minus)*mp.inverse(triangle_matrix(A))*edge_matrix(e_minus,e_plus)
    return [alpha1,alpha2]

def a_to_x_coordinate_torus(x):
    [A,B,a_minus,a_plus,b_minus,b_plus,e_minus,e_plus] = x
    qe_plus = compute_q_plus(A,b_minus, B, a_minus)
    qe_minus = compute_q_plus(B,b_plus, A, a_plus)
    A_t = compute_t(a_minus, b_minus, e_minus, a_plus, b_plus, e_plus)
    B_t = compute_t(e_plus, a_plus, b_plus, e_minus, a_minus, b_minus)
    qb_plus = compute_q_plus(A, a_minus, B, e_minus)
    qb_minus = compute_q_plus(B, a_plus, A, e_plus)
    qa_plus = compute_q_plus(A,e_minus, B, b_minus)
    qa_minus = compute_q_plus(B,e_plus, A, b_plus)
    y = np.array([A_t,B_t,qa_minus, qa_plus, qb_minus, qb_plus, qe_minus, qe_plus])
    return y

def get_length(matrix):
    #eigenvalues = np.linalg.eigvals(matrix)
    eigenvalues = mp.eig(mp.matrix(matrix))[0]
    absolute_eigenvalues = [abs(e) for e in eigenvalues]
    absolute_eigenvalues = [absolute_eigenvalues[i] for i in np.argsort(absolute_eigenvalues)]
    smallest_eigenvalue = absolute_eigenvalues[0]
    largest_eigenvalue = absolute_eigenvalues[-1]
    length = mp.log(largest_eigenvalue/smallest_eigenvalue)
    
    return length, eigenvalues


def edge_matrix(q_plus,q_minus):
    coefficient = mp.power((q_plus/q_minus), (1/3))
    matrix = mp.matrix([[0,0,q_minus],[0,-1,0],[1/q_plus, 0, 0]])
    return coefficient*matrix

def triangle_matrix(t):
    coefficient = 1/mp.power(t, (1/3))
    matrix = mp.matrix([[0,0,1],[0,-1,-1],[t,t+1,1]])
    return matrix*coefficient

def string_fraction_to_float(string):
        if '/' in string:
            string = string.rsplit('/')
            return float(string[0])/float(string[1])
        return float(string)

def integer_to_script(value, up=True):

    value = str(value)
    return_value = []
    
    if up:
        superscripts = {"-": "⁻","0": "⁰", "1": "¹","2": "²","3": "³","4": "⁴","5": "⁵","6": "⁶","7": "⁷", "8": "⁸","9": "⁹"}
        
        for digit in value:
            return_value.append(superscripts[digit])
            
    else:
        subscripts = {"0": "₀", "1": "₁", "2": "₂","3": "₃","4": "₄", "5": "₅","6": "₆", "7": "₇", "8": "₈", "9":"₉"}

        for digit in value:
            return_value.append(subscripts[digit])
            
    
    return "".join(return_value)

def beziercurve(P0,P1,P2):
    return lambda t : (1-t)**2*P0+2*(1-t)*t*P1+t**2*P2


def outitude_edge_params(A,B,a_minus,a_plus, b_minus, b_plus, e_minus, e_plus):
    return A*(e_plus*a_plus+e_minus*b_minus-e_minus*e_plus) + B*(e_plus*b_plus+e_minus*a_minus - e_minus*e_plus)

def compute_m_inverse(r0, r2, c0, c2, e03, e23):
    C = np.array([r0, r2, np.cross(c0, c2)])
    A = np.array([[1 / e03, 0, 0], [0, 1 / e23, 0], [0, 0, 1 / (e03 * e23)]])
    B = np.array([c2, c0, np.cross(r2, r0)]).T
    #m_inverse = np.matmul(A, B)
    m_inverse = np.linalg.inv(C)
    return m_inverse


def compute_c3(m_inverse, e03, e23, A023):
    c3 = np.matmul(m_inverse, np.array([[e03], [e23], [A023]]))
    c3 = c3.T.flatten()

    return c3


def compute_r3(c0, c2, c3, e30, e32):
    A = np.array([c0, c2, c3])
    r3 = np.matmul(np.linalg.inv(A), np.array([[e30], [e32], [0]]))
    r3 = r3.T.flatten()
    return r3

def compute_outitude_sign(c0,c1,c2,c3):
    D = [c1,c2,c3]
    D_prime = [c0,c1,c3]
    C = [c0,c1,c2]
    C_prime = [c0,c2,c3]
    return np.linalg.det(D) + np.linalg.det(D_prime) - np.linalg.det(C) - np.linalg.det(C_prime)


def compute_t(a_minus, b_minus, e_minus, a_plus, b_plus, e_plus):
    return a_minus*b_minus*e_minus/(a_plus*b_plus*e_plus)

def compute_q_plus(A, d_minus, B, a_minus):
    return A*d_minus/(B*a_minus)

def compute_all_until_r3c3(r0, r2, c0, c2, e03, e23, e30, e32, A023):
    m_inverse = compute_m_inverse(r0, r2, c0, c2, e03, e23)
    c3 = compute_c3(m_inverse, e03, e23, A023)
    r3 = compute_r3(c0, c2, c3, e30, e32)
    return (r3, c3)