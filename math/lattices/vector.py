import math
import numpy as np

class Vector:
    def __init__(self, *components):
        self.components = list(components)
    
    def __add__(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for addition.")
        result_components = [a + b for a, b in zip(self.components, other.components)]
        return Vector(*result_components)
    
    def __sub__(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for subtraction.")
        result_components = [a - b for a, b in zip(self.components, other.components)]
        return Vector(*result_components)
    
    def __mul__(self, scalar):
        result_components = [a * scalar for a in self.components]
        return Vector(*result_components)
    
    def __truediv__(self, scalar):
        result_components = [a / scalar for a in self.components]
        return Vector(*result_components)
    
    def __rmul__(self, scalar):
        result_components = [a * scalar for a in self.components]
        return Vector(*result_components)
    
    def dot(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for dot product.")
        result = sum(a * b for a, b in zip(self.components, other.components))
        return result
    
    def magnitude(self):
        return math.sqrt(sum(a**2 for a in self.components))
    
    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            result_components = [a / mag for a in self.components]
            return Vector(*result_components)
        else:
            return Vector(*[0] * len(self.components))
            
    def gram_schmidt(vectors):
        orthogonal_vectors = []
        
        for v in vectors:
            u = v
            for w in orthogonal_vectors:
                u -= w * (v.dot(w) / w.dot(w))
            orthogonal_vectors.append(u)
        
        return orthogonal_vectors
    
    @staticmethod
    def is_orthogonal(vectors):
        if len(vectors) < 2:
            return True  # Single vector is considered orthogonal to itself

        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                dot_product = vectors[i].dot(vectors[j])
                if abs(dot_product) > 1e-10:  # Use a small tolerance for numerical stability
                    return False

        return True

    @staticmethod
    def is_orthonormal(*vectors):
        # Vérifie si le nombre de vecteurs est au moins 2
        if len(vectors) < 2:
            return False

        # Check if all vectors are normalized
        for vector in vectors:
            if abs(vector.magnitude() - 1) > 1e-10:
                return False

        # Check if all pairs of vectors are orthogonal
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                if abs(vectors[i].dot(vectors[j])) > 1e-10:
                    return False

        return True
    
    @staticmethod
    def volume_of_domain(*vectors):
        # Check if there are enough vectors to form a volume
        if len(vectors) < 2:
            raise ValueError("At least two vectors are required to calculate a volume.")

        # Check if the vectors are in the same dimension
        dimension = len(vectors[0].components)
        for vector in vectors:
            if len(vector.components) != dimension:
                raise ValueError("Vectors must have the same dimension to calculate the volume.")

        # Convert the vectors into a numpy array
        matrix = np.array([vector.components for vector in vectors])

        # Calculate the determinant of the matrix
        volume = abs(np.linalg.det(matrix))

        return volume
    
    @staticmethod
    def gaussian_lattice_reduction(v1, v2):
        # Assurez-vous que v1 est le plus court des deux vecteurs
        if v2.magnitude() < v1.magnitude():
            v1, v2 = v2, v1

        while True:
            # Projetons v2 sur v1 et soustrayons pour obtenir un nouveau v2
            m = round(v2.dot(v1) / v1.dot(v1))
            v2 = v2 - v1 * m

            # Si v2 est maintenant plus court, échangez les vecteurs
            if v2.magnitude() < v1.magnitude():
                v1, v2 = v2, v1
            else:
                break

        # Retourne le vecteur le plus court
        return v1,v2
    
    def __str__(self):
        return "(" + ", ".join(map(str, self.components)) + ")"
    