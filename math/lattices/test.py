from vector import Vector

v1 = Vector(846835985, 9834798552)
v2 = Vector(87502093, 123094980)
u1,u2 = Vector.gaussian_lattice_reduction(v1, v2)
print("Les vecteurs le plus court sont : {u1} et {u2}")