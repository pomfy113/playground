"""Enter the (Absorbing) Matrix. For fuel.

I didn't know a lick of linear algebra until now! (shouldn't have gone Psych)
Didn't stop me from learning how to do matrices these past few days.
I knew what a Markov model was, but someone had to hint the absorbing Markov
chains. I watched a few vids on it and did all the bits and pieces
COMPLETELY from scratch using just the equations I was given.

I feel confident in doing linear algebra and matrices now. I feel
significantly more confident about transcribing math to code now too.
It's intimidating until after you get into it!

Massive shoutout to mathsisfun.com! Seriously, would not have between
able to do it without this site.
"""

from fractions import Fraction, gcd

class matrix(object):
    """Creating the absorbing Markov matrix for all of this."""

    def __init__(self, fuel):
        """HOO BOY THIS SURE IS A WHOPPER."""
        # Grabbing all unstables
        self.unstable = []
        self.unstable_rows = []
        self.get_unstable(fuel)
        # Grabing sub-matrices

        # Checking to make sure whether we're doing an early exit
        self.answer = self.early_exit_check(fuel)
        if self.answer or sum(fuel[0]) == 0:
            return

        # Submatrices (see function for explanation)
        self.sub_matrixQ = []
        self.sub_matrixR = []
        self.get_sub_matrices()

        # Getting dimensions of that sub_matrix for identity matrix
        self.sm_y = len(self.sub_matrixQ)
        self.sm_x = len(self.sub_matrixQ[0])

        # Identity-matrix
        self.identity_matrix = []
        self.get_identity_matrix()

        # Inversing
        self.sub_matrixF = []
        self.final = []
        self.get_final()

        # Now the final answer!
        self.matrix_answer()

    def get_unstable(self, fuel):
        """Grab all unstable fuel rows."""
        for index, row in enumerate(fuel):
            rowtotal = sum(row)
            # if it's not terminal, add to unstable
            if rowtotal:
                newrow = []
                self.unstable_rows.append(index)
                for item in row:
                    if item:
                        newrow.append(Fraction(item, rowtotal))
                    else:
                        newrow.append(0)
                self.unstable.append(newrow)

    def early_exit_check(self, fuel):
        """For early exit if we start off terminal."""
        # As long as there's instability, we're good to go.
        if self.unstable:
            return []
        else:
            # I mean, it's all 1s if it's empty
            return [1 for _ in xrange(len(fuel)+1)]

    def get_sub_matrices(self):
        """Create the sub matrices.

            Each set in an absorbing Markov Chain has three matrices:
                - Identity matrix:
                    The absorbing state/terminal. A dead end.
                    Once it's here, it STAYS there.
                - Q - transient state:
                    We can go to a transitional state THEN hit a dead end,
                    or we can go back to the transient state again
                - R - transition state:
                    It's a toss-up.
                    Either we go to an identity matrix or a transient state.
        """
        for y in xrange(len(self.unstable)):
            new_rowQ = []
            new_rowR = []
            for x in xrange(len(self.unstable[0])):
                if x in self.unstable_rows:
                    new_rowQ.append(self.unstable[y][x])
                else:
                    new_rowR.append(self.unstable[y][x])
            if new_rowQ:
                self.sub_matrixQ.append(new_rowQ)
            if new_rowR:
                self.sub_matrixR.append(new_rowR)

    def get_identity_matrix(self):
        """Create the identity matrix. Read above function for explanation."""
        for y in xrange(self.sm_y):
            self.identity_matrix.append([0 for _ in xrange(self.sm_x)])
            self.identity_matrix[y][y] = 1

    def get_final(self):
        """Create matrix F and get all needed data."""
        # See docstring for this; creates the sub_matrix F
        self.matrix_combine()

        # We essentially multiply F's row with R's column's.
        # For the result's first row, it's F's first row * the corresponding
        # column in R. We add up ALL the elements, and they pair up.
        for y in xrange(len(self.sub_matrixR)):
            row = []
            to_mult = self.sub_matrixF[y]
            for x in xrange(len(self.sub_matrixR[0])):
                total = 0
                for index, item in enumerate(to_mult):
                    total += (self.sub_matrixR[index][x] * item)
                row.append(total)
            self.final.append(row)

    def matrix_combine(self):
        """Identity matrix minus the Sub-Q, then invert it for F."""
        # Doing this prior to matrix multiplication
        for y in xrange(self.sm_y):
            temp = []
            for x in xrange(self.sm_x):
                # Divided to two lines for readibility
                total_sum = self.identity_matrix[y][x]\
                            - self.sub_matrixQ[y][x]
                temp.append(total_sum)
            self.sub_matrixF.append(temp)
        # See below functions
        self.sub_matrixF = self.getMatrixInverse(self.sub_matrixF)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Everything below is used just for the inversing procedure
# numpy isn't allowed, so I ended up looking up the code for inversing
# The 2x2 matrix is easy, but the others... well, it got really messy
# Credit to the stackoverflow post for this, questions/32114054
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getMatrixInverse(self, m):
        """Main Matrix Inverse function.

        Gauss-Jordan instead is easier on paper, but for programming, well.
        Essentially does it step by step:
            - Grab matrix of minors
            - Turn into matrix of cofactors
            - Adjugate/transpose cofactors
            - Multiply by 1 over determinant
        """
        determinant = self.get_determinant(m)
        # The 2x2 is special. And easy. Alter/swap * determinant
        if len(m) == 2:
            return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]]

        # Otherwise, we're going to have to do it the hard way.
        cofactors = []
        # Make matrix of minors
        for y in xrange(len(m)):
            cofactorRow = []
            for x in xrange(len(m)):
                minor = self.getMatrixMinor(m, y, x)
                cofactorRow.append(((-1)**(y+x)) * self.get_determinant(minor))
            cofactors.append(cofactorRow)

        # Tranposing; we swap diagonals
        cofactors = self.transposeMatrix(cofactors)

        # Now we just multiply by 1/determinant
        for y in xrange(len(cofactors)):
            for x in xrange(len(cofactors)):
                cofactors[y][x] = cofactors[y][x]/determinant
        return cofactors

    def transposeMatrix(self, m):
        """We just sort of swap em."""
        # Zip is interesting, laying out columns like that.
        return map(list, zip(*m))

    def getMatrixMinor(self, m, i, j):
        """Minor. Everything not in the row or column."""
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def get_determinant(self, m):
        """Grab determinant."""
        if len(m) == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]

        # Recursive functions all the way down.
        # We keep going down and down until we hit the final 2x2
        determinant = 0
        for x in xrange(len(m)):
            minor = self.getMatrixMinor(m, 0, x)
            determinant += ((-1) ** x) * m[0][x] * self.get_determinant(minor)
        return determinant

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Everything above is inversing related
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def matrix_answer(self):
        """Final answer: the numerators + denominator."""
        all_denoms = []
        # Need to grab all denominators
        for x in self.final[0]:
            all_denoms.append(x.denominator)
        # Finding lowest common via denominators
        lcm = 1
        for x in all_denoms:
            lcm = (lcm * x) / gcd(lcm, x)

        # Increasing the numerators to LCM
        for x in self.final[0]:
            num = x.numerator
            dem = x.denominator
            if num and dem != lcm:
                num = num * (lcm/dem)
            self.answer.append(num)
        # We can't forget to add the lcm
        self.answer.append(lcm)

def answer(fuel):
    fuel_matrix = matrix(fuel)
    return fuel_matrix.answer



fuel = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [4,0,0,3,2,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],  # s5 is terminal
]

# fuel = [
#     [0, 2, 1, 0, 0],
#     [0, 0, 0, 3, 4],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0]]

print(answer(fuel))
