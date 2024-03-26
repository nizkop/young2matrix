# young2matrix
### Context and Motivation
In chemistry, the interaction between molecules is one of the most significant phenomena. It is essential for understanding the structure, reactivity, and properties of chemical compounds.

Unlike laboratory experiments, where disturbances are never entirely avoidable, quantum chemistry attempts to approach the subject as accurately and detailed as possible by calculating single molecules or a few number of molecules in an empty space. Most of the time, quantum chemical molecules are mathematically unsolvable problems, so many calculation methods work with an iterative gradient descent algorithm.

### Problem
The basis of this project was the calculation of the interaction between two benzene molecules. Within molecules, there are different energy levels where the electrons of a molecule preferentially reside. When electrons transition between these levels, the process is called electronic excitation. This can be initiated, for example, by exposure to light, which is used in solar cells.
During the quantum chemical calculations of these different excitation states in two interacting benzene molecules, inconsistencies arose. To validate the results, a group-theoretical approach was pursued [ref. weissbluth]. This approach shall be automated within the scope of this work.

### Objective
The spatial shape of something, such as molecules, can be described by so-called symmetry groups. This indicates, to what extent the object can be rotated or mirrored in space, while it appears unchanged. The underlying operations of such symmetry groups may be graphically illustrated by Young tableaux. Based on this, a secular equation can be established through various steps using different rules, in which the eigenvalues $E$ of the matrix $H$ correspond to the sought-after energy levels of the molecule. Even though the equation below won't be analytically solvable, statements about the terms contained therein are of great help to understand the chemical basis.   
$$ \text{det}\left( 
\begin{array}{ccc}
H_{11} - S_{11} \cdot E & H_{12} - S_{12} \cdot E & \cdots \\
H_{21} - S_{21} \cdot E & H_{22} - S_{22} \cdot E & \cdots \\
\vdots & \vdots & \\
\end{array}
 \right) \overset{!}{=} 0  $$   

The terms $H$ are referred to as Hamiltonian matrix elements, and the terms $S$ as overlap integrals. Both are based on a product of spatial functions $\Phi$ and spin functions $\sigma$. However, a precise understanding of these terms is not required for this work, as long as the rules (see Table below) governing the mathematical equations are known. Instead, this project focuses on the various steps involved in converting Young tableaux into quantum chemical terms. The goal is to create an automatically generated overview of the various representation types and transformations, as explained in the following table:
